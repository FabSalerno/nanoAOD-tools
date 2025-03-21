import tensorflow as tf
import numpy as np
import json
import matplotlib.pyplot as plt
import ROOT
from sklearn.model_selection import train_test_split
from tensorflow.keras.callbacks import EarlyStopping, ReduceLROnPlateau
import h5py
import os
import argparse
import time
from training_Run3_PF_jets_CNN_2D_LSTM import trainer, train_test_discrimination, train_test_roc

usage       = 'python3 training_Run3.py -s component1,component2,component3 -i /path/to/h5'
example     = 'python3 training_Run3.py -s TT_semilep_2022 -i /eos/user/f/fsalerno/framework/MachineLearning/Training_PF_2022_1_jets/trainingSet.h5 -m /eos/user/f/fsalerno/framework/MachineLearning/Training_PF_2022_1/model.h5 -j /eos/user/f/fsalerno/framework/MachineLearning/Training_PF_2022_1/score_thresholds.json -g /eos/user/f/fsalerno/framework/MachineLearning/Training_PF_2022_1/graphics'
parser      = argparse.ArgumentParser(usage)
parser.add_argument('-i', '--inFile',     dest = 'inFile',    required = True,                                              type = str,      help = 'complete path to the input folder containing the h5s')
parser.add_argument('-m', '--outModel',   dest = 'outModel',  required = False,   default = './model.h5',                   type = str,      help = 'complete path to save the model (default "./model.h5")')
parser.add_argument('-j', '--outJson',    dest = 'outJson',   required = False,   default = './score_thresholds.json',      type = str,      help = 'complete path to save the score thresholds (default "./score_thresholds.json")')
parser.add_argument('-g', '--graphics',   dest = 'graphics',  required = False,   default = './graphics',                   type = str,      help = 'complete path to save the graphics (default "./graphics")')
parser.add_argument('-n', '--nPFCs',      dest = 'nPFCs',     required = True,   default = 40,                              type = int,      help = 'number of particles used for training (default "20")')

args                    = parser.parse_args()
inFile                  = args.inFile
outModel                = args.outModel
path_to_outJson         = args.outJson
path_to_graphics_folder = args.graphics
nPFCs                   = args.nPFCs
verbose                 = True
path_to_best_hps        = "/afs/cern.ch/user/f/fsalerno/CMSSW_13_2_11/src/PhysicsTools/NanoAODTools/python/postprocessing/machine_learning/Training/best_hps_trota.json"

if not os.path.exists(path_to_graphics_folder):
    os.makedirs(path_to_graphics_folder)
    print(f"Directory {path_to_graphics_folder} created")

####### DATASET LOADING #######
t0 = time.time()
# Verifica che il file HDF5 sia valido
try:
    with h5py.File(inFile, 'r') as f:
        print("File is a valid HDF5 file")
except Exception as e:
    print(f"Error: {e}")

with h5py.File(inFile, 'r') as f:
    # Verifica che il gruppo e i dataset esistano
    if 'data' in f:
        data_group = f['data']
        
        # Accedere ai dataset
        jets_data = data_group['jets'][:]
        fatjets_data = data_group['fatjets'][:]
        PFC_data = data_group['PFC'][:]
        top_data = data_group['top'][:]
        labels_data = data_group['labels'][:]

        # Verifica i dati letti (ad esempio la forma dei dati)
        print(f"Jets shape: {jets_data.shape}")
        print(f"Fatjets shape: {fatjets_data.shape}")
        print(f"PFC shape: {PFC_data.shape}")
        print(f"Top shape: {top_data.shape}")
        print(f"Labels shape: {labels_data.shape}")
    else:
        print("Il gruppo 'data' non è presente nel file.")



X_jet                     = jets_data 
X_fatjet                  = fatjets_data 
X_PFC                     = PFC_data
X_PFC                     = X_PFC[:,:nPFCs,:]
X_top                     = top_data
y                         = labels_data
data                      = X_jet, X_fatjet, X_PFC, X_top, y

# Caricamento dei migliori iperparametri (assicurati che il file esista)
with open("path_to_best_hps.json", "r") as f:
    best_hps = json.load(f)

# ---------------------------
# Creazione dell'istanza del trainer per il fine tuning
trainer_ft = trainer(X_jet, X_fatjet, X_PFC, X_top, y, best_hps)

# Carica il modello precedentemente salvato (il modello "vecchio")
model_path = f"/eos/user/f/fsalerno/framework/MachineLearning/Training_PF_2022_1/Training_PF_2022_1_jets_60_boosted_0_pt/Training_PF_2022_1_jets_60_boosted_CNN_2D_LSTM_0_pt/model.h5"  # Cambia con il tuo percorso
trainer_ft.load_model(model_path)

# ---------------------------
# Freeze (congelamento) di alcuni strati per evitare di modificare troppo le feature già apprese
# In questo esempio congeliamo tutti gli strati tranne gli ultimi 5.
for layer in trainer_ft.model.layers[:-5]:
    layer.trainable = False

# Dopo aver modificato i flag di trainabilità, è necessario ricompilare il modello.
trainer_ft.model.compile(optimizer=tf.keras.optimizers.Nadam(learning_rate=0.00001),
                         loss=tf.keras.losses.BinaryCrossentropy(),
                         metrics=[tf.keras.metrics.AUC()])

# ---------------------------
# Divisione dei nuovi dati in training e test (se non l'hai già fatto)
trainer_ft.split(test_size=0.2)

# ---------------------------
# Parametri per il fine tuning
epochs = 1000
batch_size = 128

# Esecuzione del fine tuning sul nuovo dataset
trainer_ft.training(validation_split=0.3, epochs=epochs, batch_size=batch_size, 
                    save_model=True, path_to_model=f"{outModel}", verbose=True)

# ---------------------------
# Valutazione del modello fine tuned
eval_result = trainer_ft.evaluate()
print("Risultato della valutazione dopo il fine tuning:", eval_result)

trainer_ft.train_test_discrimination(bins=100)
fpr, tpr, trs   = trainer_ft.train_test_roc()

if verbose:
    print('10%   trs', trs[fpr<0.1][-1], 'tpr ', tpr[fpr<0.1][-1])
    print('5%    trs', trs[fpr<0.05][-1], 'tpr ', tpr[fpr<0.05][-1])
    print('1%    trs', trs[fpr<0.01][-1], 'tpr ', tpr[fpr<0.01][-1])
    print('0.1%  trs', trs[fpr<0.001][-1], 'tpr ', tpr[fpr<0.001][-1])

### Saving thresholds to dictionary ###
fprs_exp            = [("10%", 0.1), ("5%", 0.05), ("1%", 0.01), ("0.1%", 0.001)]
score_thrs          = {}
for fpr_exp in fprs_exp:
    score_thrs[fpr_exp[0]]        = {}
    score_thrs[fpr_exp[0]]["fpr"] = float(fpr[fpr<fpr_exp[1]][-1])
    score_thrs[fpr_exp[0]]["thr"] = float(trs[fpr<fpr_exp[1]][-1])
    score_thrs[fpr_exp[0]]["tpr"] = float(tpr[fpr<fpr_exp[1]][-1])

print('score_thrs.keys();         ', score_thrs.keys())
print('score_thrs["0.1%"].keys(): ', score_thrs["0.1%"].keys())
print('score_thrs["0.1%"]["fpr"]: ', score_thrs["0.1%"]["fpr"])
print('score_thrs["0.1%"]["thr"]: ', score_thrs["0.1%"]["thr"])
print('score_thrs["0.1%"]["tpr"]: ', score_thrs["0.1%"]["tpr"])

with open(path_to_outJson, "w") as f:
    json.dump(score_thrs, f, indent=4)

# summarize history for auc
metric  = "auc" #"auc"
history = trainer_ft.history
fig, ax = plt.subplots(ncols=2, figsize=(25,10))
for var in history.history.keys():
    if ("loss" in var) and (not "val" in var): ax[1].plot(history.history[var], label="train")
    if "val_loss" in var: ax[1].plot(history.history[var], label ="val")
    if (f"{metric}" in var) and (not "val" in var): ax[0].plot(history.history[var], label="train")
    if f"val_{metric}" in var : ax[0].plot(history.history[var], label ="val")

ax[0].set_title(f"model {metric}")
ax[0].set_ylabel(f"{metric}")
ax[0].set_xlabel("epoch")
ax[0].legend()
# summarize history for loss
ax[1].set_title("model loss")
ax[1].set_ylabel("loss")
ax[1].set_xlabel("epoch")
ax[1].legend()
ax[1].set_yscale("log")
plt.savefig(f"{path_to_graphics_folder}/{metric}_loss.png")
plt.savefig(f"{path_to_graphics_folder}/{metric}_loss.pdf")
t_final = time.time()-t0
print(f"done in {t_final} s")
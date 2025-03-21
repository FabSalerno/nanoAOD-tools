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
old_dataset_file        = "/eos/user/f/fsalerno/framework/MachineLearning/TrainingSet_PF_folder/trainingSet_preprocessed_0_pt.h5"
old_model               = f"/eos/user/f/fsalerno/framework/MachineLearning/Training_PF_2022_1/Training_PF_2022_1_jets_60_boosted_0_pt/Training_PF_2022_1_jets_60_boosted_CNN_2D_LSTM_0_pt/model.h5"

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


new_X_jet                     = jets_data 
new_X_fatjet                  = fatjets_data 
new_X_PFC                     = PFC_data
new_X_PFC                     = new_X_PFC[:,:nPFCs,:]
new_X_top                     = top_data
new_y                         = labels_data
new_data                      = new_X_jet, new_X_fatjet, new_X_PFC, new_X_top, new_y


# --- Caricamento dei vecchi dati ---
with h5py.File(old_dataset_file, 'r') as f:
    data_group = f['data']
    old_data_jet = data_group['jets'][:]
    old_data_fatjet = data_group['fatjets'][:] 
    old_data_PFC = data_group['PFC'][:]
    old_data_top = data_group['top'][:]
    old_data_labels = data_group['labels'][:]

old_X_jet = old_data_jet
old_X_fatjet = old_data_fatjet
old_X_PFC = old_data_PFC
old_X_PFC = old_X_PFC[:,:nPFCs,:]
old_X_top = old_data_top
old_y = old_data_labels



# --- Caricamento degli iperparametri ---
with open("path_to_best_hps.json", "r") as f:
    best_hps = json.load(f)

# --- Creazione dell'istanza del trainer per il fine tuning sui nuovi dati ---
trainer_ft = trainer(new_X_jet, new_X_fatjet, new_X_PFC, new_X_top, new_y, best_hps)
trainer_ft.split(test_size=0.3)

# Carica il vecchio modello pre-addestrato (teacher) nel modello corrente
trainer_ft.load_model(old_model)

# --- Creazione del teacher model (clone del vecchio modello) ---
teacher_model = tf.keras.models.clone_model(trainer_ft.model)
teacher_model.set_weights(trainer_ft.model.get_weights())
teacher_model.trainable = False  # Il teacher non viene aggiornato

# --- Preparazione dei dati per il fine tuning ---
batch_size = 128
epochs = 1000

# Definisci il dizionario degli input per il training (nuovi dati)
new_data = {
    "fatjet": trainer_ft.X_fatjet_train,
    "jet": trainer_ft.X_jet_train,
    "PFC": trainer_ft.X_PFC_train,
    "top": trainer_ft.X_top_train
}

# Calcola le predizioni del teacher sui nuovi dati
teacher_preds = teacher_model.predict(new_data, batch_size=batch_size)

# Costruiamo un tf.data.Dataset che restituisce (input, etichetta, predizione del teacher)
dataset = tf.data.Dataset.from_tensor_slices((
    trainer_ft.X_fatjet_train,
    trainer_ft.X_jet_train,
    trainer_ft.X_PFC_train,
    trainer_ft.X_top_train,
    trainer_ft.y_train,
    teacher_preds
))
dataset = dataset.batch(batch_size)

# --- Definizione della loss LwF ---
def lwf_loss_fn(y_true, y_pred, teacher_pred, alpha=0.5, temperature=3.0):
    """
    Combina la Binary Crossentropy sul nuovo task e una distillation loss
    che penalizza la divergenza tra le predizioni dello student e quelle del teacher.
    """
    # Loss standard sul nuovo task
    ce_loss = tf.keras.losses.BinaryCrossentropy()(y_true, y_pred)
    
    # Calcola i logits a partire dalle probabilità (evitando divisioni per zero)
    student_logits = tf.math.log(tf.clip_by_value(y_pred, 1e-7, 1 - 1e-7)) - tf.math.log(tf.clip_by_value(1 - y_pred, 1e-7, 1 - 1e-7))
    teacher_logits = tf.math.log(tf.clip_by_value(teacher_pred, 1e-7, 1 - 1e-7)) - tf.math.log(tf.clip_by_value(1 - teacher_pred, 1e-7, 1 - 1e-7))
    
    # Applica il temperature scaling
    student_scaled = student_logits / temperature
    teacher_scaled = teacher_logits / temperature
    
    # Converti in distribuzioni a due classi: il secondo logit lo assumiamo zero
    student_logits_2class = tf.stack([student_scaled, tf.zeros_like(student_scaled)], axis=-1)
    teacher_logits_2class = tf.stack([teacher_scaled, tf.zeros_like(teacher_scaled)], axis=-1)
    
    student_dist = tf.nn.softmax(student_logits_2class)
    teacher_dist = tf.nn.softmax(teacher_logits_2class)
    
    kl_loss = tf.keras.losses.KLDivergence()(teacher_dist, student_dist)
    
    return alpha * ce_loss + (1 - alpha) * kl_loss

# --- Training loop custom per LwF ---
optimizer = tf.keras.optimizers.Nadam(learning_rate=1e-5)
trainer_ft.split(test_size=0.1)

for epoch in range(epochs):
    epoch_loss = 0.0
    for fatjet_batch, jet_batch, PFC_batch, top_batch, y_batch, teacher_batch in dataset:
        x_batch = {
            "fatjet": fatjet_batch,
            "jet": jet_batch,
            "PFC": PFC_batch,
            "top": top_batch
        }
        with tf.GradientTape() as tape:
            y_pred = trainer_ft.model(x_batch, training=True)
            loss_value = lwf_loss_fn(y_batch, y_pred, teacher_batch, alpha=0.5, temperature=3.0)
        grads = tape.gradient(loss_value, trainer_ft.model.trainable_variables)
        optimizer.apply_gradients(zip(grads, trainer_ft.model.trainable_variables))
        epoch_loss += loss_value.numpy()
    print(f"Epoch {epoch+1}/{epochs} - Loss: {epoch_loss/len(dataset):.4f}")
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
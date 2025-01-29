#!/usr/bin/env python3
##### FIX SEED #####
seed_value= 0
import os
os.environ['PYTHONHASHSEED']=str(seed_value)

scram_arch = os.getenv('SCRAM_ARCH')
if scram_arch:
    print(f'SCRAM_ARCH is set to: {scram_arch}')
else:
    print('SCRAM_ARCH is not set')

import random
random.seed(seed_value)
import numpy as np
np.random.seed(seed_value)
import keras
import tensorflow as tf
tf.random.set_seed(12345)
#settings delle configurazioni
session_conf = tf.compat.v1.ConfigProto(intra_op_parallelism_threads=1, inter_op_parallelism_threads=1)
sess = tf.compat.v1.Session(graph=tf.compat.v1.get_default_graph(), config=session_conf)
from keras import backend as K
K.set_session(sess)




# import tensorflow as tf
# from tensorflow import keras
import keras_tuner as kt
import pickle as pkl
# import random
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, roc_auc_score, accuracy_score, f1_score, confusion_matrix, auc, roc_curve
from tensorflow.keras.layers import Dense, Dropout, LSTM, concatenate, GRU,Masking, Activation, TimeDistributed, Conv1D, BatchNormalization, MaxPooling1D, Reshape, Flatten
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.wrappers.scikit_learn import KerasClassifier
from tensorflow.keras.callbacks import EarlyStopping
from tensorflow.keras.utils import plot_model, to_categorical
from tensorflow.keras.backend import sigmoid
from tensorflow.keras import regularizers
from keras.utils.generic_utils import get_custom_objects
import matplotlib.pyplot as plt
import ROOT
import json
import mplhep as hep
hep.style.use(hep.style.CMS)





ROOT.gROOT.SetBatch()
ROOT.gStyle.SetOptStat(0)

# Datasets
# from PhysicsTools.NanoAODTools.postprocessing.my_analysis.my_framework.MLstudies.Training.Datasets import *
# import PhysicsTools.NanoAODTools.postprocessing.my_analysis.my_framework.MLstudies.Training.Datasets as Datasets

######### Create arguments to insert from shell #########
from argparse import ArgumentParser
parser          = ArgumentParser()
parser.add_argument("-save_graphics",               dest="save_graphics",               default=False,    required=False,    type=bool,   help="True if want to save plots")
parser.add_argument("-pt_flatten",                  dest="pt_flatten",                  default=False,    required=False,    type=bool,   help="True if want to run on pt-flattened dataset")
parser.add_argument("-path_to_pkl_folder",          dest="path_to_pkl_folder",          default=None,     required=True,     type=str,    help="folder where pkl is saved")
parser.add_argument("-pklName",                     dest="pklName",                     default=None,     required=True,     type=str,    help="name of pkl file")
parser.add_argument("-path_to_graphics_folder",     dest="path_to_graphics_folder",     default=None,     required=True,     type=str,    help="folder to save plots to")
parser.add_argument("-path_to_model_folder",        dest="path_to_model_folder",        default=None,     required=True,     type=str,    help="folder to save model to")
parser.add_argument("-modelName",                   dest="modelName",                   default=None,     required=True,     type=str,    help="name of model file (usually .h5)")
options         = parser.parse_args()

### ARGS ###
save_graphics             = options.save_graphics      
pt_flatten                = options.pt_flatten  
path_to_pkl_folder        = options.path_to_pkl_folder          
pklName                   = options.pklName
path_to_graphics_folder   = options.path_to_graphics_folder              
path_to_model_folder      = options.path_to_model_folder              
modelName                 = options.modelName
path_to_model             = f"{path_to_model_folder}/{modelName}"
path_to_pkl               = f"{path_to_pkl_folder}/{pklName}"
##prova
print("Current working directory:", os.getcwd())
print("Path to pkl file:", path_to_pkl)
#fine prova

with open(path_to_pkl, "rb") as fpkl:
    dataset = pkl.load(fpkl)



#usage="python3 grid_search_hotvr.py -save_graphics {save_graphics} -pt_flatten {pt_flatten} -path_to_pkl_folder {path_to_pkl_folder} -pklName  -path_to_graphics_folder {path_to_graphics_folder} -path_to_model_folder /afs/cern.ch/user/f/fsalerno/CMSSW_12_5_2/src/PhysicsTools/NanoAODTools/python/postprocessing/machine_learning/Training/GridSearch/models -modelName {modelName}

# components = ["tDM_Mphi50_2018", "tDM_Mphi500_2018", "tDM_Mphi1000_2018", "TprimeBToTZ_M800_2018", "TprimeBToTZ_M1200_2018", "TprimeBToTZ_M1800_2018", "ZJetsToNuNu_HT2500ToInf_2018", "ZJetsToNuNu_HT1200To2500_2018"]
# components = ["tDM_Mphi50_2018", "tDM_Mphi500_2018", "tDM_Mphi1000_2018", "TprimeBToTZ_M1800_2018", "TT_Mtt_1000toInf_2018", "ZJetsToNuNu_HT2500ToInf_2018", "ZJetsToNuNu_HT1200To2500_2018"]
# components = ["tDM_Mphi50_2018", "tDM_Mphi500_2018", "tDM_Mphi1000_2018", "TprimeToTZ_1800_2018", "TT_Mtt_1000toInf_2018", "ZJetsToNuNu_HT2500ToInf_2018", "ZJetsToNuNu_HT1200To2500_2018"]
components = [  
            'QCD_HT1000_2018', 
            'QCD_HT1500_2018',
            'QCD_HT2000_2018', 
            'QCD_HTInf_2018', 
            'TT_Mtt1000toInf_2018', 
            'TT_Mtt700to1000_2018', 
            'TT_semilep_2018'
                # "tDM_Mphi50_2018", 
                # "tDM_Mphi500_2018",
                # "tDM_Mphi1000_2018", 
                #"TprimeToTZ_1800_2018", 
                #"TprimeBToTZ_M1800_2018", 
                #"TT_Mtt_1000toInf_2018", 
                #"ZJetsToNuNu_HT2500ToInf_2018", 
                #"ZJetsToNuNu_HT1200To2500_2018"
                #"TT_hadr_2018",
                # "QCD_HT100to200_2018",
                # "QCD_HT200to300_2018",
                # "QCD_HT300to500_2018",
                # "QCD_HT500to700_2018",
                #"QCD_HT700to1000_2018",
                #"QCD_HT1000to1500_2018",
                #"QCD_HT1500to2000_2018",
                #"QCD_HT2000toInf_2018"
            ]



categories    = ["3j1fj", "3j0fj", "2j1fj", "1hvrj"]


### DATASET BALANCING (remove some False Tops) ###
for c in components:
    for cat in categories:
        idx_truetop  = [i for i, x in enumerate(dataset[c][cat][4]==1) if x==True]
        idx_falsetop = [i for i, x in enumerate(dataset[c][cat][4]==0) if x==True]
        print("stiamo selezionando i top per:",c,"",cat)
        if len(idx_truetop)==0:
            ids_todrop   = random.sample(idx_falsetop, int(len(idx_falsetop)*(0.9)))
        elif len(idx_falsetop)>2*len(idx_truetop):    
            ids_todrop   = random.sample(idx_falsetop, len(idx_falsetop)-2*len(idx_truetop))
        else:
            ids_todrop=[]
        dataset[c][cat][0] = np.delete(dataset[c][cat][0], ids_todrop, axis=0)
        dataset[c][cat][1] = np.delete(dataset[c][cat][1], ids_todrop, axis=0)
        dataset[c][cat][2] = np.delete(dataset[c][cat][2], ids_todrop, axis=0)
        dataset[c][cat][3] = np.delete(dataset[c][cat][3], ids_todrop, axis=0)
        dataset[c][cat][4] = np.delete(dataset[c][cat][4], ids_todrop, axis=0)
        


X_jet      = np.concatenate([dataset[c][cat][0] for c in components for cat in categories])
X_fatjet   = np.concatenate([dataset[c][cat][1] for c in components for cat in categories])
X_hotvrjet = np.concatenate([dataset[c][cat][2] for c in components for cat in categories])
X_top      = np.concatenate([dataset[c][cat][3] for c in components for cat in categories])         
y          = np.concatenate([dataset[c][cat][4] for c in components for cat in categories])





X_jet_train, X_jet_test, X_fatjet_train, X_fatjet_test, X_hotvrjet_train, X_hotvrjet_test, X_top_train, X_top_test, y_train, y_test = train_test_split(X_jet, X_fatjet, X_hotvrjet, X_top, y, stratify=y, shuffle=True, test_size=0.3)
print(X_jet_train.shape, X_jet_test.shape, X_fatjet_train.shape, X_fatjet_test.shape, X_hotvrjet_train.shape, X_hotvrjet_test.shape, X_top_train.shape, X_top_test.shape, y_train.shape, y_test.shape)
print(y_train.shape, y_test.shape)
print(np.sum(y_train), np.sum(y_test))


### Define HYPERMODEL for GridSearch ###
InputShape_HOTVRJet=X_hotvrjet_train.shape[1]
InputShape_FatJet=X_fatjet_train.shape[1]
InputShape_Jet=X_jet_train.shape[2]
InputShape_Top=X_top_train.shape[1]
dropout=0.3

# dropout = hp.Boolean("dropout")
# lr = hp.Float("lr", min_value=1e-4, max_value=1e-2, sampling="log")

def model_builder(hp):


    # Input Layers
    hvrj_inputs = tf.keras.Input(shape=(InputShape_HOTVRJet,), name="hotvrjet")  #x
    fj_inputs   = tf.keras.Input(shape=(InputShape_FatJet,),   name="fatjet")    #y
    jet_inputs  = tf.keras.Input(shape=(None,InputShape_Jet,), name="jet")       #z
    top_inputs  = tf.keras.Input(shape=(InputShape_Top,),      name="top")       #t
    ### Operations on FATJET Input Layer ###
    x = BatchNormalization()(hvrj_inputs)
    # Tune parameters for FatJet Input Layer #
#     fj_units              = hp.Int("fj_units", min_value=1, max_value=20, step=1)
    hvrj_units              = hp.Int("hvrj_units", min_value=1, max_value=10, step=1)
    hvrj_activation         = hp.Choice("hvrj_activation", values=["relu", "sigmoid", "tanh"])
#     fj_kernel_initializer = hp.Choice("fj_kernel_initializer", values=["glorot_uniform", "glorot_normal", "random_uniform", "random_normal", "zeros", "ones"])
    hvrj_kernel_initializer = hp.Choice("hvrj_kernel_initializer", values=["random_uniform", "random_normal"])
    x                     = Dense(units=hvrj_units,
                                  activation=hvrj_activation,
                                  kernel_initializer=hvrj_kernel_initializer
                                 )(x)
    ### Operations on FATJET Input Layer ###
    y = BatchNormalization()(fj_inputs)
    # Tune parameters for FatJet Input Layer #
#     fj_units              = hp.Int("fj_units", min_value=1, max_value=20, step=1)
    fj_units              = hp.Int("fj_units", min_value=1, max_value=10, step=1)
    fj_activation         = hp.Choice("fj_activation", values=["relu", "sigmoid", "tanh"])
#     fj_kernel_initializer = hp.Choice("fj_kernel_initializer", values=["glorot_uniform", "glorot_normal", "random_uniform", "random_normal", "zeros", "ones"])
    fj_kernel_initializer = hp.Choice("fj_kernel_initializer", values=["random_uniform", "random_normal"])
    y                     = Dense(units=fj_units,
                                  activation=fj_activation,
                                  kernel_initializer=fj_kernel_initializer
                                 )(y)
    ### Operations on JET Input Layer ###
    z = Masking(mask_value=0.)(jet_inputs)
    z = BatchNormalization()(z)
    # Tune parameters for Jet Input Layer #
    # j_units              = hp.Int("j_units", min_value=1, max_value=20, step=1)
    j_units              = hp.Int("j_units", min_value=1, max_value=10, step=1)
    j_activation         = hp.Choice("j_activation", values=["relu", "sigmoid", "tanh"])
    # j_activation         = hp.Choice("j_activation", values=["relu"])
#     j_kernel_initializer = hp.Choice("j_kernel_initializer", values=["glorot_uniform", "glorot_normal", "random_uniform", "random_normal", "zeros", "ones"])
    j_kernel_initializer = hp.Choice("j_kernel_initializer", values=["random_uniform", "random_normal"])
    j_dropout            = hp.Choice("j_dropout", values=list(np.arange(0,1,0.3)))
#     y = keras.layers.SimpleRNN(5, activation="relu", kernel_initializer="random_normal")(y)
    z                    = keras.layers.LSTM(units=j_units,
                                             activation=j_activation,
                                             kernel_initializer=j_kernel_initializer,
                                             dropout=j_dropout
                                            )(z)

    ### Operations on TOP Input Layer ###
    t = Dense(units=1,
              activation="relu"
              )(top_inputs)
    ### Operations on JET+FATJET Input Layer ###
    x = concatenate([x,y])
    x = concatenate([x,z])
    x = concatenate([x,t])
    x = Dense(units=5,
              activation="relu",
              kernel_initializer="random_normal"
              )(x)
#     x = Dropout(dropout)(x)

    outputs = Dense(1, activation="sigmoid")(x) 
    model   = tf.keras.Model(inputs=[hvrj_inputs, fj_inputs, jet_inputs, top_inputs], outputs=outputs)
    
    # things
    l_rate  = hp.Float("learning_rate", 1e-4, 1e-1, sampling="log", default=1e-3)
    # trainer = tf.keras.optimizers.Adam(learning_rate=0.05)
    trainer = tf.keras.optimizers.Adam(learning_rate=l_rate)
    loss    = tf.keras.losses.BinaryCrossentropy()
    model.compile(optimizer=trainer, loss=loss, metrics=[tf.keras.metrics.AUC()])
    model.summary()
    return model



########## GRIDSEARCH ##########
epochs        = 1000
# batch_size    = 50
batch_size    = 250
# Define the objective as a Keras Tuner Objective
objective = kt.Objective("val_auc", direction="max")
# keras_tuner.RandomSearch
tuner = kt.Hyperband(model_builder,
                     objective=objective,
                     max_epochs=epochs,
                     factor=3,
                     directory=f"{path_to_model_folder}/my_dir",
                     project_name="project"
                    )

tuner.search_space_summary()

### CALLBACKS FUNCTIONS ###
# early_stop = keras.callbacks.EarlyStopping(monitor="val_loss",
#                                            mode="min", # quantity that has to be monitored(to be minimized in this case)
#                                            patience=40, # number of epochs with no improvement after which training will be stopped.
#                                            min_delta=1e-5,
#                                            restore_best_weights=True) # update the model with the best-seen weights
early_stop = keras.callbacks.EarlyStopping(monitor="val_auc",
                                            mode="max", # quantity that has to be monitored(to be minimized in this case)
                                            patience=40, # number of epochs with no improvement after which training will be stopped.
                                            min_delta=1e-5,
                                            restore_best_weights=True) # update the model with the best-seen weights

# Reduce learning rate when a metric has stopped improving
reduce_LR = keras.callbacks.ReduceLROnPlateau(monitor="val_auc",
                                                mode="max",# quantity that has to be monitored
                                                min_delta=1e-10,
                                                factor=0.1, # factor by which LR has to be reduced...
                                                patience=10, #...after waiting this number of epochs with no improvements on monitored quantity
                                                min_lr=1e-15) 
callback_list = [early_stop, reduce_LR]


### GRIDSEARCH Optimization ###
tuner.search({"hotvrjet": X_hotvrjet_train, "fatjet": X_fatjet_train, "jet": X_jet_train, "top": X_top_train}, y_train,
             validation_split=0.3, shuffle=True, callbacks=callback_list,
             epochs=epochs, batch_size=batch_size, verbose=1
            )

# Get the optimal hyperparameters
best_hps = tuner.get_best_hyperparameters(num_trials=1)
print(f"BEST HPS FOUND:\n{best_hps[0].values}")

# Save best_hps to json file
with open(f"{path_to_model_folder}/best_hps.json", "w") as jsFile:
    # f.write(best_hps[0].values)
    json.dump(best_hps[0].values, jsFile, indent=4)


# # Build the model with the optimal hyperparameters and train it on the data
# best_tuner = kt.Hyperband(model_builder,
#                           objective=objective,
#                           max_epochs=epochs,
#                           factor=3,
#                           directory=f"{path_to_model_folder}/opt_dir",
#                           project_name="intro_to_kt")
# model    = best_tuner.hypermodel.build(best_hps[0])
# history  = model.fit({"fatjet": X_fatjet_train, "jet": X_jet_train, "top": X_top_train}, y_train, callbacks=callback_list, 
#                     validation_split=0.3,
#                     epochs=epochs, batch_size=batch_size, verbose=1)

# # Save the entire model to a HDF5 file.
# # The ".h5" extension indicates that the model should be saved to HDF5.
# model.save(path_to_model)

# # list all data in history
# print(history.history.keys())
# # summarize history for accuracy
# fig, ax = plt.subplots(ncols=2, figsize=(25,10))
# for var in history.history.keys():
#     if ("loss" in var) and (not "val" in var): ax[1].plot(history.history[var], label="train")
#     if "val_loss" in var: ax[1].plot(history.history[var], label="val")
#     if ("auc" in var) and (not "val" in var): ax[0].plot(history.history[var], label="train")
#     if "val_auc" in var : ax[0].plot(history.history[var], label="val")

# ax[0].set_title("model accuracy")
# ax[0].set_ylabel("auc")
# ax[0].set_xlabel("epoch")
# ax[0].legend()
# # summarize history for loss
# ax[1].set_title("model loss")
# ax[1].set_ylabel("loss")
# ax[1].set_xlabel("epoch")
# ax[1].legend()
# ax[1].set_yscale("Log")
# if save_graphics:
#     plt.savefig(f"{path_to_graphics_folder}/auc_loss.png")


# ######## MODEL EVALUATION on Test Set ########
# eval_result  = model.evaluate({"fatjet": X_fatjet_test, "jet": X_jet_test, "top": X_top_test}, y_test)
# print("[test loss, test accuracy]:", eval_result)
# y_pred       = model.predict({"fatjet": X_fatjet_test, "jet": X_jet_test, "top": X_top_test})
# y_pred_train = model.predict({"fatjet": X_fatjet_train, "jet": X_jet_train, "top": X_top_train})


# y_pred_train_bkg = y_pred_train[y_train==0]
# y_pred_train_sgn = y_pred_train[y_train==1]
# y_pred_bkg       = y_pred[y_test==0]
# y_pred_sgn       = y_pred[y_test==1]


# bins    = 20
# fig, ax = plt.subplots(figsize=(10,10))

# bins_count_bkg = ax.hist(y_pred_train_bkg, alpha=0.3, color="blue", 
#                          density=True, label="B (train)", range=[0,1], bins=bins)
# bins_count_sgn = ax.hist(y_pred_train_sgn, alpha=0.3,color="red", 
#                          density=True, label="S (train)", range=[0,1], bins=bins)

# hist, bins  = np.histogram(y_pred_bkg, range = [0,1], bins=bins, density=True)
# scale       = len(y_pred_bkg) / sum(hist)
# err         = np.sqrt(hist * scale) / scale
# center      = (bins[:-1] + bins[1:]) / 2
# ax.errorbar(center, hist, yerr=err, fmt="o", c="b", label="B (test)")

# hist, bins  = np.histogram(y_pred_sgn, range = [0,1], bins=bins, density=True)
# scale       = len(y_pred_sgn) / sum(hist)
# err         = np.sqrt(hist * scale) / scale
# center      = (bins[:-1] + bins[1:]) / 2
# ax.errorbar(center, hist, yerr=err, fmt="o", c="r", label="S (test)")
# ax.set_xlabel("score")
# ax.set_ylabel("arbitrary units")
# ax.legend()
# plt.yscale("Log")
# if save_graphics:
#     plt.savefig(f"{path_to_graphics_folder}/traintestDiscrimination.png")
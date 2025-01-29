import pickle as pkl
import keras
import tensorflow as tf
import numpy as np
import json
import sys
import os
####### PARAMETERS #######
nPFCs=20
model="transformer"
#LSTM, CNN, CNN_2D, CNN_2D_prova, transformer, 
path_to_folder= f"/eos/user/f/fsalerno/framework/MachineLearning/Training_PF_2022_2_jets_{nPFCs}_boosted_{model}"

# training set to update
inFile             = f"/eos/user/f/fsalerno/framework/MachineLearning/Training_PF_2022_1_jets_{nPFCs}_boosted/trainingSet.pkl"
# updated training set
outFile            = f"/eos/user/f/fsalerno/framework/MachineLearning/Training_PF_2022_2_jets_{nPFCs}_boosted_{model}/trainingSet.pkl"
# model to load
model_to_load      = f"/eos/user/f/fsalerno/framework/MachineLearning/Training_PF_2022_1_jets_{nPFCs}_boosted_{model}/model.h5"  
# score thresholds
score_thresholds=f"/eos/user/f/fsalerno/framework/MachineLearning/Training_PF_2022_1_jets_{nPFCs}_boosted_{model}/score_thresholds_{nPFCs}_{model}.json"
thr                = "10%"                                                 # threshold to select top candidates

########## MAKE DIRECTORY #########
if not os.path.exists(path_to_folder):
    os.makedirs(path_to_folder)
    print(f"Directory {path_to_folder} created")

####### DATASET LOADING AND PREPROCESSING #######
with open(inFile, "rb") as fpkl:
    dataset = pkl.load(fpkl)
components  = dataset.keys()
categories  = ['3j0fj', '3j1fj', '2j1fj']

# load model & thresholds #
model           = tf.keras.models.load_model(model_to_load)
with open(score_thresholds, "r") as fjson:
    thresholds  = json.load(fjson)
thresholds   = thresholds[thr]["thr"] #lo fisso perchè è complesso trovare il file
print(thresholds)

### Remove Empty Components ###
components_todrop = []
for c in components:
    for cat in categories:
        if (dataset[c][cat]==0): # DROP EMPTY COMPONENTS OR THE ONES NOT SELECTED BY USER
            components_todrop.append(c)
            break
for c_todrop in components_todrop:
    dataset.pop(c_todrop)
    print(dataset)

# append score results #
print(f"Selecting only top candidates with score > {thresholds}, corresponding to fpr={thr} of the dataset.")
for c in components:
    for cat in categories:
        print(f"Processing {c} {cat}")
        #if dataset[c][cat]!=0:
        X_jet, X_fatjet, X_PFC, X_top, y   = dataset[c][cat]
        score                       = model({"jet": X_jet, "fatjet": X_fatjet, "PFC": X_PFC, "top": X_top})
        print(score)
        score                       = score.numpy().flatten()
        print(score)
        mask                        = score > thresholds
        print(mask)
        dataset[c][cat]             = [X_jet[mask], X_fatjet[mask], X_PFC[mask], X_top[mask], y[mask]]

# save new dataset to outFile #
print(f"Saving new dataset to {outFile}")
with open(outFile, "wb") as fpkl:
    pkl.dump(dataset, fpkl)
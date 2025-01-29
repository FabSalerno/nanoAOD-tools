import pickle as pkl
import os
import tensorflow as tf
import numpy as np
import matplotlib.pyplot as plt
from sklearn.metrics import roc_curve, auc
import re
path_to_graphics_folder = "/eos/user/f/fsalerno/framework/MachineLearning/"
with open("/eos/user/f/fsalerno/framework/MachineLearning/Training_PF_2022_1_jets_20_boosted/trainingSet.pkl", "rb") as fpkl: #b sta per binary e serve
#with open("/eos/user/f/fsalerno/framework/MachineLearning/Training_HOTVR_NEW_2018_1_final/trainingSet.pkl", "rb") as fpkl: #b sta per binary e serve
    dataset = pkl.load(fpkl)

components=dataset.keys()
categories=dataset["TT_semilep_2022"].keys()
#categories=dataset["QCD_HT1200to1500_2022"].keys()


def plot_roc(ax, y_true, y_pred, model_name):

    fpr, tpr, _ = roc_curve(y_true, y_pred)
    roc_auc = auc(fpr, tpr)
    
    ax.plot(fpr, tpr, label=f"{model_name} (AUC = {roc_auc:.2f})")

    ax.set_xlabel("False Positive [%]", fontsize=14)
    ax.set_ylabel("True Positive [%]", fontsize=14)
    ax.legend(loc="upper left", fontsize=12)
    ax.grid(alpha=0.3)


X_jet                     = np.concatenate([dataset[c][cat][0] for c in components for cat in categories]) # here we use only the components selected by the user
X_fatjet                  = np.concatenate([dataset[c][cat][1] for c in components for cat in categories]) # here we use only the components selected by the user
X_PFC                     = np.concatenate([dataset[c][cat][2] for c in components for cat in categories]) # here we use only the components selected by the user
X_top                     = np.concatenate([dataset[c][cat][3] for c in components for cat in categories]) # here we use only the components selected by the user
y                         = np.concatenate([dataset[c][cat][4] for c in components for cat in categories]) # here we use only the components selected by the user
data                      = X_jet, X_fatjet, X_PFC, X_top, y


path_to_model_folder    = "/eos/user/f/fsalerno/framework/MachineLearning/models/"
mods                    = ["CNN","CNN_2D","CNN_2D_conc","transformer","LSTM","LSTM_DNN","CNN_2D_LSTM","TROTA"]
cuts_train                    = ["","_0_pt"]#"_200_pt","_300_pt"]
#cuts_train                    = ["_200_pt"]
#cuts_train                    = ["_300_pt"]
n_PFCs                  = 20
models                  = {}
preds                   = {}
keys=[]
for mod in mods:
    for cut in cuts_train:
        key=f"{n_PFCs}_{mod}{cut}"
        if os.path.isfile(f"{path_to_model_folder}/model_{key}.h5") and key!="20_CNN_2D_LSTM":
            keys.append(key)
for key in keys:
    if os.path.isfile(f"{path_to_model_folder}/model_{key}.h5") and key!="20_CNN_2D_LSTM":
        models[key]         = tf.keras.models.load_model(f"{path_to_model_folder}/model_{key}.h5")

fig, ax = plt.subplots(figsize=(10, 7))
for key in keys:
        print(key)
        preds[key]  = models[key].predict({"fatjet":X_fatjet, "jet": X_jet, "PFC":X_PFC, "top": X_top}).flatten().tolist()
        label_0 = re.sub(r"20_","", f"{key}")
        label = re.sub(r"_0_pt","", label_0)
        plot_roc(ax=ax,y_true=y,y_pred=preds[key],model_name=label)

    # Set the title and show the plot
ax.set_title("Comparison of ROC Curves for Models", fontsize=16)
plt.xscale("log")
plt.xlim(1e-5, 1)
plt.tight_layout()
plt.savefig(f"{path_to_graphics_folder}/multi_roc_curve_0_pt.png")
plt.savefig(f"{path_to_graphics_folder}/multi_roc_curve_0_pt.pdf")
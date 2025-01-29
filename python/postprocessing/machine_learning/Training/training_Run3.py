##### FIX SEED #####
seed_value= 0
import os
os.environ['PYTHONHASHSEED']=str(seed_value)
import random
random.seed(seed_value)
import numpy as np
np.random.seed(seed_value)
import keras
import tensorflow as tf
tf.random.set_seed(12345)
session_conf = tf.compat.v1.ConfigProto(intra_op_parallelism_threads=1, inter_op_parallelism_threads=1)
sess = tf.compat.v1.Session(graph=tf.compat.v1.get_default_graph(), config=session_conf)
from keras import backend as K
K.set_session(sess)


import os
import sys
from curses import keyname
#import tensorflow as tf
#from tensorflow import keras
#import keras_tuner as kt
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
from sklearn.utils import class_weight
import argparse


ROOT.gROOT.SetBatch()
ROOT.gStyle.SetOptStat(0)


############################################
########### STARTING THE SCRIPT ############
############################################

########### INPUT ############
usage       = 'python3 training_Run3.py -s component1,component2,component3 -i /path/to/pkl'
example     = 'python3 training_Run3.py -s QCD_HT1000to1500_2018,QCD_HT1500to2000_2018,QCD_HT2000toInf_2018,QCD_HT700to1000_2018,TT_Mtt_1000toInf_2018,TT_Mtt_700to1000_2018,TprimeBToTZ_M1200_2018,TprimeBToTZ_M1800_2018,TprimeBToTZ_M800_2018,ZJetsToNuNu_HT1200To2500_2018,ZJetsToNuNu_HT200To400_2018,ZJetsToNuNu_HT2500ToInf_2018,ZJetsToNuNu_HT400To600_2018,ZJetsToNuNu_HT800To1200_2018,tDM_Mphi1000_2018,tDM_Mphi500_2018,tDM_Mphi50_2018 -i /eos/user/f/fsalerno/framework/MachineLearning/Training_2018_2/trainingSet.pkl -m /eos/user/f/fsalerno/framework/MachineLearning/Training_2018_2/model.h5 -j /eos/user/f/fsalerno/framework/MachineLearning/Training_2018_2/score_thresholds.json -g /eos/user/f/fsalerno/framework/MachineLearning/Training_2018_2/graphics'
parser      = argparse.ArgumentParser(usage)
parser.add_argument('-s', '--samples',    dest = 'samples',   required = True,                                              type = str,      help = 'samples to use for the training, given as string (e.g. "component1,component2,component3")')
parser.add_argument('-i', '--inFile',     dest = 'inFile',    required = True,                                              type = str,      help = 'complete path to the input folder containing the pkls')
parser.add_argument('-m', '--outModel',   dest = 'outModel',  required = False,   default = './model.h5',                   type = str,      help = 'complete path to save the model (default "./model.h5")')
parser.add_argument('-j', '--outJson',    dest = 'outJson',   required = False,   default = './score_thresholds.json',      type = str,      help = 'complete path to save the score thresholds (default "./score_thresholds.json")')
parser.add_argument('-g', '--graphics',   dest = 'graphics',  required = False,   default = './graphics',                   type = str,      help = 'complete path to save the graphics (default "./graphics")')

args                    = parser.parse_args()
samples                 = args.samples.split(",")
inFile                  = args.inFile
outModel                = args.outModel
path_to_outJson         = args.outJson
path_to_graphics_folder = args.graphics
verbose                 = True
path_to_best_hps        = "/afs/cern.ch/user/f/fsalerno/CMSSW_12_5_2/src/PhysicsTools/NanoAODTools/python/postprocessing/machine_learning/hps_model/best_hps.json"

if not os.path.exists(path_to_graphics_folder):
    os.makedirs(path_to_graphics_folder)
    print(f"Directory {path_to_graphics_folder} created")
####### DATASET LOADING AND PREPROCESSING #######
with open(inFile, "rb") as fpkl:
    dataset = pkl.load(fpkl)
components  = dataset.keys()
categories  = ["3j1fj", "3j0fj", "2j1fj"]

### Remove Empty Components ###
components_todrop = []
for c in components:
    for cat in categories:
        if (dataset[c][cat]==0) or (c not in samples): # DROP EMPTY COMPONENTS OR THE ONES NOT SELECTED BY USER
            components_todrop.append(c)
            break
for c_todrop in components_todrop:
    dataset.pop(c_todrop)
    print(dataset)



### DATASET BALANCING (remove some False Tops) ###
for c in components:
    for cat in categories:
        idx_truetop  = [i for i, x in enumerate(dataset[c][cat][3]==1) if x==True]
        idx_falsetop = [i for i, x in enumerate(dataset[c][cat][3]==0) if x==True]
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



########VINCOLO Pt####################

for c in components:
    for cat in categories:
        ids_todrop_pt=[]
        for i in range(len(dataset[c][cat][2])):
            ids_todrop_pt
            pt_top  = dataset[c][cat][2][i][2]
            if pt_top<=300:
                ids_todrop_pt.append(i)

        dataset[c][cat][0] = np.delete(dataset[c][cat][0], ids_todrop_pt, axis=0)
        dataset[c][cat][1] = np.delete(dataset[c][cat][1], ids_todrop_pt, axis=0)
        dataset[c][cat][2] = np.delete(dataset[c][cat][2], ids_todrop_pt, axis=0)
        dataset[c][cat][3] = np.delete(dataset[c][cat][3], ids_todrop_pt, axis=0)



####### SOME USEFUL PRINTS ABOUT DIMENSIONALITIES #######

# Printing dataset numbers #
if verbose:
    for c in components:
        for cat in categories:
            print(f"Component: {c}, Category: {cat}")
            print(f"Number of True Tops:    {len([i for i, x in enumerate(dataset[c][cat][3]==1) if x==True])}")
            print(f"Number of False Tops:   {len([i for i, x in enumerate(dataset[c][cat][3]==0) if x==True])}")
            print(f"Number of Jets:         {len(dataset[c][cat][0])}")
            print(f"Number of FatJets:      {len(dataset[c][cat][1])}")
            print(f"Number of Tops:         {len(dataset[c][cat][2])}")
            print("\n")

    print(f"N. Top:                 {sum([len(dataset[c][cat][0]) for c in components for cat in categories])}")
    print(f"N. Top True:            {sum([len([i for i, x in enumerate(dataset[c][cat][3]==1) if x==True]) for c in components for cat in categories])}")
    print(f"N. Top False:           {sum([len([i for i, x in enumerate(dataset[c][cat][3]==0) if x==True]) for c in components for cat in categories])}")
    print("\n")

    print(f"N. Top in category 3-0: {sum([len(dataset[c]['3j0fj'][0]) for c in components])}")
    print(f"N. Top True:            {sum([len([i for i, x in enumerate(dataset[c]['3j0fj'][3]==1) if x==True]) for c in components])}")
    print(f"N. Top False:           {sum([len([i for i, x in enumerate(dataset[c]['3j0fj'][3]==0) if x==True]) for c in components])}")
    print("\n")

    print(f"N. Top in category 3-1: {sum([len(dataset[c]['3j1fj'][0]) for c in components])}")
    print(f"N. Top True:            {sum([len([i for i, x in enumerate(dataset[c]['3j1fj'][3]==1) if x==True]) for c in components])}")
    print(f"N. Top False:           {sum([len([i for i, x in enumerate(dataset[c]['3j1fj'][3]==0) if x==True]) for c in components])}")
    print("\n")

    print(f"N. Top in category 2-1: {sum([len(dataset[c]['2j1fj'][0]) for c in components])}")
    print(f"N. Top True:            {sum([len([i for i, x in enumerate(dataset[c]['2j1fj'][3]==1) if x==True]) for c in components])}")
    print(f"N. Top False:           {sum([len([i for i, x in enumerate(dataset[c]['2j1fj'][3]==0) if x==True]) for c in components])}")
    print("\n")


class trainer:
    def __init__(self, X_jet, X_fatjet, X_top, y, BestHyperParameters):
        self.X_jet               = X_jet   
        self.X_fatjet            = X_fatjet
        self.X_top               = X_top   
        self.y                   = y
        self.BestHyperParameters = BestHyperParameters
    
    
    def split(self, test_size):
        self.X_jet_train, self.X_jet_test, self.X_fatjet_train, self.X_fatjet_test, self.X_top_train, self.X_top_test, self.y_train, self.y_test = train_test_split(self.X_jet, self.X_fatjet, self.X_top, self.y, 
                                                                                                                                                                    # test_size=test_size)
                                                                                                                                                                    stratify=self.y, shuffle=True, test_size=test_size)
    
    
    def model_builder(self, InputShape_Jet, InputShape_FatJet, InputShape_Top):
        # Input Layers
        fj_inputs   = tf.keras.Input(shape=(InputShape_FatJet,),   name="fatjet")    #x
        jet_inputs  = tf.keras.Input(shape=(None,InputShape_Jet,), name="jet")       #y
        top_inputs  = tf.keras.Input(shape=(InputShape_Top,),      name="top")       #z
        ### Operations on FATJET Input Layer ###
        # x           = Masking(mask_value=0.)(fj_inputs)
        # x           = BatchNormalization()(x)
        x           = BatchNormalization()(fj_inputs)
        # Tune parameters for FatJet Input Layer #
        x           = Dense(units=self.BestHyperParameters["fj_units"],
                            activation=self.BestHyperParameters["fj_activation"],
                            kernel_initializer=self.BestHyperParameters["fj_kernel_initializer"]
                            )(x)
        ### Operations on JET Input Layer ###
        y = Masking(mask_value=0.)(jet_inputs)
        y = BatchNormalization()(y)
        # Tune parameters for Jet Input Layer #
        y = keras.layers.LSTM(units=self.BestHyperParameters["j_units"],
                              activation=self.BestHyperParameters["j_activation"],
                              kernel_initializer=self.BestHyperParameters["j_kernel_initializer"],
                              dropout=self.BestHyperParameters["j_dropout"]
                             )(y)

        ### Operations on TOP Input Layer ###
        z = Dense(1, activation="relu")(top_inputs)
        ### Operations on JET+FATJET Input Layer ###
        x = concatenate([x,y])
        x = concatenate([x,z])
        x = Dense(5, activation ="relu", kernel_initializer="random_normal")(x)
    

        outputs      = Dense(1, activation="sigmoid")(x) 
        self.model   = tf.keras.Model(inputs=[fj_inputs, jet_inputs, top_inputs], outputs=outputs)
        
        ### Define trainer and compile model ###
        # trainer = tf.keras.optimizers.Adam(learning_rate=0.05)
        trainer = tf.keras.optimizers.Nadam(learning_rate=0.001)
        loss    = tf.keras.losses.BinaryCrossentropy()
        self.model.compile(optimizer=trainer, loss=loss, metrics=[tf.keras.metrics.AUC()])   
        
        
    def callbacks(self):
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
                                                      min_delta=1e-5,
                                                      factor=0.1, # factor by which LR has to be reduced...
                                                      patience=10, #...after waiting this number of epochs with no improvements on monitored quantity
                                                      min_lr=1e-15) 
        self.callback_list=[early_stop, reduce_LR]

    
    def training(self, validation_split, epochs=50, batch_size=1, verbose=True, save_model=False, path_to_model=None):
        self.callbacks()
        self.model_builder(self.X_jet_train.shape[2], self.X_fatjet_train.shape[1], self.X_top_train.shape[1])
        # Dataset Balancing #
        weights       = class_weight.compute_class_weight(class_weight="balanced", classes=np.unique(self.y_train), y=np.concatenate(self.y_train))
        class_weights = {0: weights[0], 1: weights[1]}
        self.history  = self.model.fit({"fatjet": self.X_fatjet_train, "jet": self.X_jet_train, "top": self.X_top_train}, self.y_train,
                                       callbacks=self.callback_list, validation_split=validation_split, epochs=epochs, batch_size=batch_size, verbose=verbose,
                                       class_weight=class_weights)
        if save_model:
            self.model.save(f"{path_to_model}")
        
    def load_model(self, model_to_load):
        self.model = tf.keras.models.load_model(model_to_load)

    def evaluate(self, X_jet_test=None, X_fatjet_test=None, X_top_test=None, y_test=None):
        if (X_jet_test is None) and (X_fatjet_test is None) and (X_top_test is None) and (y_test is None):
            self.eval_result = self.model.evaluate({"fatjet": self.X_fatjet_test, "jet": self.X_jet_test, "top": self.X_top_test}, self.y_test)
            return self.eval_result
        else:
            eval_result      = self.model.evaluate({"fatjet": X_fatjet_test, "jet": X_jet_test, "top": X_top_test}, y_test)
            return eval_result
    

    def predict(self, X_jet_train=None, X_fatjet_train=None, X_top_train=None, X_jet_test=None, X_fatjet_test=None, X_top_test=None):
        if (X_jet_train is None) and (X_fatjet_train is None) and (X_top_train is None) and (X_jet_test is None) and (X_fatjet_test is None) and (X_top_test is None):
            self.y_pred_train = self.model.predict({"fatjet": self.X_fatjet_train, "jet": self.X_jet_train, "top": self.X_top_train})
            self.y_pred_test  = self.model.predict({"fatjet": self.X_fatjet_test, "jet": self.X_jet_test, "top": self.X_top_test})
        else:
            y_pred_train      = self.model.predict({"fatjet": X_fatjet_train, "jet": X_jet_train, "top": X_top_train})
            y_pred_test       = self.model.predict({"fatjet": X_fatjet_test, "jet": X_jet_test, "top": X_top_test})
            return y_pred_train, y_pred_test
    
    
    def train_test_discrimination(self, bins):
        self.predict()

        y_pred_train_bkg = self.y_pred_train[self.y_train==0]
        y_pred_train_sgn = self.y_pred_train[self.y_train==1]
        y_pred_test_bkg  = self.y_pred_test[self.y_test==0]
        y_pred_test_sgn  = self.y_pred_test[self.y_test==1]

        train_test_pred  = {}
        train_test_pred["train_bkg"] = y_pred_train_bkg
        train_test_pred["train_sgn"] = y_pred_train_sgn
        train_test_pred["test_bkg"]  = y_pred_test_bkg  
        train_test_pred["test_sgn"]  = y_pred_test_sgn

        # Histograms to be drawn #
        train_test_histos = {}   
        ROOT.gStyle.SetOptStat(0)
        c = ROOT.TCanvas("c", "c", 600, 600)
        c.SetLogy()
        c.Draw()
        # leg = ROOT.TLegend(0.75, 0.6, 0.9, 0.9)
        leg = ROOT.TLegend(0.3, 0.6, 0.5, 0.9)

        train_test_histos["train_bkg"] = ROOT.TH1F("histo_train_bkg", "histo_train_bkg", bins, 0, 1)
        train_test_histos["train_sgn"] = ROOT.TH1F("histo_train_sgn", "histo_train_sgn", bins, 0, 1)
        train_test_histos["test_bkg"]  = ROOT.TH1F("histo_test_bkg",  "histo_test_bkg",  bins, 0, 1)
        train_test_histos["test_sgn"]  = ROOT.TH1F("histo_test_sgn",  "histo_test_sgn",  bins, 0, 1)


        for k in train_test_pred.keys():
            for x in train_test_pred[k]:
                train_test_histos[k].Fill(x)
            train_test_histos[k].Scale(1./train_test_histos[k].Integral())
            train_test_histos[k].SetTitle("")
            train_test_histos[k].GetXaxis().SetTitle("Score")
            train_test_histos[k].SetMaximum(1)
            train_test_histos[k].GetYaxis().SetTitle("Normalized Counts")

            if "test" in k:
                train_test_histos[k].SetMarkerStyle(ROOT.kFullCircle)
                # Add to TLegend
                leg.AddEntry(train_test_histos[k], k, "p")
            elif "train" in k:
                # Add to TLegend
                leg.AddEntry(train_test_histos[k], k, "f")
            
        train_test_histos["train_bkg"].SetFillColorAlpha(ROOT.kBlue, 0.3)
        train_test_histos["train_bkg"].SetLineColorAlpha(ROOT.kBlue, 0.3)
        train_test_histos["train_sgn"].SetFillColorAlpha(ROOT.kRed,  0.3)
        train_test_histos["train_sgn"].SetLineColorAlpha(ROOT.kRed,  0.3)

        train_test_histos["test_bkg"].SetMarkerColor(ROOT.kBlue)
        train_test_histos["test_sgn"].SetMarkerColor(ROOT.kRed)


        train_test_histos["train_bkg"].Draw("HIST")
        train_test_histos["train_sgn"].Draw("HISTSAME")
        train_test_histos["test_bkg"].Draw("SAME")
        train_test_histos["test_sgn"].Draw("SAME")
        leg.Draw("SAME")

        c.SaveAs(f"{path_to_graphics_folder}/traintestDiscrimination.png")
        c.SaveAs(f"{path_to_graphics_folder}/traintestDiscrimination.pdf")

        
    # def plot_roc(self, name, labels, predictions, **kwargs):
    def plot_roc(self, name, labels, predictions, color="steelblue", linestyle="--"):
        fpr, tpr, trs = roc_curve(labels, predictions)
        # plt.plot(100*fpr, 100*tpr, label=name, linewidth=2, color="steelblue", linestyle=linestyle)
        plt.plot(fpr, tpr, label=name, linewidth=2, color="steelblue", linestyle=linestyle)
        plt.xlabel("False positives [%]")
        plt.ylabel("True positives [%]")
        # plt.xlim(xlim)
        # plt.ylim(ylim)
        plt.grid(True)
        # ax = plt.gca()
        # ax.set_aspect("equal")

        plt.xscale("log")
        plt.legend(loc="lower right")
        plt.savefig(f"{path_to_graphics_folder}/roc_curve.png")
        plt.savefig(f"{path_to_graphics_folder}/roc_curve.pdf")
        return fpr, tpr, trs


    def train_test_roc(self):
        # fpr_train, tpr_train, trs_train = self.plot_roc("Train Baseline", np.concatenate(self.y_train), self.y_pred_train, color="steelblue")
        fpr, tpr, trs = self.plot_roc("Test Baseline", np.concatenate(self.y_test), self.y_pred_test, color="steelblue", linestyle="--")

        return fpr, tpr, trs




##################################
##################################
############ TRAINING ############
##################################
##################################

print("ATTNZION PROVA COMPONENTI", samples)
X_jet                     = np.concatenate([dataset[c][cat][0] for c in samples for cat in categories]) # here we use only the samples selected by the user
X_fatjet                  = np.concatenate([dataset[c][cat][1] for c in samples for cat in categories]) # here we use only the samples selected by the user
X_top                     = np.concatenate([dataset[c][cat][2] for c in samples for cat in categories]) # here we use only the samples selected by the user
y                         = np.concatenate([dataset[c][cat][3] for c in samples for cat in categories]) # here we use only the samples selected by the user
data                      = X_jet, X_fatjet, X_top, y

if verbose:
    print("Data loaded for the training:")
    print(f"\tsamples used:           {samples}")
    print(f"\tNumber of tops:         {len(y)}")
    print(f"\tNumber of true tops:    {len([i for i, x in enumerate(y==1) if x==True])}")
    print(f"\tNumber of false tops:   {len([i for i, x in enumerate(y==0) if x==True])}")

    print(f"\tX_jet shape:            {X_jet.shape}")
    print(f"\tX_fatjet shape:         {X_fatjet.shape}")
    print(f"\tX_top shape:            {X_top.shape}")


### LOADING BEST HYPERPARAMETERS ###
with open(path_to_best_hps) as f:
    best_hps              = json.load(f)
trainer1                  = trainer(*data, best_hps)
trainer1.split(0.3)

# training parameters #
epochs, batch_size        = 1000, 250
trainer1.training(validation_split=0.3, epochs=epochs, batch_size=batch_size, 
                      save_model=True, path_to_model=outModel, verbose=True)

# trainer1.load_model(model_to_load="/afs/cern.ch/user/l/lfavilla/CMSSW_12_6_0/src/PhysicsTools/NanoAODTools/python/postprocessing/analysis/MLstudies/Training_2018_1/Train/saved_models/model_base2.h5")
# trainer1.load_model(model_to_load="/afs/cern.ch/user/l/lfavilla/CMSSW_12_6_0/src/PhysicsTools/NanoAODTools/python/postprocessing/analysis/MLstudies/Training_2018_1/Train/saved_models/model_base.h5")

eval_result     = trainer1.evaluate()
trainer1.train_test_discrimination(bins=100)
fpr, tpr, trs   = trainer1.train_test_roc()

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
metric  = "auc"
history = trainer1.history
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
print("done")
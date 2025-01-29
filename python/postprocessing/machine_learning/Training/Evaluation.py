#!/usr/bin/env python3
##### FIX SEED #####
seed_value= 0
import os
from pyexpat import model
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



# import tensorflow as tf
import pickle as pkl
# import numpy as np
import ROOT
# import os
import pandas as pd

ROOT.gROOT.SetBatch()
ROOT.gStyle.SetOptStat(0)
# Datasets
# from PhysicsTools.NanoAODTools.postprocessing.my_analysis.my_framework.MLstudies.Training.Datasets import *
import PhysicsTools.NanoAODTools.postprocessing.machine_learning.Training.Datasets as Datasets


datasets                = Datasets.datasets
######### Create arguments to insert from shell #########
from argparse import ArgumentParser
parser                  = ArgumentParser()
parser.add_argument("-key",                     dest="key",                     default=None,   required=True,    type=str,      help="key of Datasets.datasets for the train")
parser.add_argument("-eval_keys",               dest="eval_keys",               default=None,   required=True,    type=str,      help="keys of Datasets.datasets for the evaluation")
parser.add_argument("-path_to_eval_folder",     dest="path_to_eval_folder",     default=None,   required=True,    type=str,      help="path to folder to save plots")
parser.add_argument("-path_to_model_folder",    dest="path_to_model_folder",    default=None,   required=True,    type=str,      help="path to folder where model is saved")
parser.add_argument("-path_to_graphics_folder", dest="path_to_graphics_folder", default=None,   required=True,    type=str,      help="path to folder where to save plots")


options                 = parser.parse_args()
key                     = options.key
eval_keys               = ((options.eval_keys).replace(" ", "")).split(",")                  
path_to_eval_folder     = options.path_to_eval_folder
path_to_model_folder    = options.path_to_model_folder
path_to_graphics_folder = options.path_to_graphics_folder


model                   = tf.keras.models.load_model(f"{path_to_model_folder}/model.h5")
#model                   = tf.keras.models.load_model(f"{path_to_model_folder}/model_{key}.h5")
if not os.path.exists(path_to_graphics_folder):
    os.mkdir(path_to_graphics_folder)


######### CREATE ROOT FILE TO STORE HISTOGRAMS #########
PlotsRFilePath  = f"{path_to_graphics_folder}/{key}.root"
PlotsRFile      = ROOT.TFile(PlotsRFilePath, "RECREATE")




eval_datasets               = {}
for eval_key in eval_keys:
    InputData               = {"jet": datasets[eval_key][0], "fatjet": datasets[eval_key][1], "hotvrjet": datasets[eval_key][2], "top": datasets[eval_key][3]}
    InputLabel              = datasets[eval_key][4]
    eval_datasets[eval_key] = InputData, InputLabel





predictions = {}
for eval_dataset in eval_datasets:
    predictions[eval_dataset] = {}
    print(f"PREDICTING:\tTRAIN: {key}\tEVALUATION: {eval_dataset}")
    y_pred     = model.predict(eval_datasets[eval_dataset][0])
    y_pred_bkg = y_pred[eval_datasets[eval_dataset][1]==0]
    y_pred_sig = y_pred[eval_datasets[eval_dataset][1]==1]
    # save to dictionary 
    predictions[eval_dataset]["bkg"] = y_pred_bkg
    predictions[eval_dataset]["sig"] = y_pred_sig



# for model_type in keys:
#     path_to_graphics_folder = f"/eos/user/l/lfavilla/my_framework/MLstudies/Training/plots/{model_type}"
#     if not os.path.exists(path_to_graphics_folder):
#         os.mkdir(path_to_graphics_folder)
#     for eval_dataset in eval_datasets: 
#         c      = ROOT.TCanvas("c", "c", 800, 600)
#         c.SetLogy()
#         c.Draw()

#         bins   = 50
#         histo1 = ROOT.TH1F("h1", f"Score - Train: {model_type} - Predict: {eval_dataset}", bins, 0, 1)
#         for x in predictions[model_type][eval_dataset]["sig"]:
#             histo1.Fill(x)
#         histo1.Scale(1./histo1.Integral())
#         histo1.SetLineColor(ROOT.kRed)
#         histo1.SetMaximum(1)
#         histo1.SetMinimum(1e-4)
#         histo1.Draw("HIST")

#         histo2 = ROOT.TH1F("h2", "h", bins, 0, 1)
#         for x in predictions[model_type][eval_dataset]["bkg"]:
#             histo2.Fill(x)
#         histo2.Scale(1./histo2.Integral())
#         histo2.SetMaximum(1)
#         histo2.SetMinimum(1e-4)
#         histo2.Draw("HISTSAME")
        
#         c.SaveAs(f"{path_to_graphics_folder}/Score_Train_{model_type}_Predict_{eval_dataset}.png")
#         c.SaveAs(f"{path_to_graphics_folder}/Score_Train_{model_type}_Predict_{eval_dataset}.pdf")


for eval_dataset in eval_datasets: 
    c      = ROOT.TCanvas("c", "c", 800, 600)
    c.SetLogy()
    c.Draw()

    bins   = 50
    histo1 = ROOT.TH1F(f"Score_Train_{key}_Predict_{eval_dataset}_True", f"Score - Train: {key} - Predict: {eval_dataset} - True", bins, 0, 1)
    for x in predictions[eval_dataset]["sig"]:
        histo1.Fill(x)
    histo1.Scale(1./histo1.Integral())
    histo1.GetXaxis().SetTitle("Score")
    histo1.GetYaxis().SetTitle("Norm. Counts")
    histo1.SetLineColor(ROOT.kRed)
    histo1.SetMaximum(1)
    histo1.SetMinimum(1e-4)
    histo1.SetOption("HIST")
    histo1.Write()
    histo1.SetTitle(f"Score - Train: {key} - Predict: {eval_dataset} - True")
    histo1.Draw()

    histo2 = ROOT.TH1F(f"Score_Train_{key}_Predict_{eval_dataset}_False", f"Score - Train: {key} - Predict: {eval_dataset} - False", bins, 0, 1)
    for x in predictions[eval_dataset]["bkg"]:
        histo2.Fill(x)
    histo2.Scale(1./histo2.Integral())
    histo2.GetXaxis().SetTitle("Score")
    histo2.GetYaxis().SetTitle("Norm. Counts")
    histo2.SetMaximum(1)
    histo2.SetMinimum(1e-4)
    histo2.SetOption("HIST")
    histo2.Write()
    histo2.Draw("HISTSAME")
    
    #### DRAW CANVAS ####
    c.SaveAs(f"{path_to_graphics_folder}/Score_Train_{key}_Predict_{eval_dataset}.png")
    c.SaveAs(f"{path_to_graphics_folder}/Score_Train_{key}_Predict_{eval_dataset}.pdf")





PlotsRFile.Close()
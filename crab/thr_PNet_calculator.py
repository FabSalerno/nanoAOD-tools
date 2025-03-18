#!/usr/bin/env python
import os
import sys
import ROOT
ROOT.PyConfig.IgnoreCommandLineOptions = True
import matplotlib.pyplot as plt


h_score_top_merged_false_tot = ROOT.TH1F("score_top_merged_false_tot", "score_top_merged_false_tot", 100, 0, 1)
h_score_top_merged_false_res_tot = ROOT.TH1F("score_top_merged_false_res_tot", "score_top_merged_false_res_tot", 1000, 0, 1)
h_tops_counter_tot = ROOT.TH1F('ntops_tot', 'ntops_tot', 3, 0, 3)

dirpath = "/afs/cern.ch/user/f/fsalerno/CMSSW_13_2_11/src/PhysicsTools/NanoAODTools/python/postprocessing/modules/common"
path_to_graphic_folder = "/eos/user/f/fsalerno/"

components = ["100_200","200_400","400_600","600_800","800_1000","1000_1200","1200_1500","1500_2000","2000_inf"]
#components = ["1000_1200","1200_1500","1500_2000","2000_inf"]
file_paths = []
file_dict={}

for c in components:
    inFile = f"{dirpath}/fpr_PNet_{c}.root"
    if not inFile.startswith('.'):
        file_dict[c]=ROOT.TFile.Open(inFile)
        #print(file_dict[c].ls())


# Initialize all histogram dictionaries before the loop starts
h_score_top_merged_false_res = {}
h_score_top_merged_false = {}

# N tops
h_tops_counter = {}


for c in components:

    # Scores
    h_score_top_merged_false_res[c] = file_dict[c].Get(f"plots_{c}/score_res")
    h_score_top_merged_false_res_tot.Add(h_score_top_merged_false_res[c])

    h_score_top_merged_false[c] = file_dict[c].Get(f"plots_{c}/score")
    h_score_top_merged_false_tot.Add(h_score_top_merged_false[c])

    # N tops
    h_tops_counter[c] = file_dict[c].Get(f"plots_{c}/ntop")
    h_tops_counter_tot.Add(h_tops_counter[c])

outFile = ROOT.TFile("/eos/user/f/fsalerno/FPR_PNet.root", "RECREATE")    
h_score_top_merged_false_tot.Write()
outFile.Close()

outFile_res = ROOT.TFile("/eos/user/f/fsalerno/FPR_PNet_res.root", "RECREATE")    
h_score_top_merged_false_res_tot.Write()
outFile_res.Close()
#CICLO FOR PER LA ROC

FPR_merged = []
FPR_merged_res = []
score_merged = []
score_merged_res = []

print("integral",h_score_top_merged_false_tot.Integral(-1,101),"getentries",h_score_top_merged_false_tot.GetEntries(),"ntops",h_tops_counter_tot.GetEntries())
#faccio il for al contrario così inizio da score alti e TPR e FPR bassi
for bin in range (101,-1,-1):
    #se lo score tresh è 0 il TPR è 1
    FPR=0
    if h_score_top_merged_false_tot.Integral(-1,101) !=0:
        FPR = h_score_top_merged_false_tot.Integral(bin,101)/h_score_top_merged_false_tot.GetEntries()
        #print("FPR",FPR)

    else:
        FPR = 0
    score = h_score_top_merged_false_tot.GetBinCenter(bin)

    FPR_merged.append(FPR)
  
    score_merged.append(score)
    
    

for i, fpr in enumerate(FPR_merged):
    if fpr>=0.01:
        print("FPR:",fpr,"\n", "Thr:",score_merged[i])
        break


#faccio il for al contrario così inizio da score alti e TPR e FPR bassi
for bin in range (1001,-1,-1):
    #se lo score tresh è 0 il TPR è 1
    FPR_res=0
    if h_score_top_merged_false_res_tot.Integral(-1,1001) !=0:
        FPR_res = h_score_top_merged_false_res_tot.Integral(bin,1001)/h_score_top_merged_false_res_tot.GetEntries()
        #print("bin", bin, "FPR_res",FPR_res)

    else:
        FPR_res = 0
    score_res = h_score_top_merged_false_res_tot.GetBinCenter(bin)
    #print("bin", bin, "FPR_res",FPR_res,"score_res",score_res)

    FPR_merged_res.append(FPR_res)

    score_merged_res.append(score_res)
    
    

for i, fpr_r in enumerate(FPR_merged_res):
    if fpr_r>=0.01:
        print("FPR res:",fpr_r,"\n", "Thr res:",score_merged_res[i])
        break

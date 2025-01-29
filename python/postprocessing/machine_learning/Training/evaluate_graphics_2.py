import ROOT 
import numpy as np
import argparse
from curses import keyname
import json
import os
import sys

usage       = 'python3 training_Run3.py -s component  -i /path/to/inputfile'
example     = 'python3 training_Run3.py -s TT_Mtt-1000toInf -i /eos/user/f/fsalerno/Data/evaluate/TT_Mtt-1000toInf_Skim_evaluate.root -g /eos/user/f/fsalerno/framework/MachineLearning/Training_2018_2/graphics_evaluate'
parser      = argparse.ArgumentParser(usage)
parser.add_argument('-s', '--component',    dest = 'component',   required = True,                                              type = str,      help = 'samples to use for the training, given as string (e.g. "component1,component2,component3")')
parser.add_argument('-i', '--inFile',     dest = 'inFile',    required = True,                                              type = str,      help = 'complete path to the input folder containing the pkls')
parser.add_argument('-g', '--graphics',   dest = 'graphics',  required = False,   default = './graphics',                   type = str,      help = 'complete path to save the graphics (default "./graphics")')

args                    = parser.parse_args()
component                 = args.component
inFile                  = args.inFile
path_to_graphics_folder = args.graphics
verbose                 = True

if not os.path.exists(path_to_graphics_folder):
    os.makedirs(path_to_graphics_folder)
    print(f"Directory {path_to_graphics_folder} created")


file_to_read = ROOT.TFile(inFile,"OPEN")
my_tree = file_to_read.Friends

#Istogrammi
h_n_mixed = ROOT.TH1F("nTopMixed_histo","n_mixed",100,0,1020)
h_n_resolved = ROOT.TH1F("nTopResolved", "n_resolved",50,0,300)
h_n_mixed_true = ROOT.TH1F("nTopMixed_histo_true","n_mixed_true",10,0,20)
h_n_resolved_true = ROOT.TH1F("nTopResolved_true", "n_resolved_true",10,0,10)
h_n_mixed_false_qcd = ROOT.TH1F("nTopMixed_histo_false_qcd","n_mixed_false_qcd",100,0,1020)
h_n_mixed_false_other = ROOT.TH1F("nTopMixed_histo_false_other","n_mixed_false_other",100,0,1020)
h_n_mixed_false_all = ROOT.TH1F("nTopMixed_histo_false_all","n_mixed_false_all",100,0,1020)
h_n_resolved_false = ROOT.TH1F("nTopResolved_false", "n_resolved_false",50,0,300)
h_score_mixed_true = ROOT.TH1F("TopMixed_score_histo_true","score_mixed_true",100,0,1)
h_score_resolved_true = ROOT.TH1F("TopResolved_score_histo_true", "score_resolved_true",100,0,1)
h_score_mixed_false_qcd = ROOT.TH1F("TopMixed_score_histo_false_qcd","score_mixed_false_qcd",100,0,1)
h_score_mixed_false_other = ROOT.TH1F("TopMixed_score_histo_false_other","score_mixed_false_other",100,0,1)
h_score_mixed_false_all = ROOT.TH1F("TopMixed_score_histo_false_all","score_mixed_false_all",100,0,1)
h_score_resolved_false = ROOT.TH1F("TopResolved_score_histo_false", "score_resolved_false",100,0,1)
bins = 100

#Ciclo for per il fill
for i in range(my_tree.GetEntries()):
    my_tree.GetEntry(i)
    n_mixed_true = 0
    n_mixed_false_qcd = 0
    n_mixed_false_other = 0
    n_mixed_false_all = 0
    if my_tree.nTopMixed!=0:
        for j in range(0,my_tree.nTopMixed):
            if my_tree.TopMixed_truth[j]==1:
                n_mixed_true+=1
                h_score_mixed_true.Fill(my_tree.TopMixed_TopScore[j])
            if my_tree.TopMixed_truth[j]!=1:
                n_mixed_false_all+=1
                h_score_mixed_false_all.Fill(my_tree.TopMixed_TopScore[j])   
            if my_tree.TopMixed_truth[j]==0:
                n_mixed_false_qcd+=1
                h_score_mixed_false_qcd.Fill(my_tree.TopMixed_TopScore[j])
            if my_tree.TopMixed_truth[j]==-1:
                n_mixed_false_other+=1
                h_score_mixed_false_other.Fill(my_tree.TopMixed_TopScore[j])
        h_n_mixed_true.Fill(n_mixed_true)
        h_n_mixed_false_all.Fill(n_mixed_false_all)
        h_n_mixed_false_qcd.Fill(n_mixed_false_qcd)
        h_n_mixed_false_other.Fill(n_mixed_false_other)
        
    
    n_resolved_true = 0
    n_resolved_false = 0
    if my_tree.nTopResolved!=0:
        for j in range(0,my_tree.nTopResolved):
            if my_tree.TopResolved_truth[j]==1:
                h_score_resolved_true.Fill(my_tree.TopResolved_TopScore[j])
                n_resolved_true+=1
        h_n_resolved_true.Fill(n_resolved_true)
        #print("evento:",i,"n resolved true:", n_resolved_true)
                
        for j in range(0, my_tree.nTopResolved):
            if my_tree.TopResolved_truth[j]==0:
                h_score_resolved_false.Fill(my_tree.TopResolved_TopScore[j])
                n_resolved_false+=1
        h_n_resolved_false.Fill(n_resolved_false)
        #print("evento:",i,"n resolved false:", n_resolved_false)
        #print(i,my_tree.GetEntries())
    if i%100==0:
        print("Il ciclo è al ", (i/my_tree.GetEntries())*100,"%")
print("fine")

# Histograms to be drawn #
ROOT.gStyle.SetOptStat(0)
c = ROOT.TCanvas("c", "c", 600, 600)
c.SetLogy()

leg = ROOT.TLegend(0.3, 0.6, 0.7, 0.9)

if h_score_mixed_false_other.Integral() !=0:  
    h_score_mixed_false_other.Scale(1./h_score_mixed_false_other.Integral())
h_score_mixed_false_other.SetTitle("")
h_score_mixed_false_other.GetXaxis().SetTitle("Score")
h_score_mixed_false_other.SetMaximum(1)
h_score_mixed_false_other.GetYaxis().SetTitle("Normalized Counts")
h_score_mixed_false_other.SetFillColorAlpha(ROOT.kGreen, 0.6)
h_score_mixed_false_other.Draw("histsameerror")
c.SetTitle("prova")

if h_score_mixed_true.Integral() !=0:
    h_score_mixed_true.Scale(1./h_score_mixed_true.Integral())
h_score_mixed_true.SetTitle("Discrimination")
h_score_mixed_true.GetXaxis().SetTitle("Score")
h_score_mixed_true.SetMaximum(1)
h_score_mixed_true.GetYaxis().SetTitle("Normalized Counts")
h_score_mixed_true.SetFillColorAlpha(ROOT.kRed, 0.6)
h_score_mixed_true.Draw("histsameerror")

if h_score_mixed_false_qcd.Integral() !=0:  
    h_score_mixed_false_qcd.Scale(1./h_score_mixed_false_qcd.Integral())
h_score_mixed_false_qcd.SetTitle("")
h_score_mixed_false_qcd.GetXaxis().SetTitle("Score")
h_score_mixed_false_qcd.SetMaximum(1)
h_score_mixed_false_qcd.GetYaxis().SetTitle("Normalized Counts")
h_score_mixed_false_qcd.SetFillColorAlpha(ROOT.kBlue, 0.6)
h_score_mixed_false_qcd.Draw("histsameerror")
c.SetTitle("prova")



c.Draw()

leg.AddEntry(h_score_mixed_true, "score top mixed true")
leg.AddEntry(h_score_mixed_false_qcd, "score top mixed false qcd")
leg.AddEntry(h_score_mixed_false_other, "score top mixed false other")
leg.Draw("SAME")

c.SaveAs(f"{path_to_graphics_folder}/{component}_Discrimination_mixed.png")
c.SaveAs(f"{path_to_graphics_folder}/{component}_Discrimination_mixed.pdf")


ROOT.gStyle.SetOptStat(0)
c = ROOT.TCanvas("c", "c", 600, 600)
c.SetLogy()


leg = ROOT.TLegend(0.3, 0.6, 0.7, 0.9)
if h_score_mixed_true.Integral() !=0:
    h_score_mixed_true.Scale(1./h_score_mixed_true.Integral())
h_score_mixed_true.SetTitle("Discrimination")
h_score_mixed_true.GetXaxis().SetTitle("Score")
h_score_mixed_true.SetMaximum(1)
h_score_mixed_true.GetYaxis().SetTitle("Normalized Counts")
h_score_mixed_true.SetFillColorAlpha(ROOT.kRed, 0.6)
h_score_mixed_true.Draw("histsameerror")

if h_score_mixed_false_all.Integral() !=0:  
    h_score_mixed_false_all.Scale(1./h_score_mixed_false_all.Integral())
h_score_mixed_false_all.SetTitle("")
h_score_mixed_false_all.GetXaxis().SetTitle("Score")
h_score_mixed_false_all.SetMaximum(1)
h_score_mixed_false_all.GetYaxis().SetTitle("Normalized Counts")
h_score_mixed_false_all.SetFillColorAlpha(ROOT.kBlue, 0.6)
h_score_mixed_false_all.Draw("histsameerror")
c.SetTitle("prova")


c.Draw()

leg.AddEntry(h_score_mixed_true, "score top mixed true")
leg.AddEntry(h_score_mixed_false_all, "score top mixed false all")

leg.Draw("SAME")

c.SaveAs(f"{path_to_graphics_folder}/{component}_Discrimination_mixed_all.png")
c.SaveAs(f"{path_to_graphics_folder}/{component}_Discrimination_mixed_all.pdf")

c1 = ROOT.TCanvas("c1", "c1", 600, 600)
c1.SetLogy()


leg = ROOT.TLegend(0.3, 0.6, 0.7, 0.9)
if h_score_resolved_true.Integral() !=0:
    h_score_resolved_true.Scale(1./h_score_resolved_true.Integral())
h_score_resolved_true.SetTitle("Discrimination")
h_score_resolved_true.GetXaxis().SetTitle("Score")
h_score_resolved_true.SetMaximum(1)
h_score_resolved_true.GetYaxis().SetTitle("Normalized Counts")
h_score_resolved_true.SetFillColorAlpha(ROOT.kRed, 0.6)
h_score_resolved_true.Draw("histsameerror")

if h_score_resolved_false.Integral() !=0:
    h_score_resolved_false.Scale(1./h_score_resolved_false.Integral())
h_score_resolved_false.SetTitle("")
h_score_resolved_false.GetXaxis().SetTitle("Score")
h_score_resolved_false.SetMaximum(1)
h_score_resolved_false.GetYaxis().SetTitle("Normalized Counts")
h_score_resolved_false.SetFillColorAlpha(ROOT.kBlue, 0.6)
h_score_resolved_false.Draw("histsameerror")
c1.SetTitle("prova")
c1.Draw()

leg.AddEntry(h_score_resolved_true, "score top resolved true")
leg.AddEntry(h_score_resolved_false, "score top resolved false")
leg.Draw("SAME")

c1.SaveAs(f"{path_to_graphics_folder}/{component}_Discrimination_resolved.png")
c1.SaveAs(f"{path_to_graphics_folder}/{component}_Discrimination_resolved.pdf")


#CICLO FOR PER LA ROC
TPR_mixed = []
FPR_mixed_qcd = []
FPR_mixed_other = []
FPR_mixed_all = []
score_mixed = []
TPR_resolved = []
FPR_resolved = []
score_resolved = []
#faccio il for al contrario così inizio da score alti e TPR e FPR bassi
for bin in range (100,-1,-1):
    #se lo score tresh è 0 il TPR è 1
    if h_score_mixed_true.Integral(0,100) !=0:
        TPR_m = h_score_mixed_true.Integral(bin,100)/h_score_mixed_true.Integral(0,100)
    else:
        TPR_m = 0
    if h_score_mixed_false_qcd.Integral(0,100) !=0:
        FPR_m_qcd = h_score_mixed_false_qcd.Integral(bin,100)/h_score_mixed_false_qcd.Integral(0,100)
    else:
        FPR_m_qcd = 0
    if h_score_mixed_false_other.Integral(0,100) !=0:
        FPR_m_other = h_score_mixed_false_other.Integral(bin,100)/h_score_mixed_false_other.Integral(0,100)
    else:
        FPR_m_other = 0
    if h_score_mixed_false_all.Integral(0,100) !=0:
        FPR_m_all = h_score_mixed_false_all.Integral(bin,100)/h_score_mixed_false_all.Integral(0,100)
    else:
        FPR_m_all = 0
    score_m = h_score_mixed_false_all.GetBinCenter(h_score_mixed_false_all.GetBin(bin)) #avrei potuto mettere bin/100 ma forse così è più generale
    TPR_mixed.append(TPR_m)
    FPR_mixed_qcd.append(FPR_m_qcd)
    FPR_mixed_other.append(FPR_m_other)
    FPR_mixed_all.append(FPR_m_all)
    score_mixed.append(score_m)
    if h_score_resolved_true.Integral(0,100) !=0:
        TPR_r = h_score_resolved_true.Integral(bin,100)/h_score_resolved_true.Integral(0,100)
    else:
        TPR_r = 0
    if h_score_resolved_false.Integral(0,100) !=0:
        FPR_r = h_score_resolved_false.Integral(bin,100)/h_score_resolved_false.Integral(0,100) 
    else: 
        FPR_r = 0
    score_r = h_score_resolved_false.GetBinCenter(h_score_resolved_false.GetBin(bin))
    TPR_resolved.append(TPR_r)
    FPR_resolved.append(FPR_r)
    score_resolved.append(score_r)
#print("FPR:",FPR_mixed,"\n", "TPR:",TPR_mixed)



import matplotlib.pyplot as plt
plt.figure(1)
plt.plot(FPR_mixed_qcd, TPR_mixed,  linewidth=2, color="steelblue", linestyle="--")
plt.xlabel("False positives [%]")
plt.ylabel("True positives [%]")
# plt.xlim(xlim)
# plt.ylim(ylim)
plt.grid(True)
# ax = plt.gca()
# ax.set_aspect("equal")
plt.xscale("log")
plt.legend(loc="lower right")
plt.savefig(f"{path_to_graphics_folder}/{component}_roc_curve_mixed_qcd.png")
plt.savefig(f"{path_to_graphics_folder}/{component}_roc_curve_mixed_qcd.pdf")


plt.figure(2)
plt.plot(FPR_mixed_other, TPR_mixed,  linewidth=2, color="steelblue", linestyle="--")
plt.xlabel("False positives [%]")
plt.ylabel("True positives [%]")
# plt.xlim(xlim)
# plt.ylim(ylim)
plt.grid(True)
# ax = plt.gca()
# ax.set_aspect("equal")
plt.xscale("log")
plt.legend(loc="lower right")
plt.savefig(f"{path_to_graphics_folder}/{component}_roc_curve_mixed_other.png")
plt.savefig(f"{path_to_graphics_folder}/{component}_roc_curve_mixed_other.pdf")

plt.figure(3)
plt.plot(FPR_mixed_all, TPR_mixed,  linewidth=2, color="steelblue", linestyle="--")
plt.xlabel("False positives [%]")
plt.ylabel("True positives [%]")
# plt.xlim(xlim)
# plt.ylim(ylim)
plt.grid(True)
# ax = plt.gca()
# ax.set_aspect("equal")
plt.xscale("log")
plt.legend(loc="lower right")
plt.savefig(f"{path_to_graphics_folder}/{component}_roc_curve_mixed_all.png")
plt.savefig(f"{path_to_graphics_folder}/{component}_roc_curve_mixed_all.pdf")

plt.figure(4)
plt.plot(FPR_resolved, TPR_resolved,  linewidth=2, color="steelblue", linestyle="--")
plt.xlabel("False positives [%]")
plt.ylabel("True positives [%]")
# plt.xlim(xlim)
# plt.ylim(ylim)
plt.grid(True)
# ax = plt.gca()
# ax.set_aspect("equal")
plt.xscale("log")
plt.legend(loc="lower right")
plt.savefig(f"{path_to_graphics_folder}/{component}roc_curve_resolved.png")
plt.savefig(f"{path_to_graphics_folder}/{component}roc_curve_resolved.pdf")
#!/usr/bin/env python
import os
import sys
import ROOT
ROOT.PyConfig.IgnoreCommandLineOptions = True
import matplotlib.pyplot as plt
import mplhep as hep
import cmsstyle as CMS
hep.style.use("CMS")

def plotEfficiency(h_den, h_eff_merged, h_eff_mixed, h_eff_resolved, canv_name = "canv" ,extraTest="Work in progress", iPos=0, energy="13.6", lumi = "",  addInfo="", ytitle = "", samplelabel = "t#bar{t}", ymax=0):
    CMS.SetExtraText(extraTest)
    iPos = iPos
    canv_name = canv_name
    CMS.SetLumi(lumi)
    CMS.SetEnergy(energy)
    CMS.ResetAdditionalInfo()
    CMS.AppendAdditionalInfo(addInfo)
    CMS.setCMSStyle()
    x_min = h_den.GetXaxis().GetXmin()
    x_max = h_den.GetXaxis().GetXmax()
    y_min = 0.
    if ymax!=0: y_max = ymax
    else: y_max = 1.5#max([eff.GetEfficiency(i) for i in range(eff.GetTotalHistogram().GetNbinsX())]) +0.2
    print(y_max)
    x_axis_name = h_den.GetXaxis().GetTitle()
    ytitle = h_den.GetYaxis().GetTitle()
    canv = CMS.cmsCanvas(canv_name,x_min,x_max, y_min ,y_max,x_axis_name,ytitle,square=CMS.kRectangular, extraSpace=20.0, iPos=iPos)
    hdf = CMS.GetcmsCanvasHist(canv)
    hdf.GetYaxis().SetMaxDigits(1)
    hdf.GetYaxis().SetLabelOffset(0.001)
    hdf.GetYaxis().SetLabelSize(0.045)
    hdf.GetYaxis().SetTitleOffset(1.1)
    hdf.GetYaxis().SetTitleSize(0.045)
    hdf.GetXaxis().SetLabelOffset(0.001)
    hdf.GetXaxis().SetLabelSize(0.045)
    hdf.GetXaxis().SetTitleOffset(1.1)
    hdf.GetXaxis().SetTitleSize(0.045)
    h_eff_merged.SetMarkerColor(2)
    h_eff_merged.SetLineColor(2)
    h_eff_merged.SetMarkerStyle(8)
    h_eff_mixed.SetMarkerColor(5)
    h_eff_mixed.SetLineColor(5)
    h_eff_mixed.SetMarkerStyle(8)
    h_eff_resolved.SetMarkerColor(7)
    h_eff_resolved.SetLineColor(7)
    h_eff_resolved.SetMarkerStyle(8)
    h_eff_merged.Draw("same")
    h_eff_mixed.Draw("same")
    h_eff_resolved.Draw("same")
    # canv.SetLogy()
    # Shift multiplier position
    ROOT.TGaxis.SetExponentOffset(-0.10, 0.01, "Y")
    # leg = CMS.cmsLeg(0.5, 0.1, 0.98, 0.5, textSize=0.04)
    return canv

def efficiency_calculator(h_num, h_den, h_eff):
    for i in range(0, h_eff.GetNbinsX() + 2):
        num = h_num.GetBinContent(i)
        den = h_den.GetBinContent(i)
        num_error = h_num.GetBinError(i)
        den_error = h_den.GetBinError(i)
        
        if den != 0 and num != 0:
            eff = num / den
            error = ((eff * (1-eff))/den) ** 0.5
            h_eff.SetBinError(i, error)
        else:
            eff=0
            h_eff.SetBinError(i, 0)  # Imposta errore a 0 se il denominatore è 0 (da vedere come gesitire in maniera corretta)
        h_eff.SetBinContent(i, eff)
    return h_eff

dirpath = "/eos/user/f/fsalerno/Evaluation/Prelim/"
path_to_graphic_folder = "/eos/user/f/fsalerno/Evaluation"
file_name="recoTagNumber_histos_presel.root"
inFile = f"{dirpath}/{file_name}"
histos_file = ROOT.TFile.Open(inFile)
h_den = histos_file.Get("recoTagNumber/h_hadronic_top_gen")
print(histos_file.ls())
keys=["60_CNN_2D_0_pt","60_CNN_2D_LSTM_0_pt","60_CNN_2D_2_0_pt","60_CNN_2D_LSTM_2_0_pt"]
h_reco_num_mixed = {}
for key in keys:
    h_reco_num_mixed[key] = histos_file.Get(f"recoTagNumber/h_recoNumber_mixed_{key}")
    #print(h_reco_num_mixed)
h_reco_num_resolved = histos_file.Get(f"recoTagNumber/h_recoNumber_resolved")
h_reco_num_merged = histos_file.Get(f"recoTagNumber/h_recoNumber_merged")

h_reco_tag_num_mixed = {}
for key in keys:
    h_reco_tag_num_mixed[key] = histos_file.Get(f"recoTagNumber/h_recoTagNumber_mixed_{key}")
    #print(h_reco_tag_num_mixed)
h_reco_tag_num_resolved = histos_file.Get(f"recoTagNumber/h_recoTagNumber_resolved")
h_reco_tag_num_merged = histos_file.Get(f"recoTagNumber/h_recoTagNumber_merged")
h_reco_tag_num_merged_high_pt_thr = histos_file.Get(f"recoTagNumber/h_recoTagNumber_merged_high_pt_thr")
h_reco_tag_num_merged_Antimo_thr = histos_file.Get(f"recoTagNumber/h_recoTagNumber_merged_Antimo_thr")

h_reco_eff_mixed = {}
h_reco_tag_eff_mixed = {}
for key in keys:
    h_reco_eff_mixed[key] = h_reco_num_mixed[key].Clone()
    #h_reco_eff_mixed[key].Divide(h_den)
    h_reco_eff_mixed[key] = efficiency_calculator(h_reco_num_mixed[key], h_den, h_reco_eff_mixed[key])

    h_reco_tag_eff_mixed[key] = h_reco_tag_num_mixed[key].Clone()
    #h_reco_tag_eff_mixed[key].Divide(h_den)
    h_reco_tag_eff_mixed[key] = efficiency_calculator(h_reco_tag_num_mixed[key], h_den, h_reco_tag_eff_mixed[key])

h_reco_eff_resolved = h_reco_num_resolved.Clone()
#h_reco_eff_resolved.Divide(h_den)
h_reco_eff_resolved = efficiency_calculator(h_reco_num_resolved, h_den, h_reco_eff_resolved)
h_reco_eff_merged = h_reco_num_merged.Clone()
h_reco_eff_merged = efficiency_calculator(h_reco_num_merged, h_den, h_reco_eff_merged)
#h_reco_eff_merged.Divide(h_den)

h_reco_tag_eff_resolved = h_reco_tag_num_resolved.Clone()
h_reco_tag_eff_resolved = efficiency_calculator(h_reco_tag_num_resolved, h_den, h_reco_tag_eff_resolved)
h_reco_tag_eff_merged = h_reco_tag_num_merged.Clone()
h_reco_tag_eff_merged = efficiency_calculator(h_reco_tag_num_merged, h_den, h_reco_tag_eff_merged)
h_reco_tag_eff_merged_high_pt_thr = h_reco_tag_num_merged_high_pt_thr.Clone()
h_reco_tag_eff_merged_high_pt_thr = efficiency_calculator(h_reco_tag_num_merged_high_pt_thr, h_den, h_reco_tag_eff_merged_high_pt_thr)
h_reco_tag_eff_merged_Antimo_thr = h_reco_tag_num_merged_Antimo_thr.Clone()
h_reco_tag_eff_merged_Antimo_thr = efficiency_calculator(h_reco_tag_num_merged_Antimo_thr, h_den, h_reco_tag_eff_merged_Antimo_thr)



outFile = ROOT.TFile(f"{path_to_graphic_folder}/RecoEff.root", "RECREATE")    
h_reco_eff_resolved.Write()
h_reco_eff_merged.Write()
h_reco_tag_eff_resolved.Write()
h_reco_tag_eff_merged.Write()
for key in keys:
    h_reco_eff_mixed[key].Write()
    h_reco_tag_eff_mixed[key].Write()
outFile.Close()

c_reco={}
for key in keys:
    h_den.SetTitle("Reconstruction efficiency")
    h_den.GetXaxis().SetTitle("p_{T}^{gen} [GeV]")
    h_den.GetYaxis().SetTitle("Reco Efficiency")
    c_reco[key]=plotEfficiency(h_den=h_den, h_eff_merged=h_reco_eff_merged, h_eff_mixed=h_reco_eff_mixed[key], h_eff_resolved=h_reco_eff_resolved, canv_name=f"c_reco_efficiency_{key}") 
    c_reco[key].SaveAs(f"{path_to_graphic_folder}/RecoEff_{key}.png")

c_reco_tag={}
for key in keys:
    h_den.SetTitle("Reconstruction efficiency")
    h_den.GetXaxis().SetTitle("p_{T}^{gen} [GeV]")
    h_den.GetYaxis().SetTitle("Reco*Tag Efficiency")
    c_reco_tag[key]=plotEfficiency(h_den=h_den, h_eff_merged=h_reco_tag_eff_merged, h_eff_mixed=h_reco_tag_eff_mixed[key], h_eff_resolved=h_reco_tag_eff_resolved, canv_name=f"c_reco_tag_efficiency_{key}") 
    c_reco_tag[key].SaveAs(f"{path_to_graphic_folder}/RecoTagEff_{key}.png")

c_reco_tag_high_pt={}
for key in keys:
    h_den.SetTitle("Reconstruction efficiency")
    h_den.GetXaxis().SetTitle("p_{T}^{gen} [GeV]")
    h_den.GetYaxis().SetTitle("Reco*Tag Efficiency")
    c_reco_tag_high_pt[key]=plotEfficiency(h_den=h_den, h_eff_merged=h_reco_tag_eff_merged_high_pt_thr, h_eff_mixed=h_reco_tag_eff_mixed[key], h_eff_resolved=h_reco_tag_eff_resolved, canv_name=f"c_reco_tag_high_pt_efficiency_{key}") 
    c_reco_tag_high_pt[key].SaveAs(f"{path_to_graphic_folder}/RecoTagEffHighPtThr_{key}.png")

c_reco_tag_Antimo={}
for key in keys:
    h_den.SetTitle("Reconstruction efficiency")
    h_den.GetXaxis().SetTitle("p_{T}^{gen} [GeV]")
    h_den.GetYaxis().SetTitle("Reco*Tag Efficiency")
    c_reco_tag_Antimo[key]=plotEfficiency(h_den=h_den, h_eff_merged=h_reco_tag_eff_merged_Antimo_thr, h_eff_mixed=h_reco_tag_eff_mixed[key], h_eff_resolved=h_reco_tag_eff_resolved, canv_name=f"c_reco_tag_Antimo_efficiency_{key}") 
    c_reco_tag_Antimo[key].SaveAs(f"{path_to_graphic_folder}/RecoTagAntimoThr_{key}.png")
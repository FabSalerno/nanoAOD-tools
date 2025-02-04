import ROOT 
import numpy as np
import argparse
from curses import keyname
import json
import os
import sys
import samples

dirpath = "/eos/user/f/fsalerno/framework/MachineLearning/Evaluate_PF/no_presel/"
path_to_graphic_folder = "/eos/user/f/fsalerno/framework/MachineLearning/Evaluate_PF/no_presel/graphics/"
components = ["TT_semilep_2022","QCD_HT1000to1200_2022","QCD_HT1200to1500_2022","QCD_HT1500to2000_2022"]

file_dict={}
for c in components:
    for f, file_name in enumerate(os.listdir(dirpath)):
        if not file_name.startswith('.') and c in file_name:
            inFile=dirpath+file_name
            file_dict[c]=ROOT.TFile.Open(inFile)

path_to_model_folder    = "/eos/user/f/fsalerno/framework/MachineLearning/models/"
mods                    = ["CNN","CNN_2D","CNN_conc","CNN_2D_conc","transformer","LSTM","LSTM_DNN","CNN_2D_LSTM","CNN_2D_LSTM_conc","TROTA"]
cuts                    = ["","_0_pt","_200_pt","_300_pt"]
n_PFCs                  = 20
models                  = {}

keys=[]
for mod in mods:
    for cut in cuts:
        key=f"{n_PFCs}_{mod}{cut}"
        if os.path.isfile(f"{path_to_model_folder}/model_{key}.h5"):
            keys.append(key)


histo_dict = {}

# Initialize all histogram dictionaries before the loop starts
h_score_top_mixed_true = {}
h_score_top_mixed_false_other = {}
h_score_top_mixed_false_QCD = {}
h_score_top_mixed_false_all = {}
h_score_top_mixed_true_cut_200_pt = {}
h_score_top_mixed_false_other_cut_200_pt = {}
h_score_top_mixed_false_QCD_cut_200_pt = {}
h_score_top_mixed_false_all_cut_200_pt = {}
h_score_top_mixed_true_cut_300_pt = {}
h_score_top_mixed_false_other_cut_300_pt = {}
h_score_top_mixed_false_QCD_cut_300_pt = {}
h_score_top_mixed_false_all_cut_300_pt = {}


h_score_3j1fj_true = {}
h_score_3j0fj_true = {}
h_score_2j1fj_true = {}
h_score_3j1fj_false = {}
h_score_3j0fj_false = {}
h_score_2j1fj_false = {}

# PT Top
h_pt_top_mixed_true = {}
h_pt_top_mixed_false_other = {}
h_pt_top_mixed_false_QCD = {}
h_pt_top_mixed_false_all = {}
h_pt_5_100 = {}
h_pt_1_100 = {}
h_pt_1_1000 = {}

# N Events
h_event_counter_pre = {}
h_event_counter_post = {}
h_event_counter_5_100 = {}
h_event_counter_1_100 = {}
h_event_counter_1_1000 = {}
h_event_counter_5_100_cut_200_pt = {}
h_event_counter_1_100_cut_200_pt = {}
h_event_counter_1_1000_cut_200_pt = {}
h_event_counter_5_100_cut_300_pt = {}
h_event_counter_1_100_cut_300_pt = {}
h_event_counter_1_1000_cut_300_pt = {}


# MET
h_MET_pre_all = {}
h_MET_post_all = {}
h_MET_5_100 = {}
h_MET_1_100 = {}
h_MET_1_1000 = {}

# Mass Top
h_mass_top_mixed_true = {}
h_mass_top_mixed_false_other = {}
h_mass_top_mixed_false_QCD = {}
h_mass_top_mixed_false_all = {}
h_mass_5_100 = {}
h_mass_1_100 = {}
h_mass_1_1000 = {}

for c in components:
    # Initialize the dictionary for the component if not already initialized
    if c not in histo_dict:
        histo_dict[c] = {}

    for key in keys:
        # Scores
        h_score_top_mixed_true[key] = file_dict[c].Get(f"score_top_mixed_true_{key}")
        h_score_top_mixed_false_other[key] = file_dict[c].Get(f"score_top_mixed_false_other_{key}")
        h_score_top_mixed_false_QCD[key] = file_dict[c].Get(f"score_top_mixed_false_qcd_{key}")
        h_score_top_mixed_false_all[key] = file_dict[c].Get(f"score_top_mixed_false_all_{key}")
        h_score_top_mixed_true_cut_200_pt[key] = file_dict[c].Get(f"score_top_mixed_true_cut_200_pt_{key}")
        h_score_top_mixed_false_other_cut_200_pt[key] = file_dict[c].Get(f"score_top_mixed_false_other_cut_200_pt_{key}")
        h_score_top_mixed_false_QCD_cut_200_pt[key] = file_dict[c].Get(f"score_top_mixed_false_qcd_cut_200_pt_{key}")
        h_score_top_mixed_false_all_cut_200_pt[key] = file_dict[c].Get(f"score_top_mixed_false_all_cut_200_pt_{key}")
        h_score_top_mixed_true_cut_300_pt[key] = file_dict[c].Get(f"score_top_mixed_true_cut_300_pt_{key}")
        h_score_top_mixed_false_other_cut_300_pt[key] = file_dict[c].Get(f"score_top_mixed_false_other_cut_300_pt_{key}")
        h_score_top_mixed_false_QCD_cut_300_pt[key] = file_dict[c].Get(f"score_top_mixed_false_qcd_cut_300_pt_{key}")
        h_score_top_mixed_false_all_cut_300_pt[key] = file_dict[c].Get(f"score_top_mixed_false_all_cut_300_pt_{key}")
        h_score_3j1fj_true[key] = file_dict[c].Get(f"score_3j1fj_true_{key}")
        h_score_3j0fj_true[key] = file_dict[c].Get(f"score_3j0fj_true_{key}")
        h_score_2j1fj_true[key] = file_dict[c].Get(f"score_2j1fj_true_{key}")
        h_score_3j1fj_false[key] = file_dict[c].Get(f"score_3j1fj_false_{key}")
        h_score_3j0fj_false[key] = file_dict[c].Get(f"score_3j0fj_false_{key}")
        h_score_2j1fj_false[key] = file_dict[c].Get(f"score_2j1fj_false_{key}")

        # PT Top
        h_pt_top_mixed_true[key] = file_dict[c].Get(f"pt_top_mixed_true_{key}")
        h_pt_top_mixed_false_other[key] = file_dict[c].Get(f"pt_top_mixed_false_other_{key}")
        h_pt_top_mixed_false_QCD[key] = file_dict[c].Get(f"pt_top_mixed_false_qcd_{key}")
        h_pt_top_mixed_false_all[key] = file_dict[c].Get(f"pt_top_mixed_false_all_{key}")
        h_pt_5_100[key] = file_dict[c].Get(f"pt_5_per_100_{key}")
        h_pt_1_100[key] = file_dict[c].Get(f"pt_1_per_100_{key}")
        h_pt_1_1000[key] = file_dict[c].Get(f"pt_1_per_1000_{key}")

        # N Events
        h_event_counter_pre[key] = file_dict[c].Get(f"nevents_pre")
        h_event_counter_post[key] = file_dict[c].Get(f"nevents_post")
        h_event_counter_5_100[key] = file_dict[c].Get(f"nevents_5_per_100_{key}")
        h_event_counter_1_100[key] = file_dict[c].Get(f"nevents_1_per_100_{key}")
        h_event_counter_1_1000[key] = file_dict[c].Get(f"nevents_1_per_1000_{key}")
        h_event_counter_5_100_cut_200_pt[key] = file_dict[c].Get(f"nevents_5_per_100_cut_200_pt_{key}")
        h_event_counter_1_100_cut_200_pt[key] = file_dict[c].Get(f"nevents_1_per_100_cut_200_pt_{key}")
        h_event_counter_1_1000_cut_200_pt[key] = file_dict[c].Get(f"nevents_1_per_1000_cut_200_pt_{key}")
        h_event_counter_5_100_cut_300_pt[key] = file_dict[c].Get(f"nevents_5_per_100_cut_300_pt_{key}")
        h_event_counter_1_100_cut_300_pt[key] = file_dict[c].Get(f"nevents_1_per_100_cut_300_pt_{key}")
        h_event_counter_1_1000_cut_300_pt[key] = file_dict[c].Get(f"nevents_1_per_1000_cut_300_pt_{key}")

        # MET
        h_MET_pre_all[key] = file_dict[c].Get(f"MET_pre")
        h_MET_post_all[key] = file_dict[c].Get(f"MET_post")
        h_MET_5_100[key] = file_dict[c].Get(f"MET_5_per_100_{key}")
        h_MET_1_100[key] = file_dict[c].Get(f"MET_1_per_100_{key}")
        h_MET_1_1000[key] = file_dict[c].Get(f"MET_1_per_1000_{key}")

        # Mass Top
        h_mass_top_mixed_true[key] = file_dict[c].Get(f"mass_top_mixed_true_{key}")
        h_mass_top_mixed_false_other[key] = file_dict[c].Get(f"mass_top_mixed_false_other_{key}")
        h_mass_top_mixed_false_QCD[key] = file_dict[c].Get(f"mass_top_mixed_false_qcd_{key}")
        h_mass_top_mixed_false_all[key] = file_dict[c].Get(f"mass_top_mixed_false_all_{key}")
        h_mass_5_100[key] = file_dict[c].Get(f"mass_5_per_100_{key}")
        h_mass_1_100[key] = file_dict[c].Get(f"mass_1_per_100_{key}")
        h_mass_1_1000[key] = file_dict[c].Get(f"mass_1_per_1000_{key}")

        # Store the data in histo_dict
        histo_dict[c][key] = { 
            #score
            f"h_score_top_mixed_true_{key}":h_score_top_mixed_true[key],
            f"h_score_top_mixed_false_other_{key}":h_score_top_mixed_false_other[key],
            f"h_score_top_mixed_false_QCD_{key}":h_score_top_mixed_false_QCD[key],
            f"h_score_top_mixed_false_all_{key}":h_score_top_mixed_false_all[key],
            f"h_score_top_mixed_true_cut_200_pt_{key}":h_score_top_mixed_true_cut_200_pt[key],
            f"h_score_top_mixed_false_other_cut_200_pt_{key}":h_score_top_mixed_false_other_cut_200_pt[key],
            f"h_score_top_mixed_false_QCD_cut_200_pt_{key}":h_score_top_mixed_false_QCD_cut_200_pt[key],
            f"h_score_top_mixed_false_all_cut_200_pt_{key}":h_score_top_mixed_false_all_cut_200_pt[key],
            f"h_score_top_mixed_true_cut_300_pt_{key}":h_score_top_mixed_true_cut_300_pt[key],
            f"h_score_top_mixed_false_other_cut_300_pt_{key}":h_score_top_mixed_false_other_cut_300_pt[key],
            f"h_score_top_mixed_false_QCD_cut_300_pt_{key}":h_score_top_mixed_false_QCD_cut_300_pt[key],
            f"h_score_top_mixed_false_all_cut_300_pt_{key}":h_score_top_mixed_false_all_cut_300_pt[key],
            f"h_score_3j1fj_true_{key}" : h_score_3j1fj_true[key],
            f"h_score_3j0fj_true_{key}" : h_score_3j0fj_true[key],
            f"h_score_2j1fj_true_{key}" : h_score_2j1fj_true[key],
            f"h_score_3j1fj_false_{key}" : h_score_3j1fj_false[key],
            f"h_score_3j0fj_false_{key}" : h_score_3j0fj_false[key],
            f"h_score_2j1fj_false_{key}" : h_score_2j1fj_false[key],
            #pt top
            f"h_pt_top_mixed_true_{key}": h_pt_top_mixed_true[key],
            f"h_pt_top_mixed_false_other_{key}": h_pt_top_mixed_false_other[key],
            f"h_pt_top_mixed_false_QCD_{key}": h_pt_top_mixed_false_QCD[key],
            f"h_pt_top_mixed_false_all_{key}": h_pt_top_mixed_false_all[key],
            f"h_pt_5_100_{key}": h_pt_5_100[key],
            f"h_pt_1_100_{key}": h_pt_1_100[key],
            f"h_pt_1_1000_{key}": h_pt_1_1000[key],
            # n events
            f"h_event_counter_pre_{key}": h_event_counter_pre[key],
            f"h_event_counter_post_{key}": h_event_counter_post[key],
            f"h_event_counter_5_100_{key}": h_event_counter_5_100[key],
            f"h_event_counter_5_100_cut_200_pt_{key}": h_event_counter_5_100_cut_200_pt[key],
            f"h_event_counter_5_100_cut_300_pt_{key}": h_event_counter_5_100_cut_300_pt[key],
            f"h_event_counter_1_100_{key}": h_event_counter_1_100[key],
            f"h_event_counter_1_100_cut_200_pt_{key}": h_event_counter_1_100_cut_200_pt[key],
            f"h_event_counter_1_100_cut_300_pt_{key}": h_event_counter_1_100_cut_300_pt[key],
            f"h_event_counter_1_1000_{key}": h_event_counter_1_1000[key],
            f"h_event_counter_1_1000_cut_200_pt_{key}": h_event_counter_1_1000_cut_200_pt[key],
            f"h_event_counter_1_1000_cut_300_pt_{key}": h_event_counter_1_1000_cut_300_pt[key],
            # MET
            f"h_MET_pre_all_{key}": h_MET_pre_all[key],
            f"h_MET_post_all_{key}": h_MET_post_all[key],
            f"h_MET_5_100_{key}": h_MET_5_100[key],
            f"h_MET_1_100_{key}": h_MET_1_100[key],
            f"h_MET_1_1000_{key}": h_MET_1_1000[key],
            # mass top
            f"h_mass_top_mixed_true_{key}": h_mass_top_mixed_true[key],
            f"h_mass_top_mixed_false_other_{key}": h_mass_top_mixed_false_other[key],
            f"h_mass_top_mixed_false_QCD_{key}": h_mass_top_mixed_false_QCD[key],
            f"h_mass_top_mixed_false_all_{key}": h_mass_top_mixed_false_all[key],
            f"h_mass_5_100_{key}": h_mass_5_100[key],
            f"h_mass_1_100_{key}": h_mass_1_100[key],
            f"h_mass_1_1000_{key}": h_mass_1_1000[key],
        }


normalizations={}
key="20_TROTA"
for c in components:
    sample = getattr(samples, c)
    n_gen_events = histo_dict[c][key][f"h_event_counter_pre_{key}"].GetEntries()
    print(n_gen_events,c)
    cross_sec = sample.sigma
    print("cross section",cross_sec)
    norm = cross_sec/n_gen_events
    normalizations[c]=norm


def prepare_histogram(hist, num_bins, x_min, x_max):
    if hist.GetNbinsX() != num_bins or hist.GetXaxis().GetXmin() != x_min or hist.GetXaxis().GetXmax() != x_max:
        new_hist = ROOT.TH1F(hist.GetName() + "_rebinned", hist.GetTitle(), num_bins, x_min, x_max)
        for bin_idx in range(1, hist.GetNbinsX() + 1):  # Copy existing bin content
            new_hist.SetBinContent(bin_idx, hist.GetBinContent(bin_idx))
        hist = new_hist
    

    hist.SetBinContent(0, 0)
    hist.SetBinContent(hist.GetNbinsX() + 1, 0)  
    return hist

num_bins = 8
x_min = 0
x_max = 8


ROOT.gStyle.SetOptStat(0)
# List of wanted components and keys
wanted_components = ["TT_semilep_2022"]

# Canvas setup
c = ROOT.TCanvas("c", "c", 600, 600)

# Initialize dictionaries for histograms
histo_events_pre_signal = {}
histo_events_post_signal = {}
histo_events_1_100_signal = {}
histo_events_1_1000_signal = {}
histo_events_5_100_signal = {}

# Loop over keys to create histograms for each
for key in keys:
    histo_events_pre_signal[key] = ROOT.TH1F(f"n_events_pre_{key}", f"n_events_pre_{key}", 8, 0, 8)
    histo_events_post_signal[key] = ROOT.TH1F(f"n_events_post_{key}", f"n_events_post_{key}", 8, 0, 8)
    histo_events_1_100_signal[key] = ROOT.TH1F(f"n_events_1_100_{key}", f"n_events_1_100_{key}", 8, 0, 8)
    histo_events_1_1000_signal[key] = ROOT.TH1F(f"n_events_1_1000_{key}", f"n_events_1_1000_{key}", 8, 0, 8)
    histo_events_5_100_signal[key] = ROOT.TH1F(f"n_events_5_100_{key}", f"n_events_5_100_{key}", 8, 0, 8)
    histo_events_5_100_signal_TROTA = ROOT.TH1F("n_events_5_100_TROTA", f"n_events_5_100_TROTA", 8, 0, 8)
    histo_events_1_100_signal_TROTA = ROOT.TH1F("n_events_1_100_TROTA", f"n_events_1_100_TROTA", 8, 0, 8)
    histo_events_1_1000_signal_TROTA = ROOT.TH1F("n_events_1_1000_TROTA", f"n_events_1_1000_TROTA", 8, 0, 8)

    # Processing and filling histograms
    for w in wanted_components:
        print(w,key)
        if histo_dict[w][key][f"h_event_counter_pre_{key}"].Integral() > 0:
            histo_norm_1 = prepare_histogram(histo_dict[w][key][f"h_event_counter_pre_{key}"].Clone(), num_bins, x_min, x_max)
            histo_norm_1.Scale(normalizations[w])
            histo_events_pre_signal[key].Add(histo_norm_1)

            histo_norm_2 = prepare_histogram(histo_dict[w][key][f"h_event_counter_post_{key}"].Clone(), num_bins, x_min, x_max)
            histo_norm_2.Scale(normalizations[w])
            histo_events_post_signal[key].Add(histo_norm_2)

            histo_norm_3 = prepare_histogram(histo_dict[w][key][f"h_event_counter_5_100_{key}"].Clone(), num_bins, x_min, x_max)
            histo_norm_3.Scale(normalizations[w])
            histo_events_5_100_signal[key].Add(histo_norm_3)
            
            if "200_pt"in key:
                histo_norm_4 = prepare_histogram(histo_dict[w]["20_TROTA_200_pt"]["h_event_counter_5_100_20_TROTA_200_pt"].Clone(), num_bins, x_min, x_max)
            elif "300_pt"in key:
                histo_norm_4 = prepare_histogram(histo_dict[w]["20_TROTA_300_pt"]["h_event_counter_5_100_20_TROTA_300_pt"].Clone(), num_bins, x_min, x_max)
            else:
                histo_norm_4 = prepare_histogram(histo_dict[w]["20_TROTA"]["h_event_counter_5_100_20_TROTA"].Clone(), num_bins, x_min, x_max)
            source_bin_4 = 3
            target_bin_4 = 4
            source_content_4 = histo_norm_4.GetBinContent(source_bin_4)
            target_content_4 = histo_norm_4.GetBinContent(target_bin_4)
            histo_norm_4.SetBinContent(target_bin_4, target_content_4 + source_content_4)
            histo_norm_4.SetBinContent(source_bin_4, 0)
            histo_norm_4.Scale(normalizations[w])
            histo_events_5_100_signal_TROTA.Add(histo_norm_4)

            histo_norm_5 = prepare_histogram(histo_dict[w][key][f"h_event_counter_1_100_{key}"].Clone(), num_bins, x_min, x_max)
            source_bin_5 = 4
            target_bin_5 = 5
            source_content_5 = histo_norm_5.GetBinContent(source_bin_5)
            target_content_5 = histo_norm_5.GetBinContent(target_bin_5)
            histo_norm_5.SetBinContent(target_bin_5, target_content_5 + source_content_5)
            histo_norm_5.SetBinContent(source_bin_5, 0)
            histo_norm_5.Scale(normalizations[w])
            histo_events_1_100_signal[key].Add(histo_norm_5)
            
            if "200_pt"in key:
                histo_norm_6 = prepare_histogram(histo_dict[w]["20_TROTA_200_pt"]["h_event_counter_1_100_20_TROTA_200_pt"].Clone(), num_bins, x_min, x_max)
            elif "300_pt"in key:
                histo_norm_6 = prepare_histogram(histo_dict[w]["20_TROTA_300_pt"]["h_event_counter_1_100_20_TROTA_300_pt"].Clone(), num_bins, x_min, x_max)
            else:
                histo_norm_6 = prepare_histogram(histo_dict[w]["20_TROTA"]["h_event_counter_1_100_20_TROTA"].Clone(), num_bins, x_min, x_max)
            source_bin_6 = 4
            target_bin_6 = 6
            source_content_6 = histo_norm_6.GetBinContent(source_bin_6)
            target_content_6 = histo_norm_6.GetBinContent(target_bin_6)
            histo_norm_6.SetBinContent(target_bin_6, target_content_6 + source_content_6)
            histo_norm_6.SetBinContent(source_bin_6, 0)
            histo_norm_6.Scale(normalizations[w])
            histo_events_1_100_signal_TROTA.Add(histo_norm_6)

            histo_norm_7 = prepare_histogram(histo_dict[w][key][f"h_event_counter_1_1000_{key}"].Clone(), num_bins, x_min, x_max)
            source_bin_7 = 5
            target_bin_7 = 7
            source_content_7 = histo_norm_7.GetBinContent(source_bin_7)
            target_content_7 = histo_norm_7.GetBinContent(target_bin_7)
            histo_norm_7.SetBinContent(target_bin_7, target_content_7 + source_content_7)
            histo_norm_7.SetBinContent(source_bin_7, 0)
            histo_norm_7.Scale(normalizations[w])
            histo_events_1_1000_signal[key].Add(histo_norm_7)
            
            if "200_pt"in key:
                histo_norm_8 = prepare_histogram(histo_dict[w]["20_TROTA_200_pt"]["h_event_counter_1_1000_20_TROTA_200_pt"].Clone(), num_bins, x_min, x_max)
            elif "300_pt"in key:
                histo_norm_8 = prepare_histogram(histo_dict[w]["20_TROTA_300_pt"]["h_event_counter_1_1000_20_TROTA_300_pt"].Clone(), num_bins, x_min, x_max)
            else:
                histo_norm_8 = prepare_histogram(histo_dict[w]["20_TROTA"]["h_event_counter_1_1000_20_TROTA"].Clone(), num_bins, x_min, x_max)
            source_bin_8 = 5
            target_bin_8 = 8
            source_content_8 = histo_norm_8.GetBinContent(source_bin_8)
            target_content_8 = histo_norm_8.GetBinContent(target_bin_8)
            histo_norm_8.SetBinContent(target_bin_8, target_content_8 + source_content_8)
            histo_norm_8.SetBinContent(source_bin_8, 0)
            histo_norm_8.Scale(normalizations[w])
            histo_events_1_100_signal_TROTA.Add(histo_norm_8)

        else:
            print(f"histo {key} for {w} is empty")

    # Drawing histograms
    histo_events_pre_signal[key].SetTitle(f"Signal events after cuts for {key}")
    histo_events_pre_signal[key].GetXaxis().SetRangeUser(0, 8)

    histo_events_pre_signal[key].GetYaxis().SetTitle("Normalized Events")
    histo_events_pre_signal[key].GetXaxis().SetBinLabel(1, "no selection")
    histo_events_pre_signal[key].GetXaxis().SetBinLabel(2, "preselection")
    histo_events_pre_signal[key].GetXaxis().SetBinLabel(3, f"5% {key}")
    histo_events_pre_signal[key].GetXaxis().SetBinLabel(4, f"5% TROTA")
    histo_events_pre_signal[key].GetXaxis().SetBinLabel(5, f"1% {key}")
    histo_events_pre_signal[key].GetXaxis().SetBinLabel(6, f"1% TROTA")
    histo_events_pre_signal[key].GetXaxis().SetBinLabel(7, f"0.1% {key}")
    histo_events_pre_signal[key].GetXaxis().SetBinLabel(8, f"0.1% TROTA")

    # Draw all histograms for the current key
    histo_events_pre_signal[key].Draw("histo")
    histo_events_post_signal[key].Draw("histosame")
    histo_events_5_100_signal[key].Draw("histosame")
    histo_events_1_100_signal[key].Draw("histosame")
    histo_events_1_1000_signal[key].Draw("histosame")
    histo_events_5_100_signal_TROTA.Draw("histosame")
    histo_events_1_100_signal_TROTA.Draw("histosame")
    histo_events_1_1000_signal_TROTA.Draw("histosame")

    # Enable log scale and draw the canvas
    c.SetLogy()
    c.Draw()
    c.SaveAs(f"{path_to_graphic_folder}signal_cuts/signal_events_{key}.pdf")

    # Reset all histograms for the current key before moving to the next key
    histo_events_pre_signal[key].Reset()
    histo_events_post_signal[key].Reset()
    histo_events_5_100_signal[key].Reset()
    histo_events_1_100_signal[key].Reset()
    histo_events_1_1000_signal[key].Reset()
    histo_events_5_100_signal_TROTA.Reset()
    histo_events_1_100_signal_TROTA.Reset()
    histo_events_1_1000_signal_TROTA.Reset()



# Canvas setup
c = ROOT.TCanvas("c", "c", 600, 600)

# Initialize dictionaries for histograms
histo_events_pre_signal = {}
histo_events_post_signal = {}
histo_events_1_100_cut_200_pt_signal = {}
histo_events_1_1000_cut_200_pt_signal = {}
histo_events_5_100_cut_200_pt_signal = {}

# Loop over keys to create histograms for each
for key in keys:
    histo_events_pre_signal[key] = ROOT.TH1F(f"n_events_pre_{key}", f"n_events_pre_{key}", 8, 0, 8)
    histo_events_post_signal[key] = ROOT.TH1F(f"n_events_post_{key}", f"n_events_post_{key}", 8, 0, 8)
    histo_events_1_100_cut_200_pt_signal[key] = ROOT.TH1F(f"n_events_1_100_cut_200_pt_{key}", f"n_events_1_100_cut_200_pt_{key}", 8, 0, 8)
    histo_events_1_1000_cut_200_pt_signal[key] = ROOT.TH1F(f"n_events_1_1000_cut_200_pt_{key}", f"n_events_1_1000_cut_200_pt_{key}", 8, 0, 8)
    histo_events_5_100_cut_200_pt_signal[key] = ROOT.TH1F(f"n_events_5_100_cut_200_pt_{key}", f"n_events_5_100_cut_200_pt_{key}", 8, 0, 8)
    histo_events_5_100_cut_200_pt_signal_TROTA = ROOT.TH1F("n_events_5_100_cut_200_pt_TROTA", f"n_events_5_100_cut_200_pt_TROTA", 8, 0, 8)
    histo_events_1_100_cut_200_pt_signal_TROTA = ROOT.TH1F("n_events_1_100_cut_200_pt_TROTA", f"n_events_1_100_cut_200_pt_TROTA", 8, 0, 8)
    histo_events_1_1000_cut_200_pt_signal_TROTA = ROOT.TH1F("n_events_1_1000_cut_200_pt_TROTA", f"n_events_1_1000_cut_200_pt_TROTA", 8, 0, 8)

    # Processing and filling histograms
    for w in wanted_components:
        if histo_dict[w][key][f"h_event_counter_pre_{key}"].Integral() > 0:
            histo_norm_1 = prepare_histogram(histo_dict[w][key][f"h_event_counter_pre_{key}"].Clone(), num_bins, x_min, x_max)
            histo_norm_1.Scale(normalizations[w])
            histo_events_pre_signal[key].Add(histo_norm_1)

            histo_norm_1 = prepare_histogram(histo_dict[w][key][f"h_event_counter_post_{key}"].Clone(), num_bins, x_min, x_max)
            histo_norm_2.Scale(normalizations[w])
            histo_events_post_signal[key].Add(histo_norm_2)

            histo_norm_3 = prepare_histogram(histo_dict[w][key][f"h_event_counter_5_100_cut_200_pt_{key}"].Clone(), num_bins, x_min, x_max)
            histo_norm_3.Scale(normalizations[w])
            histo_events_5_100_cut_200_pt_signal[key].Add(histo_norm_3)
            
            if "200_pt"in key:
                print(key,200)
                histo_norm_4 = prepare_histogram(histo_dict[w]["20_TROTA_200_pt"]["h_event_counter_5_100_cut_200_pt_20_TROTA_200_pt"].Clone(), num_bins, x_min, x_max)
            elif "300_pt"in key:
                print(key,300)
                histo_norm_4 = prepare_histogram(histo_dict[w]["20_TROTA_300_pt"]["h_event_counter_5_100_cut_200_pt_20_TROTA_300_pt"].Clone(), num_bins, x_min, x_max)
            else:
                print(key,0)
                histo_norm_4 = prepare_histogram(histo_dict[w]["20_TROTA"]["h_event_counter_5_100_cut_200_pt_20_TROTA"].Clone(), num_bins, x_min, x_max)
            source_bin_4 = 3
            target_bin_4 = 4
            source_content_4 = histo_norm_4.GetBinContent(source_bin_4)
            target_content_4 = histo_norm_4.GetBinContent(target_bin_4)
            histo_norm_4.SetBinContent(target_bin_4, target_content_4 + source_content_4)
            histo_norm_4.SetBinContent(source_bin_4, 0)
            histo_norm_4.Scale(normalizations[w])
            histo_events_5_100_cut_200_pt_signal_TROTA.Add(histo_norm_4)

            histo_norm_5 = prepare_histogram(histo_dict[w][key][f"h_event_counter_1_100_cut_200_pt_{key}"].Clone(), num_bins, x_min, x_max)
            source_bin_5 = 4
            target_bin_5 = 5
            source_content_5 = histo_norm_5.GetBinContent(source_bin_5)
            target_content_5 = histo_norm_5.GetBinContent(target_bin_5)
            histo_norm_5.SetBinContent(target_bin_5, target_content_5 + source_content_5)
            histo_norm_5.SetBinContent(source_bin_5, 0)
            histo_norm_5.Scale(normalizations[w])
            histo_events_1_100_cut_200_pt_signal[key].Add(histo_norm_5)
            
            if "200_pt"in key:
                histo_norm_6 = prepare_histogram(histo_dict[w]["20_TROTA_200_pt"]["h_event_counter_1_100_cut_200_pt_20_TROTA_200_pt"].Clone(), num_bins, x_min, x_max)
            elif "300_pt"in key:
                histo_norm_6 = prepare_histogram(histo_dict[w]["20_TROTA_300_pt"]["h_event_counter_1_100_cut_200_pt_20_TROTA_300_pt"].Clone(), num_bins, x_min, x_max)
            else:
                histo_norm_6 = prepare_histogram(histo_dict[w]["20_TROTA"]["h_event_counter_1_100_cut_200_pt_20_TROTA"].Clone(), num_bins, x_min, x_max)
            source_bin_6 = 4
            target_bin_6 = 6
            source_content_6 = histo_norm_6.GetBinContent(source_bin_6)
            target_content_6 = histo_norm_6.GetBinContent(target_bin_6)
            histo_norm_6.SetBinContent(target_bin_6, target_content_6 + source_content_6)
            histo_norm_6.SetBinContent(source_bin_6, 0)
            histo_norm_6.Scale(normalizations[w])
            histo_events_1_100_cut_200_pt_signal_TROTA.Add(histo_norm_6)

            histo_norm_7 = prepare_histogram(histo_dict[w][key][f"h_event_counter_1_1000_cut_200_pt_{key}"].Clone(), num_bins, x_min, x_max)
            source_bin_7 = 5
            target_bin_7 = 7
            source_content_7 = histo_norm_7.GetBinContent(source_bin_7)
            target_content_7 = histo_norm_7.GetBinContent(target_bin_7)
            histo_norm_7.SetBinContent(target_bin_7, target_content_7 + source_content_7)
            histo_norm_7.SetBinContent(source_bin_7, 0)
            histo_norm_7.Scale(normalizations[w])
            histo_events_1_1000_cut_200_pt_signal[key].Add(histo_norm_7)
            
            if "200_pt"in key:
                histo_norm_8 = prepare_histogram(histo_dict[w]["20_TROTA_200_pt"]["h_event_counter_1_1000_cut_200_pt_20_TROTA_200_pt"].Clone(), num_bins, x_min, x_max)
            elif "300_pt"in key:
                histo_norm_8 = prepare_histogram(histo_dict[w]["20_TROTA_300_pt"]["h_event_counter_1_1000_cut_200_pt_20_TROTA_300_pt"].Clone(), num_bins, x_min, x_max)
            else:
                histo_norm_8 = prepare_histogram(histo_dict[w]["20_TROTA"]["h_event_counter_1_1000_cut_200_pt_20_TROTA"].Clone(), num_bins, x_min, x_max)
            source_bin_8 = 5
            target_bin_8 = 8
            source_content_8 = histo_norm_8.GetBinContent(source_bin_8)
            target_content_8 = histo_norm_8.GetBinContent(target_bin_8)
            histo_norm_8.SetBinContent(target_bin_8, target_content_8 + source_content_8)
            histo_norm_8.SetBinContent(source_bin_8, 0)
            histo_norm_8.Scale(normalizations[w])
            histo_events_1_100_cut_200_pt_signal_TROTA.Add(histo_norm_8)

        else:
            print(f"histo {key} for {w} is empty")

    # Drawing histograms
    histo_events_pre_signal[key].SetTitle(f"Signal events after cuts for {key}")
    histo_events_pre_signal[key].GetXaxis().SetRangeUser(0, 8)

    histo_events_pre_signal[key].GetYaxis().SetTitle("Normalized Events")
    histo_events_pre_signal[key].GetXaxis().SetBinLabel(1, "no selection")
    histo_events_pre_signal[key].GetXaxis().SetBinLabel(2, "preselection")
    histo_events_pre_signal[key].GetXaxis().SetBinLabel(3, f"5% {key}")
    histo_events_pre_signal[key].GetXaxis().SetBinLabel(4, f"5% TROTA")
    histo_events_pre_signal[key].GetXaxis().SetBinLabel(5, f"1% {key}")
    histo_events_pre_signal[key].GetXaxis().SetBinLabel(6, f"1% TROTA")
    histo_events_pre_signal[key].GetXaxis().SetBinLabel(7, f"0.1% {key}")
    histo_events_pre_signal[key].GetXaxis().SetBinLabel(8, f"0.1% TROTA")

    # Draw all histograms for the current key
    histo_events_pre_signal[key].Draw("histo")
    histo_events_post_signal[key].Draw("histosame")
    histo_events_5_100_cut_200_pt_signal[key].Draw("histosame")
    histo_events_1_100_cut_200_pt_signal[key].Draw("histosame")
    histo_events_1_1000_cut_200_pt_signal[key].Draw("histosame")
    histo_events_5_100_cut_200_pt_signal_TROTA.Draw("histosame")
    histo_events_1_100_cut_200_pt_signal_TROTA.Draw("histosame")
    histo_events_1_1000_cut_200_pt_signal_TROTA.Draw("histosame")

    # Enable log scale and draw the canvas
    c.SetLogy()
    c.Draw()
    c.SaveAs(f"{path_to_graphic_folder}signal_cuts/signal_events_{key}_cut_200_pt.pdf")

    # Reset all histograms for the current key before moving to the next key
    histo_events_pre_signal[key].Reset()
    histo_events_post_signal[key].Reset()
    histo_events_5_100_cut_200_pt_signal[key].Reset()
    histo_events_1_100_cut_200_pt_signal[key].Reset()
    histo_events_1_1000_cut_200_pt_signal[key].Reset()
    histo_events_5_100_cut_200_pt_signal_TROTA.Reset()
    histo_events_1_100_cut_200_pt_signal_TROTA.Reset()
    histo_events_1_1000_cut_200_pt_signal_TROTA.Reset()


# Canvas setup
c = ROOT.TCanvas("c", "c", 600, 600)

# Initialize dictionaries for histograms
histo_events_pre_signal = {}
histo_events_post_signal = {}
histo_events_1_100_cut_300_pt_signal = {}
histo_events_1_1000_cut_300_pt_signal = {}
histo_events_5_100_cut_300_pt_signal = {}

# Loop over keys to create histograms for each
for key in keys:
    histo_events_pre_signal[key] = ROOT.TH1F(f"n_events_pre_{key}", f"n_events_pre_{key}", 8, 0, 8)
    histo_events_post_signal[key] = ROOT.TH1F(f"n_events_post_{key}", f"n_events_post_{key}", 8, 0, 8)
    histo_events_1_100_cut_300_pt_signal[key] = ROOT.TH1F(f"n_events_1_100_cut_300_pt_{key}", f"n_events_1_100_cut_300_pt_{key}", 8, 0, 8)
    histo_events_1_1000_cut_300_pt_signal[key] = ROOT.TH1F(f"n_events_1_1000_cut_300_pt_{key}", f"n_events_1_1000_cut_300_pt_{key}", 8, 0, 8)
    histo_events_5_100_cut_300_pt_signal[key] = ROOT.TH1F(f"n_events_5_100_cut_300_pt_{key}", f"n_events_5_100_cut_300_pt_{key}", 8, 0, 8)
    histo_events_5_100_cut_300_pt_signal_TROTA = ROOT.TH1F("n_events_5_100_cut_300_pt_TROTA", f"n_events_5_100_cut_300_pt_TROTA", 8, 0, 8)
    histo_events_1_100_cut_300_pt_signal_TROTA = ROOT.TH1F("n_events_1_100_cut_300_pt_TROTA", f"n_events_1_100_cut_300_pt_TROTA", 8, 0, 8)
    histo_events_1_1000_cut_300_pt_signal_TROTA = ROOT.TH1F("n_events_1_1000_cut_300_pt_TROTA", f"n_events_1_1000_cut_300_pt_TROTA", 8, 0, 8)

    # Processing and filling histograms
    for w in wanted_components:
        if histo_dict[w][key][f"h_event_counter_pre_{key}"].Integral() > 0:
            histo_norm_1 = prepare_histogram(histo_dict[w][key][f"h_event_counter_pre_{key}"].Clone(), num_bins, x_min, x_max)
            histo_norm_1.Scale(normalizations[w])
            histo_events_pre_signal[key].Add(histo_norm_1)

            histo_norm_1 = prepare_histogram(histo_dict[w][key][f"h_event_counter_post_{key}"].Clone(), num_bins, x_min, x_max)
            histo_norm_2.Scale(normalizations[w])
            histo_events_post_signal[key].Add(histo_norm_2)

            histo_norm_3 = prepare_histogram(histo_dict[w][key][f"h_event_counter_5_100_cut_300_pt_{key}"].Clone(), num_bins, x_min, x_max)
            histo_norm_3.Scale(normalizations[w])
            histo_events_5_100_cut_300_pt_signal[key].Add(histo_norm_3)
            
            if "200_pt"in key:
                histo_norm_4 = prepare_histogram(histo_dict[w]["20_TROTA_200_pt"]["h_event_counter_5_100_cut_300_pt_20_TROTA_200_pt"].Clone(), num_bins, x_min, x_max)
            elif "300_pt"in key:
                histo_norm_4 = prepare_histogram(histo_dict[w]["20_TROTA_300_pt"]["h_event_counter_5_100_cut_300_pt_20_TROTA_300_pt"].Clone(), num_bins, x_min, x_max)
            else:
                histo_norm_4 = prepare_histogram(histo_dict[w]["20_TROTA"]["h_event_counter_5_100_cut_300_pt_20_TROTA"].Clone(), num_bins, x_min, x_max)
            source_bin_4 = 3
            target_bin_4 = 4
            source_content_4 = histo_norm_4.GetBinContent(source_bin_4)
            target_content_4 = histo_norm_4.GetBinContent(target_bin_4)
            histo_norm_4.SetBinContent(target_bin_4, target_content_4 + source_content_4)
            histo_norm_4.SetBinContent(source_bin_4, 0)
            histo_norm_4.Scale(normalizations[w])
            histo_events_5_100_cut_300_pt_signal_TROTA.Add(histo_norm_4)

            histo_norm_5 = prepare_histogram(histo_dict[w][key][f"h_event_counter_1_100_cut_300_pt_{key}"].Clone(), num_bins, x_min, x_max)
            source_bin_5 = 4
            target_bin_5 = 5
            source_content_5 = histo_norm_5.GetBinContent(source_bin_5)
            target_content_5 = histo_norm_5.GetBinContent(target_bin_5)
            histo_norm_5.SetBinContent(target_bin_5, target_content_5 + source_content_5)
            histo_norm_5.SetBinContent(source_bin_5, 0)
            histo_norm_5.Scale(normalizations[w])
            histo_events_1_100_cut_300_pt_signal[key].Add(histo_norm_5)
            
            if "200_pt"in key:
                histo_norm_6 = prepare_histogram(histo_dict[w]["20_TROTA_200_pt"]["h_event_counter_1_100_cut_300_pt_20_TROTA_200_pt"].Clone(), num_bins, x_min, x_max)
            elif "300_pt"in key:
                histo_norm_6 = prepare_histogram(histo_dict[w]["20_TROTA_300_pt"]["h_event_counter_1_100_cut_300_pt_20_TROTA_300_pt"].Clone(), num_bins, x_min, x_max)
            else:
                histo_norm_6 = prepare_histogram(histo_dict[w]["20_TROTA"]["h_event_counter_1_100_cut_300_pt_20_TROTA"].Clone(), num_bins, x_min, x_max)
            source_bin_6 = 4
            target_bin_6 = 6
            source_content_6 = histo_norm_6.GetBinContent(source_bin_6)
            target_content_6 = histo_norm_6.GetBinContent(target_bin_6)
            histo_norm_6.SetBinContent(target_bin_6, target_content_6 + source_content_6)
            histo_norm_6.SetBinContent(source_bin_6, 0)
            histo_norm_6.Scale(normalizations[w])
            histo_events_1_100_cut_300_pt_signal_TROTA.Add(histo_norm_6)

            histo_norm_7 = prepare_histogram(histo_dict[w][key][f"h_event_counter_1_1000_cut_300_pt_{key}"].Clone(), num_bins, x_min, x_max)
            source_bin_7 = 5
            target_bin_7 = 7
            source_content_7 = histo_norm_7.GetBinContent(source_bin_7)
            target_content_7 = histo_norm_7.GetBinContent(target_bin_7)
            histo_norm_7.SetBinContent(target_bin_7, target_content_7 + source_content_7)
            histo_norm_7.SetBinContent(source_bin_7, 0)
            histo_norm_7.Scale(normalizations[w])
            histo_events_1_1000_cut_300_pt_signal[key].Add(histo_norm_7)
            
            if "200_pt"in key:
                histo_norm_8 = prepare_histogram(histo_dict[w]["20_TROTA_200_pt"]["h_event_counter_1_1000_cut_300_pt_20_TROTA_200_pt"].Clone(), num_bins, x_min, x_max)
            elif "300_pt"in key:
                histo_norm_8 = prepare_histogram(histo_dict[w]["20_TROTA_300_pt"]["h_event_counter_1_1000_cut_300_pt_20_TROTA_300_pt"].Clone(), num_bins, x_min, x_max)
            else:
                histo_norm_8 = prepare_histogram(histo_dict[w]["20_TROTA"]["h_event_counter_1_1000_cut_300_pt_20_TROTA"].Clone(), num_bins, x_min, x_max)
            source_bin_8 = 5
            target_bin_8 = 8
            source_content_8 = histo_norm_8.GetBinContent(source_bin_8)
            target_content_8 = histo_norm_8.GetBinContent(target_bin_8)
            histo_norm_8.SetBinContent(target_bin_8, target_content_8 + source_content_8)
            histo_norm_8.SetBinContent(source_bin_8, 0)
            histo_norm_8.Scale(normalizations[w])
            histo_events_1_100_cut_300_pt_signal_TROTA.Add(histo_norm_8)

        else:
            print(f"histo {key} for {w} is empty")

    # Drawing histograms
    histo_events_pre_signal[key].SetTitle(f"Signal events after cuts for {key}")
    histo_events_pre_signal[key].GetXaxis().SetRangeUser(0, 8)

    histo_events_pre_signal[key].GetYaxis().SetTitle("Normalized Events")
    histo_events_pre_signal[key].GetXaxis().SetBinLabel(1, "no selection")
    histo_events_pre_signal[key].GetXaxis().SetBinLabel(2, "preselection")
    histo_events_pre_signal[key].GetXaxis().SetBinLabel(3, f"5% {key}")
    histo_events_pre_signal[key].GetXaxis().SetBinLabel(4, f"5% TROTA")
    histo_events_pre_signal[key].GetXaxis().SetBinLabel(5, f"1% {key}")
    histo_events_pre_signal[key].GetXaxis().SetBinLabel(6, f"1% TROTA")
    histo_events_pre_signal[key].GetXaxis().SetBinLabel(7, f"0.1% {key}")
    histo_events_pre_signal[key].GetXaxis().SetBinLabel(8, f"0.1% TROTA")

    # Draw all histograms for the current key
    histo_events_pre_signal[key].Draw("histo")
    histo_events_post_signal[key].Draw("histosame")
    histo_events_5_100_cut_300_pt_signal[key].Draw("histosame")
    histo_events_1_100_cut_300_pt_signal[key].Draw("histosame")
    histo_events_1_1000_cut_300_pt_signal[key].Draw("histosame")
    histo_events_5_100_cut_300_pt_signal_TROTA.Draw("histosame")
    histo_events_1_100_cut_300_pt_signal_TROTA.Draw("histosame")
    histo_events_1_1000_cut_300_pt_signal_TROTA.Draw("histosame")

    # Enable log scale and draw the canvas
    c.SetLogy()
    c.Draw()
    c.SaveAs(f"{path_to_graphic_folder}signal_cuts/signal_events_{key}_cut_300_pt.pdf")

    # Reset all histograms for the current key before moving to the next key
    histo_events_pre_signal[key].Reset()
    histo_events_post_signal[key].Reset()
    histo_events_5_100_cut_300_pt_signal[key].Reset()
    histo_events_1_100_cut_300_pt_signal[key].Reset()
    histo_events_1_1000_cut_300_pt_signal[key].Reset()
    histo_events_5_100_cut_300_pt_signal_TROTA.Reset()
    histo_events_1_100_cut_300_pt_signal_TROTA.Reset()
    histo_events_1_1000_cut_300_pt_signal_TROTA.Reset()


wanted_components = ["QCD_HT1000to1200_2022","QCD_HT1200to1500_2022","QCD_HT1500to2000_2022"]
# Canvas setup
c = ROOT.TCanvas("c", "c", 600, 600)

# Initialize dictionaries for histograms
histo_events_pre_background = {}
histo_events_post_background = {}
histo_events_1_100_background = {}
histo_events_1_1000_background = {}
histo_events_5_100_background = {}

# Loop over keys to create histograms for each
for key in keys:
    histo_events_pre_background[key] = ROOT.TH1F(f"n_events_pre_{key}", f"n_events_pre_{key}", 8, 0, 8)
    histo_events_post_background[key] = ROOT.TH1F(f"n_events_post_{key}", f"n_events_post_{key}", 8, 0, 8)
    histo_events_1_100_background[key] = ROOT.TH1F(f"n_events_1_100_{key}", f"n_events_1_100_{key}", 8, 0, 8)
    histo_events_1_1000_background[key] = ROOT.TH1F(f"n_events_1_1000_{key}", f"n_events_1_1000_{key}", 8, 0, 8)
    histo_events_5_100_background[key] = ROOT.TH1F(f"n_events_5_100_{key}", f"n_events_5_100_{key}", 8, 0, 8)
    histo_events_5_100_background_TROTA = ROOT.TH1F("n_events_5_100_TROTA", f"n_events_5_100_TROTA", 8, 0, 8)
    histo_events_1_100_background_TROTA = ROOT.TH1F("n_events_1_100_TROTA", f"n_events_1_100_TROTA", 8, 0, 8)
    histo_events_1_1000_background_TROTA = ROOT.TH1F("n_events_1_1000_TROTA", f"n_events_1_1000_TROTA", 8, 0, 8)

    # Processing and filling histograms
    for w in wanted_components:
        if histo_dict[w][key][f"h_event_counter_pre_{key}"].Integral() > 0:
            histo_norm_1 = prepare_histogram(histo_dict[w][key][f"h_event_counter_pre_{key}"].Clone(), num_bins, x_min, x_max)
            histo_norm_1.Scale(normalizations[w])
            histo_events_pre_background[key].Add(histo_norm_1)

            histo_norm_1 = prepare_histogram(histo_dict[w][key][f"h_event_counter_post_{key}"].Clone(), num_bins, x_min, x_max)
            histo_norm_2.Scale(normalizations[w])
            histo_events_post_background[key].Add(histo_norm_2)

            histo_norm_3 = prepare_histogram(histo_dict[w][key][f"h_event_counter_5_100_{key}"].Clone(), num_bins, x_min, x_max)
            histo_norm_3.Scale(normalizations[w])
            histo_events_5_100_background[key].Add(histo_norm_3)
            
            if "200_pt"in key:
                histo_norm_4 = prepare_histogram(histo_dict[w]["20_TROTA_200_pt"]["h_event_counter_5_100_20_TROTA_200_pt"].Clone(), num_bins, x_min, x_max)
            elif "300_pt"in key:
                histo_norm_4 = prepare_histogram(histo_dict[w]["20_TROTA_300_pt"]["h_event_counter_5_100_20_TROTA_300_pt"].Clone(), num_bins, x_min, x_max)
            else:
                histo_norm_4 = prepare_histogram(histo_dict[w]["20_TROTA"]["h_event_counter_5_100_20_TROTA"].Clone(), num_bins, x_min, x_max)
            source_bin_4 = 3
            target_bin_4 = 4
            source_content_4 = histo_norm_4.GetBinContent(source_bin_4)
            target_content_4 = histo_norm_4.GetBinContent(target_bin_4)
            histo_norm_4.SetBinContent(target_bin_4, target_content_4 + source_content_4)
            histo_norm_4.SetBinContent(source_bin_4, 0)
            histo_norm_4.Scale(normalizations[w])
            histo_events_5_100_background_TROTA.Add(histo_norm_4)

            histo_norm_5 = prepare_histogram(histo_dict[w][key][f"h_event_counter_1_100_{key}"].Clone(), num_bins, x_min, x_max)
            source_bin_5 = 4
            target_bin_5 = 5
            source_content_5 = histo_norm_5.GetBinContent(source_bin_5)
            target_content_5 = histo_norm_5.GetBinContent(target_bin_5)
            histo_norm_5.SetBinContent(target_bin_5, target_content_5 + source_content_5)
            histo_norm_5.SetBinContent(source_bin_5, 0)
            histo_norm_5.Scale(normalizations[w])
            histo_events_1_100_background[key].Add(histo_norm_5)
            
            if "200_pt"in key:
                histo_norm_6 = prepare_histogram(histo_dict[w]["20_TROTA_200_pt"]["h_event_counter_1_100_20_TROTA_200_pt"].Clone(), num_bins, x_min, x_max)
            elif "300_pt"in key:
                histo_norm_6 = prepare_histogram(histo_dict[w]["20_TROTA_300_pt"]["h_event_counter_1_100_20_TROTA_300_pt"].Clone(), num_bins, x_min, x_max)
            else:
                histo_norm_6 = prepare_histogram(histo_dict[w]["20_TROTA"]["h_event_counter_1_100_20_TROTA"].Clone(), num_bins, x_min, x_max)
            source_bin_6 = 4
            target_bin_6 = 6
            source_content_6 = histo_norm_6.GetBinContent(source_bin_6)
            target_content_6 = histo_norm_6.GetBinContent(target_bin_6)
            histo_norm_6.SetBinContent(target_bin_6, target_content_6 + source_content_6)
            histo_norm_6.SetBinContent(source_bin_6, 0)
            histo_norm_6.Scale(normalizations[w])
            histo_events_1_100_background_TROTA.Add(histo_norm_6)

            histo_norm_7 = prepare_histogram(histo_dict[w][key][f"h_event_counter_1_1000_{key}"].Clone(), num_bins, x_min, x_max)
            source_bin_7 = 5
            target_bin_7 = 7
            source_content_7 = histo_norm_7.GetBinContent(source_bin_7)
            target_content_7 = histo_norm_7.GetBinContent(target_bin_7)
            histo_norm_7.SetBinContent(target_bin_7, target_content_7 + source_content_7)
            histo_norm_7.SetBinContent(source_bin_7, 0)
            histo_norm_7.Scale(normalizations[w])
            histo_events_1_1000_background[key].Add(histo_norm_7)
            
            if "200_pt"in key:
                histo_norm_8 = prepare_histogram(histo_dict[w]["20_TROTA_200_pt"]["h_event_counter_1_1000_20_TROTA_200_pt"].Clone(), num_bins, x_min, x_max)
            elif "300_pt"in key:
                histo_norm_8 = prepare_histogram(histo_dict[w]["20_TROTA_300_pt"]["h_event_counter_1_1000_20_TROTA_300_pt"].Clone(), num_bins, x_min, x_max)
            else:
                histo_norm_8 = prepare_histogram(histo_dict[w]["20_TROTA"]["h_event_counter_1_1000_20_TROTA"].Clone(), num_bins, x_min, x_max)
            source_bin_8 = 5
            target_bin_8 = 8
            source_content_8 = histo_norm_8.GetBinContent(source_bin_8)
            target_content_8 = histo_norm_8.GetBinContent(target_bin_8)
            histo_norm_8.SetBinContent(target_bin_8, target_content_8 + source_content_8)
            histo_norm_8.SetBinContent(source_bin_8, 0)
            histo_norm_8.Scale(normalizations[w])
            histo_events_1_100_background_TROTA.Add(histo_norm_8)

        else:
            print(f"histo {key} for {w} is empty")

    # Drawing histograms
    histo_events_pre_background[key].SetTitle(f"background events after cuts for {key}")
    histo_events_pre_background[key].GetXaxis().SetRangeUser(0, 8)
    #histo_events_pre_background[key].Getyaxis().SetRangeUser(0.0001, 8)
    histo_events_pre_background[key].GetYaxis().SetTitle("Normalized Events")
    histo_events_pre_background[key].GetXaxis().SetBinLabel(1, "no selection")
    histo_events_pre_background[key].GetXaxis().SetBinLabel(2, "preselection")
    histo_events_pre_background[key].GetXaxis().SetBinLabel(3, f"5% {key}")
    histo_events_pre_background[key].GetXaxis().SetBinLabel(4, f"5% TROTA")
    histo_events_pre_background[key].GetXaxis().SetBinLabel(5, f"1% {key}")
    histo_events_pre_background[key].GetXaxis().SetBinLabel(6, f"1% TROTA")
    histo_events_pre_background[key].GetXaxis().SetBinLabel(7, f"0.1% {key}")
    histo_events_pre_background[key].GetXaxis().SetBinLabel(8, f"0.1% TROTA")

    # Draw all histograms for the current key
    histo_events_pre_background[key].Draw("histo")
    histo_events_post_background[key].Draw("histosame")
    histo_events_5_100_background[key].Draw("histosame")
    histo_events_1_100_background[key].Draw("histosame")
    histo_events_1_1000_background[key].Draw("histosame")
    histo_events_5_100_background_TROTA.Draw("histosame")
    histo_events_1_100_background_TROTA.Draw("histosame")
    histo_events_1_1000_background_TROTA.Draw("histosame")

    # Enable log scale and draw the canvas
    c.SetLogy()
    c.Draw()
    c.SaveAs(f"{path_to_graphic_folder}background_cuts/background_events_{key}.pdf")

    # Reset all histograms for the current key before moving to the next key
    histo_events_pre_background[key].Reset()
    histo_events_post_background[key].Reset()
    histo_events_5_100_background[key].Reset()
    histo_events_1_100_background[key].Reset()
    histo_events_1_1000_background[key].Reset()
    histo_events_5_100_background_TROTA.Reset()
    histo_events_1_100_background_TROTA.Reset()
    histo_events_1_1000_background_TROTA.Reset()

# Canvas setup
c = ROOT.TCanvas("c", "c", 600, 600)

# Initialize dictionaries for histograms
histo_events_pre_background = {}
histo_events_post_background = {}
histo_events_1_100_cut_200_pt_background = {}
histo_events_1_1000_cut_200_pt_background = {}
histo_events_5_100_cut_200_pt_background = {}

# Loop over keys to create histograms for each
for key in keys:
    histo_events_pre_background[key] = ROOT.TH1F(f"n_events_pre_{key}", f"n_events_pre_{key}", 8, 0, 8)
    histo_events_post_background[key] = ROOT.TH1F(f"n_events_post_{key}", f"n_events_post_{key}", 8, 0, 8)
    histo_events_1_100_cut_200_pt_background[key] = ROOT.TH1F(f"n_events_1_100_cut_200_pt_{key}", f"n_events_1_100_cut_200_pt_{key}", 8, 0, 8)
    histo_events_1_1000_cut_200_pt_background[key] = ROOT.TH1F(f"n_events_1_1000_cut_200_pt_{key}", f"n_events_1_1000_cut_200_pt_{key}", 8, 0, 8)
    histo_events_5_100_cut_200_pt_background[key] = ROOT.TH1F(f"n_events_5_100_cut_200_pt_{key}", f"n_events_5_100_cut_200_pt_{key}", 8, 0, 8)
    histo_events_5_100_cut_200_pt_background_TROTA = ROOT.TH1F("n_events_5_100_cut_200_pt_TROTA", f"n_events_5_100_cut_200_pt_TROTA", 8, 0, 8)
    histo_events_1_100_cut_200_pt_background_TROTA = ROOT.TH1F("n_events_1_100_cut_200_pt_TROTA", f"n_events_1_100_cut_200_pt_TROTA", 8, 0, 8)
    histo_events_1_1000_cut_200_pt_background_TROTA = ROOT.TH1F("n_events_1_1000_cut_200_pt_TROTA", f"n_events_1_1000_cut_200_pt_TROTA", 8, 0, 8)

    # Processing and filling histograms
    for w in wanted_components:
        if histo_dict[w][key][f"h_event_counter_pre_{key}"].Integral() > 0:
            histo_norm_1 = prepare_histogram(histo_dict[w][key][f"h_event_counter_pre_{key}"].Clone(), num_bins, x_min, x_max)
            histo_norm_1.Scale(normalizations[w])
            histo_events_pre_background[key].Add(histo_norm_1)

            histo_norm_1 = prepare_histogram(histo_dict[w][key][f"h_event_counter_post_{key}"].Clone(), num_bins, x_min, x_max)
            histo_norm_2.Scale(normalizations[w])
            histo_events_post_background[key].Add(histo_norm_2)

            histo_norm_3 = prepare_histogram(histo_dict[w][key][f"h_event_counter_5_100_cut_200_pt_{key}"].Clone(), num_bins, x_min, x_max)
            histo_norm_3.Scale(normalizations[w])
            histo_events_5_100_cut_200_pt_background[key].Add(histo_norm_3)
            
            if "200_pt"in key:
                histo_norm_4 = prepare_histogram(histo_dict[w]["20_TROTA_200_pt"]["h_event_counter_5_100_cut_200_pt_20_TROTA_200_pt"].Clone(), num_bins, x_min, x_max)
            elif "300_pt"in key:
                histo_norm_4 = prepare_histogram(histo_dict[w]["20_TROTA_300_pt"]["h_event_counter_5_100_cut_200_pt_20_TROTA_300_pt"].Clone(), num_bins, x_min, x_max)
            else:
                histo_norm_4 = prepare_histogram(histo_dict[w]["20_TROTA"]["h_event_counter_5_100_cut_200_pt_20_TROTA"].Clone(), num_bins, x_min, x_max)
            source_bin_4 = 3
            target_bin_4 = 4
            source_content_4 = histo_norm_4.GetBinContent(source_bin_4)
            target_content_4 = histo_norm_4.GetBinContent(target_bin_4)
            histo_norm_4.SetBinContent(target_bin_4, target_content_4 + source_content_4)
            histo_norm_4.SetBinContent(source_bin_4, 0)
            histo_norm_4.Scale(normalizations[w])
            histo_events_5_100_cut_200_pt_background_TROTA.Add(histo_norm_4)

            histo_norm_5 = prepare_histogram(histo_dict[w][key][f"h_event_counter_1_100_cut_200_pt_{key}"].Clone(), num_bins, x_min, x_max)
            source_bin_5 = 4
            target_bin_5 = 5
            source_content_5 = histo_norm_5.GetBinContent(source_bin_5)
            target_content_5 = histo_norm_5.GetBinContent(target_bin_5)
            histo_norm_5.SetBinContent(target_bin_5, target_content_5 + source_content_5)
            histo_norm_5.SetBinContent(source_bin_5, 0)
            histo_norm_5.Scale(normalizations[w])
            histo_events_1_100_cut_200_pt_background[key].Add(histo_norm_5)
            
            if "200_pt"in key:
                histo_norm_6 = prepare_histogram(histo_dict[w]["20_TROTA_200_pt"]["h_event_counter_1_100_cut_200_pt_20_TROTA_200_pt"].Clone(), num_bins, x_min, x_max)
            elif "300_pt"in key:
                histo_norm_6 = prepare_histogram(histo_dict[w]["20_TROTA_300_pt"]["h_event_counter_1_100_cut_200_pt_20_TROTA_300_pt"].Clone(), num_bins, x_min, x_max)
            else:
                histo_norm_6 = prepare_histogram(histo_dict[w]["20_TROTA"]["h_event_counter_1_100_cut_200_pt_20_TROTA"].Clone(), num_bins, x_min, x_max)
            source_bin_6 = 4
            target_bin_6 = 6
            source_content_6 = histo_norm_6.GetBinContent(source_bin_6)
            target_content_6 = histo_norm_6.GetBinContent(target_bin_6)
            histo_norm_6.SetBinContent(target_bin_6, target_content_6 + source_content_6)
            histo_norm_6.SetBinContent(source_bin_6, 0)
            histo_norm_6.Scale(normalizations[w])
            histo_events_1_100_cut_200_pt_background_TROTA.Add(histo_norm_6)

            histo_norm_7 = prepare_histogram(histo_dict[w][key][f"h_event_counter_1_1000_cut_200_pt_{key}"].Clone(), num_bins, x_min, x_max)
            source_bin_7 = 5
            target_bin_7 = 7
            source_content_7 = histo_norm_7.GetBinContent(source_bin_7)
            target_content_7 = histo_norm_7.GetBinContent(target_bin_7)
            histo_norm_7.SetBinContent(target_bin_7, target_content_7 + source_content_7)
            histo_norm_7.SetBinContent(source_bin_7, 0)
            histo_norm_7.Scale(normalizations[w])
            histo_events_1_1000_cut_200_pt_background[key].Add(histo_norm_7)
            
            if "200_pt"in key:
                histo_norm_8 = prepare_histogram(histo_dict[w]["20_TROTA_200_pt"]["h_event_counter_1_1000_cut_200_pt_20_TROTA_200_pt"].Clone(), num_bins, x_min, x_max)
            elif "300_pt"in key:
                histo_norm_8 = prepare_histogram(histo_dict[w]["20_TROTA_300_pt"]["h_event_counter_1_1000_cut_200_pt_20_TROTA_300_pt"].Clone(), num_bins, x_min, x_max)
            else:
                histo_norm_8 = prepare_histogram(histo_dict[w]["20_TROTA"]["h_event_counter_1_1000_cut_200_pt_20_TROTA"].Clone(), num_bins, x_min, x_max)
            source_bin_8 = 5
            target_bin_8 = 8
            source_content_8 = histo_norm_8.GetBinContent(source_bin_8)
            target_content_8 = histo_norm_8.GetBinContent(target_bin_8)
            histo_norm_8.SetBinContent(target_bin_8, target_content_8 + source_content_8)
            histo_norm_8.SetBinContent(source_bin_8, 0)
            histo_norm_8.Scale(normalizations[w])
            histo_events_1_100_cut_200_pt_background_TROTA.Add(histo_norm_8)

        else:
            print(f"histo {key} for {w} is empty")

    # Drawing histograms
    histo_events_pre_background[key].SetTitle(f"background events after cuts for {key}")
    histo_events_pre_background[key].GetXaxis().SetRangeUser(0, 8)

    histo_events_pre_background[key].GetYaxis().SetTitle("Normalized Events")
    histo_events_pre_background[key].GetXaxis().SetBinLabel(1, "no selection")
    histo_events_pre_background[key].GetXaxis().SetBinLabel(2, "preselection")
    histo_events_pre_background[key].GetXaxis().SetBinLabel(3, f"5% {key}")
    histo_events_pre_background[key].GetXaxis().SetBinLabel(4, f"5% TROTA")
    histo_events_pre_background[key].GetXaxis().SetBinLabel(5, f"1% {key}")
    histo_events_pre_background[key].GetXaxis().SetBinLabel(6, f"1% TROTA")
    histo_events_pre_background[key].GetXaxis().SetBinLabel(7, f"0.1% {key}")
    histo_events_pre_background[key].GetXaxis().SetBinLabel(8, f"0.1% TROTA")

    # Draw all histograms for the current key
    histo_events_pre_background[key].Draw("histo")
    histo_events_post_background[key].Draw("histosame")
    histo_events_5_100_cut_200_pt_background[key].Draw("histosame")
    histo_events_1_100_cut_200_pt_background[key].Draw("histosame")
    histo_events_1_1000_cut_200_pt_background[key].Draw("histosame")
    histo_events_5_100_cut_200_pt_background_TROTA.Draw("histosame")
    histo_events_1_100_cut_200_pt_background_TROTA.Draw("histosame")
    histo_events_1_1000_cut_200_pt_background_TROTA.Draw("histosame")

    # Enable log scale and draw the canvas
    c.SetLogy()
    c.Draw()
    c.SaveAs(f"{path_to_graphic_folder}background_cuts/background_events_{key}_cut_200_pt.pdf")

    # Reset all histograms for the current key before moving to the next key
    histo_events_pre_background[key].Reset()
    histo_events_post_background[key].Reset()
    histo_events_5_100_cut_200_pt_background[key].Reset()
    histo_events_1_100_cut_200_pt_background[key].Reset()
    histo_events_1_1000_cut_200_pt_background[key].Reset()
    histo_events_5_100_cut_200_pt_background_TROTA.Reset()
    histo_events_1_100_cut_200_pt_background_TROTA.Reset()
    histo_events_1_1000_cut_200_pt_background_TROTA.Reset()

# Canvas setup
c = ROOT.TCanvas("c", "c", 600, 600)

# Initialize dictionaries for histograms
histo_events_pre_background = {}
histo_events_post_background = {}
histo_events_1_100_cut_300_pt_background = {}
histo_events_1_1000_cut_300_pt_background = {}
histo_events_5_100_cut_300_pt_background = {}

# Loop over keys to create histograms for each
for key in keys:
    histo_events_pre_background[key] = ROOT.TH1F(f"n_events_pre_{key}", f"n_events_pre_{key}", 8, 0, 8)
    histo_events_post_background[key] = ROOT.TH1F(f"n_events_post_{key}", f"n_events_post_{key}", 8, 0, 8)
    histo_events_1_100_cut_300_pt_background[key] = ROOT.TH1F(f"n_events_1_100_cut_300_pt_{key}", f"n_events_1_100_cut_300_pt_{key}", 8, 0, 8)
    histo_events_1_1000_cut_300_pt_background[key] = ROOT.TH1F(f"n_events_1_1000_cut_300_pt_{key}", f"n_events_1_1000_cut_300_pt_{key}", 8, 0, 8)
    histo_events_5_100_cut_300_pt_background[key] = ROOT.TH1F(f"n_events_5_100_cut_300_pt_{key}", f"n_events_5_100_cut_300_pt_{key}", 8, 0, 8)
    histo_events_5_100_cut_300_pt_background_TROTA = ROOT.TH1F("n_events_5_100_cut_300_pt_TROTA", f"n_events_5_100_cut_300_pt_TROTA", 8, 0, 8)
    histo_events_1_100_cut_300_pt_background_TROTA = ROOT.TH1F("n_events_1_100_cut_300_pt_TROTA", f"n_events_1_100_cut_300_pt_TROTA", 8, 0, 8)
    histo_events_1_1000_cut_300_pt_background_TROTA = ROOT.TH1F("n_events_1_1000_cut_300_pt_TROTA", f"n_events_1_1000_cut_300_pt_TROTA", 8, 0, 8)

    # Processing and filling histograms
    for w in wanted_components:
        if histo_dict[w][key][f"h_event_counter_pre_{key}"].Integral() > 0:
            histo_norm_1 = prepare_histogram(histo_dict[w][key][f"h_event_counter_pre_{key}"].Clone(), num_bins, x_min, x_max)
            histo_norm_1.Scale(normalizations[w])
            histo_events_pre_background[key].Add(histo_norm_1)

            histo_norm_1 = prepare_histogram(histo_dict[w][key][f"h_event_counter_post_{key}"].Clone(), num_bins, x_min, x_max)
            histo_norm_2.Scale(normalizations[w])
            histo_events_post_background[key].Add(histo_norm_2)

            histo_norm_3 = prepare_histogram(histo_dict[w][key][f"h_event_counter_5_100_cut_300_pt_{key}"].Clone(), num_bins, x_min, x_max)
            histo_norm_3.Scale(normalizations[w])
            histo_events_5_100_cut_300_pt_background[key].Add(histo_norm_3)
            
            if "200_pt"in key:
                histo_norm_4 = prepare_histogram(histo_dict[w]["20_TROTA_200_pt"]["h_event_counter_5_100_cut_300_pt_20_TROTA_200_pt"].Clone(), num_bins, x_min, x_max)
            elif "300_pt"in key:
                histo_norm_4 = prepare_histogram(histo_dict[w]["20_TROTA_300_pt"]["h_event_counter_5_100_cut_300_pt_20_TROTA_300_pt"].Clone(), num_bins, x_min, x_max)
            else:
                histo_norm_4 = prepare_histogram(histo_dict[w]["20_TROTA"]["h_event_counter_5_100_cut_300_pt_20_TROTA"].Clone(), num_bins, x_min, x_max)
            source_bin_4 = 3
            target_bin_4 = 4
            source_content_4 = histo_norm_4.GetBinContent(source_bin_4)
            target_content_4 = histo_norm_4.GetBinContent(target_bin_4)
            histo_norm_4.SetBinContent(target_bin_4, target_content_4 + source_content_4)
            histo_norm_4.SetBinContent(source_bin_4, 0)
            histo_norm_4.Scale(normalizations[w])
            histo_events_5_100_cut_300_pt_background_TROTA.Add(histo_norm_4)

            histo_norm_5 = prepare_histogram(histo_dict[w][key][f"h_event_counter_1_100_cut_300_pt_{key}"].Clone(), num_bins, x_min, x_max)
            source_bin_5 = 4
            target_bin_5 = 5
            source_content_5 = histo_norm_5.GetBinContent(source_bin_5)
            target_content_5 = histo_norm_5.GetBinContent(target_bin_5)
            histo_norm_5.SetBinContent(target_bin_5, target_content_5 + source_content_5)
            histo_norm_5.SetBinContent(source_bin_5, 0)
            histo_norm_5.Scale(normalizations[w])
            histo_events_1_100_cut_300_pt_background[key].Add(histo_norm_5)
            
            if "200_pt"in key:
                histo_norm_6 = prepare_histogram(histo_dict[w]["20_TROTA_200_pt"]["h_event_counter_1_100_cut_300_pt_20_TROTA_200_pt"].Clone(), num_bins, x_min, x_max)
            elif "300_pt"in key:
                histo_norm_6 = prepare_histogram(histo_dict[w]["20_TROTA_300_pt"]["h_event_counter_1_100_cut_300_pt_20_TROTA_300_pt"].Clone(), num_bins, x_min, x_max)
            else:
                histo_norm_6 = prepare_histogram(histo_dict[w]["20_TROTA"]["h_event_counter_1_100_cut_300_pt_20_TROTA"].Clone(), num_bins, x_min, x_max)
            source_bin_6 = 4
            target_bin_6 = 6
            source_content_6 = histo_norm_6.GetBinContent(source_bin_6)
            target_content_6 = histo_norm_6.GetBinContent(target_bin_6)
            histo_norm_6.SetBinContent(target_bin_6, target_content_6 + source_content_6)
            histo_norm_6.SetBinContent(source_bin_6, 0)
            histo_norm_6.Scale(normalizations[w])
            histo_events_1_100_cut_300_pt_background_TROTA.Add(histo_norm_6)

            histo_norm_7 = prepare_histogram(histo_dict[w][key][f"h_event_counter_1_1000_cut_300_pt_{key}"].Clone(), num_bins, x_min, x_max)
            source_bin_7 = 5
            target_bin_7 = 7
            source_content_7 = histo_norm_7.GetBinContent(source_bin_7)
            target_content_7 = histo_norm_7.GetBinContent(target_bin_7)
            histo_norm_7.SetBinContent(target_bin_7, target_content_7 + source_content_7)
            histo_norm_7.SetBinContent(source_bin_7, 0)
            histo_norm_7.Scale(normalizations[w])
            histo_events_1_1000_cut_300_pt_background[key].Add(histo_norm_7)
            
            if "200_pt"in key:
                histo_norm_8 = prepare_histogram(histo_dict[w]["20_TROTA_200_pt"]["h_event_counter_1_1000_cut_300_pt_20_TROTA_200_pt"].Clone(), num_bins, x_min, x_max)
            elif "300_pt"in key:
                histo_norm_8 = prepare_histogram(histo_dict[w]["20_TROTA_300_pt"]["h_event_counter_1_1000_cut_300_pt_20_TROTA_300_pt"].Clone(), num_bins, x_min, x_max)
            else:
                histo_norm_8 = prepare_histogram(histo_dict[w]["20_TROTA"]["h_event_counter_1_1000_cut_300_pt_20_TROTA"].Clone(), num_bins, x_min, x_max)
            source_bin_8 = 5
            target_bin_8 = 8
            source_content_8 = histo_norm_8.GetBinContent(source_bin_8)
            target_content_8 = histo_norm_8.GetBinContent(target_bin_8)
            histo_norm_8.SetBinContent(target_bin_8, target_content_8 + source_content_8)
            histo_norm_8.SetBinContent(source_bin_8, 0)
            histo_norm_8.Scale(normalizations[w])
            histo_events_1_100_cut_300_pt_background_TROTA.Add(histo_norm_8)

        else:
            print(f"histo {key} for {w} is empty")

    # Drawing histograms
    histo_events_pre_background[key].SetTitle(f"background events after cuts for {key}")
    histo_events_pre_background[key].GetXaxis().SetRangeUser(0, 8)
    histo_events_pre_background[key].GetYaxis().SetTitle("Normalized Events")
    histo_events_pre_background[key].GetXaxis().SetBinLabel(1, "no selection")
    histo_events_pre_background[key].GetXaxis().SetBinLabel(2, "preselection")
    histo_events_pre_background[key].GetXaxis().SetBinLabel(3, f"5% {key}")
    histo_events_pre_background[key].GetXaxis().SetBinLabel(4, f"5% TROTA")
    histo_events_pre_background[key].GetXaxis().SetBinLabel(5, f"1% {key}")
    histo_events_pre_background[key].GetXaxis().SetBinLabel(6, f"1% TROTA")
    histo_events_pre_background[key].GetXaxis().SetBinLabel(7, f"0.1% {key}")
    histo_events_pre_background[key].GetXaxis().SetBinLabel(8, f"0.1% TROTA")

    # Draw all histograms for the current key
    histo_events_pre_background[key].Draw("histo")
    histo_events_post_background[key].Draw("histosame")
    histo_events_5_100_cut_300_pt_background[key].Draw("histosame")
    histo_events_1_100_cut_300_pt_background[key].Draw("histosame")
    histo_events_1_1000_cut_300_pt_background[key].Draw("histosame")
    histo_events_5_100_cut_300_pt_background_TROTA.Draw("histosame")
    histo_events_1_100_cut_300_pt_background_TROTA.Draw("histosame")
    histo_events_1_1000_cut_300_pt_background_TROTA.Draw("histosame")

    # Enable log scale and draw the canvas
    c.SetLogy()
    c.Draw()
    c.SaveAs(f"{path_to_graphic_folder}background_cuts/background_events_{key}_cut_200_pt.pdf")

    # Reset all histograms for the current key before moving to the next key
    histo_events_pre_background[key].Reset()
    histo_events_post_background[key].Reset()
    histo_events_5_100_cut_300_pt_background[key].Reset()
    histo_events_1_100_cut_300_pt_background[key].Reset()
    histo_events_1_1000_cut_300_pt_background[key].Reset()
    histo_events_5_100_cut_300_pt_background_TROTA.Reset()
    histo_events_1_100_cut_300_pt_background_TROTA.Reset()
    histo_events_1_1000_cut_300_pt_background_TROTA.Reset()


cuts=["","_cut_200_pt","_cut_300_pt"]
wanted_components = ["TT_semilep_2022","QCD_HT1000to1200_2022","QCD_HT1200to1500_2022","QCD_HT1500to2000_2022"]

ROOT.gStyle.SetOptStat(0)
h_score_mixed_true = {}
h_score_mixed_false_other = {}
h_score_mixed_false_QCD = {}
h_score_mixed_false_all = {}
# Loop over the components and keys in the dictionary
for key in keys:
    h_score_mixed_true[key] = {}
    h_score_mixed_false_other[key] = {}
    h_score_mixed_false_QCD[key] = {}
    h_score_mixed_false_all[key] = {}
    for cut in cuts:
        h_score_mixed_true[key][cut] = ROOT.TH1F(f"h_score_mixed_true{cut}_{key}", f"h_score_mixed_true{cut}_{key}", 100, 0, 1)
        h_score_mixed_false_all[key][cut] = ROOT.TH1F(f"h_score_mixed_false_all{cut}_{key}", f"h_score_mixed_false_all{cut}_{key}", 100, 0, 1)
        for w in wanted_components:
            

            # Initialize histograms for this key
            h_true = histo_dict[w][key][f"h_score_top_mixed_true{cut}_{key}"].Clone()
            h_score_mixed_true[key][cut].Add(h_true)
            h_score_mixed_false_other[key][cut] = histo_dict[w][key][f"h_score_top_mixed_false_other{cut}_{key}"].Clone()
            h_score_mixed_false_QCD[key][cut] = histo_dict[w][key][f"h_score_top_mixed_false_QCD{cut}_{key}"].Clone()
            h_score_mixed_false_all[key][cut] = histo_dict[w][key][f"h_score_top_mixed_false_all{cut}_{key}"].Clone()

            # Normalize histograms if they have content
            if h_score_mixed_true[key][cut].Integral() > 0:
                h_score_mixed_true[key][cut].Scale(1 / h_score_mixed_true[key][cut].Integral())
            if h_score_mixed_false_other[key][cut].Integral() > 0:
                h_score_mixed_false_other[key][cut].Scale(1 / h_score_mixed_false_other[key][cut].Integral())
            if h_score_mixed_false_QCD[key][cut].Integral() > 0:
                h_score_mixed_false_QCD[key][cut].Scale(1 / h_score_mixed_false_QCD[key][cut].Integral())
            if h_score_mixed_false_all[key][cut].Integral() > 0:
                h_score_mixed_false_all[key][cut].Scale(1 / h_score_mixed_false_all[key][cut].Integral())
                
        # Create a canvas for each key
        c = ROOT.TCanvas(f"c{cut}{key}", f"c{cut}{key}", 600, 600)
        c.SetLogy()
        # Set styles for histograms
        h_score_mixed_true[key][cut].SetTitle(f"Discrimination for -{cut} {key}")
        h_score_mixed_true[key][cut].GetXaxis().SetTitle("score")
        h_score_mixed_true[key][cut].GetYaxis().SetTitle("Normalized Counts")
        h_score_mixed_true[key][cut].GetYaxis().SetRangeUser(0.0001,1)
        h_score_mixed_true[key][cut].SetFillColorAlpha(ROOT.kRed, 0.6)

        #h_score_mixed_false_other[key][cut].SetFillColorAlpha(ROOT.kGreen, 0.6)
        #h_score_mixed_false_QCD[key][cut].SetFillColorAlpha(ROOT.kBlue, 0.6)
        h_score_mixed_false_all[key][cut].SetFillColorAlpha(ROOT.kBlue, 0.6)

        # Draw histograms
        h_score_mixed_true[key][cut].Draw("hist")
        h_score_mixed_false_all[key][cut].Draw("histsame")
        #h_score_mixed_false_other[key][cut].Draw("histsame")
        #h_score_mixed_false_QCD[key][cut].Draw("histsame")

        # Create legend
        leg = ROOT.TLegend(0.3, 0.6, 0.7, 0.9)
        leg.AddEntry(h_score_mixed_true[key][cut], "score top mixed true")
        leg.AddEntry(h_score_mixed_false_all[key][cut], "score top mixed false")
        #leg.AddEntry(h_score_mixed_false_QCD[key][cut], "score top mixed false QCD")
        #leg.AddEntry(h_score_mixed_false_other[key][cut], "score top mixed false other")
        leg.Draw("SAME")

        # Save the canvas as a PDF
        c.SaveAs(f"{path_to_graphic_folder}traintest/{cut}{key}_discrimination.pdf")

        #h_score_mixed_true[key][cut].Reset()
        #h_score_mixed_false_all[key][cut].Reset


#CICLO FOR PER LA ROC
import matplotlib.pyplot as plt
TPR_mixed = {}
FPR_mixed_QCD = {}
FPR_mixed_other = {}
FPR_mixed_all = {}
score_mixed = {}
for cut in cuts:
    plt.figure(1)
    TPR_mixed[cut] = {}
    FPR_mixed_QCD[cut] = {}
    FPR_mixed_other[cut] = {}
    FPR_mixed_all[cut] = {}
    score_mixed[cut] = {}
    for key in keys:
        TPR_mixed[cut][key] = []
        FPR_mixed_QCD[cut][key] = []
        FPR_mixed_other[cut][key] = []
        FPR_mixed_all[cut][key] = []
        score_mixed[cut][key] = []

        #faccio il for al contrario così inizio da score alti e TPR e FPR bassi
        for bin in range (100,-1,-1):
            #se lo score tresh è 0 il TPR è 1
            #print(bin)
            if h_score_mixed_true[key][cut].Integral(-1,100) !=0:
                TPR_m = h_score_mixed_true[key][cut].Integral(bin,100)/h_score_mixed_true[key][cut].Integral()
                #print("TPR",TPR_m)
            else:
                TPR_m = 0
                #print("TPR",TPR_m)
            if h_score_mixed_false_QCD[key][cut].Integral(-1,100) !=0:
                FPR_m_QCD = h_score_mixed_false_QCD[key][cut].Integral(bin,100)/h_score_mixed_false_QCD[key][cut].Integral()
            else:
                FPR_m_QCD = 0
            if h_score_mixed_false_other[key][cut].Integral(-1,100) !=0:
                FPR_m_other = h_score_mixed_false_other[key][cut].Integral(bin,100)/h_score_mixed_false_other[key][cut].Integral()
            else:
                FPR_m_other = 0
            if h_score_mixed_false_all[key][cut].Integral(-1,100) !=0:
                FPR_m_all = h_score_mixed_false_all[key][cut].Integral(bin,100)/h_score_mixed_false_all[key][cut].Integral()
                #print("FPR",FPR_m_all)

            else:
                FPR_m_all = 0
                #print("FPR",FPR_m_all)
            #score_m = h_score_mixed_false_all.GetBinCenter(h_score_mixed_false_all.GetBin(bin)) #avrei potuto mettere bin/100 ma forse così è più generale
            score_m = bin/100
            #print("thr:",score_m)
            TPR_mixed[cut][key].append(TPR_m)
            FPR_mixed_QCD[cut][key].append(FPR_m_QCD)
            FPR_mixed_other[cut][key].append(FPR_m_other)
            FPR_mixed_all[cut][key].append(FPR_m_all)
            score_mixed[cut][key].append(score_m)
            
            
            plt.plot(FPR_mixed_all[cut][key], TPR_mixed[cut][key], label=f"{key}",  linewidth=1, linestyle="-")
            plt.xlabel("False positives [%]")
            plt.ylabel("True positives [%]")
            # plt.xlim(xlim)
            plt.ylim(-0.1,1.1)
            plt.grid(True)
            # ax = plt.gca()
            # ax.set_aspect("equal")
            plt.xscale("log")
            plt.legend(loc="lower right")
            if cut=="" :
                plt.title(f"ROC curves on the full dataset")
            else:
                plt.title(f"ROC curves for {cut}")
            #plt.savefig(f"{path_to_graphics_folder}/{component}_roc_curve_mixed_all.png")
            plt.savefig(f"{path_to_graphic_folder}multiROC/roc_curve_mixed_all{cut}.pdf")
            
        #print(cut,key,"FPR:",FPR_mixed_all[cut][key],"\n", "TPR:",TPR_mixed[cut][key],"\n", "Thr:",score_mixed[cut][key])
        print(cut,key,"FPR:",FPR_mixed_all[cut][key],"\n", "TPR:",TPR_mixed[cut][key],"\n", "Thr:",score_mixed[cut][key])
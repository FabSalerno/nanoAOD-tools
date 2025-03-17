import ROOT
ROOT.PyConfig.IgnoreCommandLineOptions = True
import json
from PhysicsTools.NanoAODTools.postprocessing.framework.datamodel import Collection, Object 
from PhysicsTools.NanoAODTools.postprocessing.framework.eventloop import Module
import os
# score thresholds

path_to_model_folder    = "/eos/user/f/fsalerno/framework/MachineLearning/models/"
mods                    = ["CNN_2D","CNN_2D_LSTM"]
cuts                    = ["_0_pt",]
n_PFCs                  = 60
models                  = {}


keys=[]
for mod in mods:
    for cut in cuts:
        key=f"{n_PFCs}_{mod}{cut}"
        if os.path.isfile(f"{path_to_model_folder}/model_{key}.h5"):
            keys.append(key)

thr                = "0.1%"  
threshold = {}
for key in keys:    
    score_thresholds = f"/eos/user/f/fsalerno/framework/MachineLearning/thresholds/score_thresholds_{key}.json"                                          
    with open(score_thresholds, "r") as fjson:
        thresholds  = json.load(fjson)
    threshold[key]   = thresholds[thr]["thr"]

class event_counter_1_1000(Module):
    def __init__(self):
        pass

    def beginJob(self):
        pass

    def endJob(self):
        pass

    def beginFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):  
        
        self.h_ntops_1_per_1000 = {}
        self.h_nevents_1_per_1000 = {}
        self.h_nevents_1_per_1000_cut_200_pt = {}
        self.h_nevents_1_per_1000_cut_300_pt = {}
        self.h_pt_1_per_1000 = {}
        self.h_MET_1_per_1000 = {}

        for key in keys:
            self.h_ntops_1_per_1000[key] = ROOT.TH1F(f"ntops_1_per_1000_{key}",  f"ntops_1_per_1000_{key}", 6, 0, 6)
            self.h_nevents_1_per_1000[key] = ROOT.TH1F(f"nevents_1_per_1000_{key}", f"nevents_1_per_1000_{key}", 6, 0, 6)
            self.h_nevents_1_per_1000_cut_200_pt[key] = ROOT.TH1F(f"nevents_1_per_1000_cut_200_pt_{key}", f"nevents_1_per_1000_cut_200_pt_{key}", 6, 0, 6)
            self.h_nevents_1_per_1000_cut_300_pt[key] = ROOT.TH1F(f"nevents_1_per_1000_cut_300_pt_{key}", f"nevents_1_per_1000_cut_300_pt_{key}", 6, 0, 6)
            self.h_pt_1_per_1000[key] = ROOT.TH1F(f"pt_1_per_1000_{key}", f"pt_1_per_1000_{key}", 100, 0, 1000)
            self.h_MET_1_per_1000[key] = ROOT.TH1F(f"MET_1_per_1000_{key}", f"MET_1_per_1000_{key}", 100, 200, 800)
    
    def endFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):
        prevdir = ROOT.gDirectory
        outputFile.cd()
        for key in keys:
            self.h_ntops_1_per_1000[key].Write() 
            self.h_nevents_1_per_1000[key].Write() 
            self.h_nevents_1_per_1000_cut_200_pt[key].Write()
            self.h_pt_1_per_1000[key].Write()
            self.h_MET_1_per_1000[key].Write()
        prevdir.cd()

    def analyze(self, event):
        """Process event, return True (go to next module) or False (fail, go to next event)"""
        tops_mixed = Collection(event, "TopMixed")
        met = Object(event, "MET")
        
        for key in keys:  
            event = 0
            event_200 = 0
            event_300 = 0
            for top in tops_mixed:
                top_score_key = f"TopScore_{key}"
                if hasattr(top, top_score_key):
                    TopScore = getattr(top, top_score_key) 
                if TopScore>= threshold[key]:
                    event = 1
                    self.h_ntops_1_per_1000[key].Fill(4)
                    self.h_pt_1_per_1000[key].Fill(top.pt)
                    if top.pt>=200:
                        event_200 = 1
                    if top.pt>=300:
                        event_300 = 1
            
            if event == 1:
                self.h_nevents_1_per_1000[key].Fill(4)
                self.h_MET_1_per_1000[key].Fill(met.pt)
            if event_200 == 1:
                self.h_nevents_1_per_1000_cut_200_pt[key].Fill(4)
            if event_300 == 1:
                self.h_nevents_1_per_1000_cut_300_pt[key].Fill(4)
        
        return True
import ROOT
ROOT.PyConfig.IgnoreCommandLineOptions = True
import json

from PhysicsTools.NanoAODTools.postprocessing.framework.datamodel import Collection, Object 
from PhysicsTools.NanoAODTools.postprocessing.framework.eventloop import Module

# score thresholds
score_thresholds   = "/eos/user/f/fsalerno/framework/MachineLearning/Training_HOTVR_2018_1_j_in_HVRj/score_thresholds.json"
 # threshold to select top candidates
thr                = "5%"                                                
with open(score_thresholds, "r") as fjson:
    thresholds  = json.load(fjson)
threshold   = thresholds[thr]["thr"]

class event_counter_5_100(Module):
    def __init__(self):
        self.writeHistFile=True

    def beginJob(self,histFile=None,histDirName=None):
        Module.beginJob(self,histFile,histDirName+"_event_counter_5_per_100")
        self.h_ntops_5_per_100_standard = ROOT.TH1F("ntops_standard_5_per_100","ntops_standard_5_per_100",15,0,15)
        self.h_ntops_5_per_100_BDT = ROOT.TH1F("ntops_BDT_5_per_100","ntops_BDT_5_per_100",15,0,15)
        self.h_n_best_tops_5_per_100 = ROOT.TH1F("n_best_tops_5_per_100","n_best_tops_5_per_100",15,0,15)
        self.h_nevents_5_per_100_standard = ROOT.TH1F("nevents_standard_5_per_100","nevents_standard_5_per_100",15,0,15)
        self.h_nevents_5_per_100_BDT = ROOT.TH1F("nevents_BDT_5_per_100","nevents_BDT_5_per_100",15,0,15)
        self.h_nevents_5_per_100_standard_200_pt = ROOT.TH1F("nevents_standard_5_per_100_200_pt","nevents_standard_5_per_100_200_pt",15,0,15)
        self.h_nevents_5_per_100_BDT_200_pt = ROOT.TH1F("nevents_BDT_5_per_100_200_pt","nevents_BDT_5_per_100_200_pt",15,0,15)
        self.h_pt_5_per_100_standard = ROOT.TH1F("pt_standard_5_per_100","pt_standard_5_per_100",100,0,1000)
        self.h_pt_5_per_100_BDT = ROOT.TH1F("pt_BDT_5_per_100","pt_BDT_5_per_100",100,0,1000) 
        self.h_mass_5_per_100_standard = ROOT.TH1F("mass_standard_5_per_100","mass_standard_5_per_100",100,0,1000)
        self.h_mass_5_per_100_BDT = ROOT.TH1F("mass_BDT_5_per_100","mass_BDT_5_per_100",100,0,1000) 
        self.h_MET_5_per_100_standard = ROOT.TH1F("MET_standard_5_per_100","MET_standard_5_per_100",100,200,800)
        self.h_MET_5_per_100_BDT = ROOT.TH1F("MET_BDT_5_per_100","MET_BDT_5_per_100",60,200,800) 
        self.addObject(self.h_ntops_5_per_100_standard)
        self.addObject(self.h_ntops_5_per_100_BDT)
        self.addObject(self.h_n_best_tops_5_per_100)
        self.addObject(self.h_nevents_5_per_100_standard)
        self.addObject(self.h_nevents_5_per_100_BDT)
        self.addObject(self.h_nevents_5_per_100_standard_200_pt)
        self.addObject(self.h_nevents_5_per_100_BDT_200_pt)
        self.addObject(self.h_pt_5_per_100_standard)
        self.addObject(self.h_pt_5_per_100_BDT)
        self.addObject(self.h_mass_5_per_100_standard)
        self.addObject(self.h_mass_5_per_100_BDT)
        self.addObject(self.h_MET_5_per_100_standard)
        self.addObject(self.h_MET_5_per_100_BDT)



    def analyze(self, event):
        """process event, return True (go to next module) or False (fail, go to next event)"""
        tops_mixed= Collection(event, "TopMixed")
        hvrjets    = Collection(event,"selectedHOTVRJets_nominal")
        met        = Object(event, "MET")
        event_standard=0
        event_BDT=0
        event_standard_200=0
        event_BDT_200=0
        best_tops=[]
        for top in tops_mixed:
            if (top.TopScore_standard>=threshold):
                event_standard=1
                self.h_ntops_5_per_100_standard.Fill(3)
                self.h_pt_5_per_100_standard.Fill(top.pt)
                self.h_mass_5_per_100_standard.Fill(top.mass)
                if top.pt>200:
                    event_standard_200=1
        if event_standard==1:
            self.h_nevents_5_per_100_standard.Fill(2)
        if event_standard_200==1:
            self.h_nevents_5_per_100_standard_200_pt.Fill(4)

        for hvrjet in hvrjets:
            if hvrjet.scoreBDT>=0.79:
                event_BDT=1
                self.h_ntops_5_per_100_BDT.Fill(5)
                self.h_pt_5_per_100_BDT.Fill(hvrjet.pt)
                self.h_mass_5_per_100_BDT.Fill(hvrjet.mass)
                if hvrjet.pt>200:
                    event_BDT_200=1
        if event_BDT==1:
            self.h_nevents_5_per_100_BDT.Fill(3)
            self.h_MET_5_per_100_BDT.Fill(met.energy)
        if event_BDT_200==1:
            self.h_nevents_5_per_100_BDT_200_pt.Fill(5)


            
        return True
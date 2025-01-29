import ROOT
ROOT.PyConfig.IgnoreCommandLineOptions = True
import json

from PhysicsTools.NanoAODTools.postprocessing.framework.datamodel import Collection, Object 
from PhysicsTools.NanoAODTools.postprocessing.framework.eventloop import Module


# score thresholds
score_thresholds   = "/eos/user/f/fsalerno/framework/MachineLearning/Training_HOTVR_2018_2_final/score_thresholds.json"
 # threshold to select top candidates
thr                = "0.1%"                                                
with open(score_thresholds, "r") as fjson:
    thresholds  = json.load(fjson)
threshold   = thresholds[thr]["thr"]



class close_histos(Module):
    def __init__(self):
        self.writeHistFile=True

    def beginJob(self,histFile=None,histDirName=None):
        Module.beginJob(self,histFile,histDirName+"_close")
        self.h_nevents_close = ROOT.TH1F("nevents_close","nevents_close",15,0,15)
        self.addObject(self.h_nevents_close)


    def analyze(self, event):
        """process event, return True (go to next module) or False (fail, go to next event)"""
        
        self.h_nevents_close.Fill(1)
       
        return True





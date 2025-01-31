import ROOT
ROOT.PyConfig.IgnoreCommandLineOptions = True
import json

from PhysicsTools.NanoAODTools.postprocessing.framework.datamodel import Collection, Object 
from PhysicsTools.NanoAODTools.postprocessing.framework.eventloop import Module





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





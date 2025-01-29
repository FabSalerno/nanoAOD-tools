import ROOT
ROOT.PyConfig.IgnoreCommandLineOptions = True

from PhysicsTools.NanoAODTools.postprocessing.framework.datamodel import Collection, Object 
from PhysicsTools.NanoAODTools.postprocessing.framework.eventloop import Module

class event_counter_post(Module):
    def __init__(self):
        self.writeHistFile=True

    def beginJob(self,histFile=None,histDirName=None):
        Module.beginJob(self,histFile,histDirName+"_event_counter_post")
        self.h_nevents_post = ROOT.TH1F("nevents_post","nevents_post",15,0,15)
        self.h_MET_post = ROOT.TH1F("MET_post","MET_post",60,200,800)
        self.addObject(self.h_nevents_post)
        self.addObject(self.h_MET_post)


    def analyze(self, event):
        """process event, return True (go to next module) or False (fail, go to next event)"""
        met        = Object(event, "MET")
        self.h_nevents_post.Fill(1)
        self.h_MET_post.Fill(met.energy)

        return True

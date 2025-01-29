import ROOT
ROOT.PyConfig.IgnoreCommandLineOptions = True
from PhysicsTools.NanoAODTools.postprocessing.framework.datamodel import Collection, Object 
from PhysicsTools.NanoAODTools.postprocessing.framework.eventloop import Module

class event_counter_pre(Module):
    def __init__(self):
        self.writeHistFile=True

    def beginJob(self,histFile=None,histDirName=None):
        Module.beginJob(self,histFile,histDirName+"_event_counter_pre")
        self.h_nevents_pre = ROOT.TH1F("nevents_pre","nevents_pre",6,0,6)
        self.h_MET_pre = ROOT.TH1F("MET_post","MET_pre",60,200,800)
        self.addObject(self.h_MET_pre)
        self.addObject(self.h_nevents_pre)


    def analyze(self, event):
        met        = Object(event, "MET")
        self.h_nevents_pre.Fill(0)
        self.h_MET_pre.Fill(met.pt)
        return True

import ROOT
ROOT.PyConfig.IgnoreCommandLineOptions = True
from PhysicsTools.NanoAODTools.postprocessing.framework.datamodel import Collection, Object 
from PhysicsTools.NanoAODTools.postprocessing.framework.eventloop import Module

class event_counter_pre(Module):
    def __init__(self):
        pass

    def beginJob(sel):
        pass

    def endJob(self):
        pass
    
    def beginFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):
        self.out = wrappedOutputTree
        #self.out.branch("nEvents_initial",          "I", lenVar="nEvents")
        self.h_nevents_pre = ROOT.TH1D("nevents_pre","nevents_pre",6,0,6)
        self.h_neventsgenweighted_pre = ROOT.TH1D('nEventsGenWeighted_pre', 'nEventsGenWeighted_pre', 6, 0, 6)
        
    def endFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):
        prevdir = ROOT.gDirectory
        outputFile.cd()
        self.h_nevents_pre.Write()
        #        self.h_nweightedevents.Write()
        self.h_neventsgenweighted_pre.Write()
        prevdir.cd()


    def analyze(self, event):
        #met        = Object(event, "MET")
        self.h_nevents_pre.Fill(0)
        if hasattr(event, 'Generator_weight') and event.Generator_weight < 0:
            self.h_neventsgenweighted_pre.Fill(0, -1)
        else:
            self.h_neventsgenweighted_pre.Fill(0)
        #self.out.fillBranch("nEvents_initial", 0)
        return True

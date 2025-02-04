import ROOT
ROOT.PyConfig.IgnoreCommandLineOptions = True
from PhysicsTools.NanoAODTools.postprocessing.framework.datamodel import Collection, Object 
from PhysicsTools.NanoAODTools.postprocessing.framework.eventloop import Module

class event_counter_post(Module):
    def __init__(self):
        pass

    def beginJob(sel):
        pass

    def endJob(self):
        pass
    
    def beginFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):
        self.h_nevents_post = ROOT.TH1D("nevents_post","nevents_post",6,0,6)
        self.h_neventsgenweighted_post = ROOT.TH1D('nEventsGenWeighted_post', 'nEventsGenWeighted_post', 6, 0, 6)
        
    def endFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):
        prevdir = ROOT.gDirectory
        outputFile.cd()
        self.h_nevents_post.Write()
        #        self.h_nweightedevents.Write()
        self.h_neventsgenweighted_post.Write()
        prevdir.cd()


    def analyze(self, event):
        #met        = Object(event, "MET")
        self.h_nevents_post.Fill(1)
        if hasattr(event, 'Generator_weight') and event.Generator_weight < 0:
            self.h_neventsgenweighted_post.Fill(1, -1)
        else:
            self.h_neventsgenweighted_post.Fill(1)

        return True

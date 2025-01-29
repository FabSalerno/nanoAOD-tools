import ROOT
import math
#from datetime import datetime
ROOT.PyConfig.IgnoreCommandLineOptions = True

from PhysicsTools.NanoAODTools.postprocessing.framework.datamodel import Collection, Object
from PhysicsTools.NanoAODTools.postprocessing.framework.eventloop import Module
from PhysicsTools.NanoAODTools.postprocessing.tools import *

    
class Mtt_cut_gen_lvl(Module):
    def __init__(self):
        pass
    def beginJob(self):
        pass
    def endJob(self):
        pass
    def beginFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):
        self.out = wrappedOutputTree
    def endFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):
        pass
    def analyze(self, event):
        save = True
        genpart = Collection(event, "GenPart")
        tops = list(filter(lambda x : int(x.pdgId)==6, genpart))
        antitops = list(filter(lambda x : int(x.pdgId)==-6, genpart))
        top = ROOT.TLorentzVector()
        antitop = ROOT.TLorentzVector()
        if tops.pt>0:
            top.SetPtEtaPhiM(tops.pt, tops.eta, tops.phi, tops.mass)
        else:
            top.SetPtEtaPhiM(0, 0, 0, 0)
            print("Found top with pt=0")
        if antitops.pt>0:
            antitop.SetPtEtaPhiM(antitops.pt, antitops.eta, antitops.phi, antitops.mass)
        else:
            antitop.SetPtEtaPhiM(0, 0, 0, 0)
            print("Found antitop with pt=0")

        Mtt = (top+antitop).M()
        if Mtt>=700:
            save = True
        else:
            save = False

        return save
    
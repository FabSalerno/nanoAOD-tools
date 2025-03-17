import ROOT
import math
import numpy as np
from array import array
#from datetime import datetime
ROOT.PyConfig.IgnoreCommandLineOptions = True
#from PhysicsTools.NanoAODTools.postprocessing.samples.samples import *
from PhysicsTools.NanoAODTools.postprocessing.framework.datamodel import Collection, Object
from PhysicsTools.NanoAODTools.postprocessing.framework.eventloop import Module
from PhysicsTools.NanoAODTools.postprocessing.tools import *
#from PhysicsTools.NanoAODTools.postprocessing.skimtree_utils import *
from itertools import combinations, chain
from scipy.special import comb


class truth_match_PNet(Module):
    def __init__(self, isMC=1):
        self.isMC = isMC
        pass
    def beginJob(self):
        pass
    def beginFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):
        self.out = wrappedOutputTree
        "branches Top candidate high pt"
        self.out.branch("nTopMerged", "I")
        self.out.branch("TopMerged_pt", "F", lenVar="nTopMerged")
        self.out.branch("TopMerged_eta", "F", lenVar="nTopMerged")
        self.out.branch("TopMerged_phi", "F", lenVar="nTopMerged")
        self.out.branch("TopMerged_mass", "F", lenVar="nTopMerged")
        self.out.branch("TopMerged_truth", "F", lenVar="nTopMerged")
        
    def endFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):
        pass

    def analyze(self, event):
        #t0 = datetime.now()
        """process event, return True (go to next module) or False (fail, go to next event)"""
        
        tops_merged = Collection(event,"FatJet")
        ntopmerged = len(tops_merged)
        #nessuna presel su top_merged
        genpart = Collection(event, "GenPart")
        tops_gen = list(filter(lambda x : int(x.pdgId)==6, genpart))
        topmerged_pt = []
        topmerged_eta = []
        topmerged_phi = []
        topmerged_mass = []

        topmergedtruth = np.zeros(ntopmerged)
        radius = 0.8
        for tm, top_merged in enumerate(tops_merged):
            topmerged_pt.append(top_merged.pt)
            topmerged_eta.append(top_merged.eta)
            topmerged_phi.append(top_merged.phi)
            topmerged_mass.append(top_merged.mass)
            for top_gen in tops_gen:
                #sto assumendo che non ci siano match multipli
                deltaR = deltaR(top_merged, top_gen)
                if deltaR < radius:
                    topmergedtruth[tm] = 1
                    break
                else:
                    topmergedtruth[tm] = 0
        self.out.fillBranch("TopMerged_truth", topmergedtruth)
        self.out.fillBranch("nTopMerged", ntopmerged)
        self.out.fillBranch("TopMerged_pt", topmerged_pt)
        self.out.fillBranch("TopMerged_eta", topmerged_eta)
        self.out.fillBranch("TopMerged_phi", topmerged_phi)
        self.out.fillBranch("TopMerged_mass", topmerged_mass)
        
        # t1 = datetime.now()
        # print("TopCandidate module time :", t1-t0)  
        return True


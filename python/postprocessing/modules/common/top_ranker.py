import ROOT
import math
import numpy as np
from array import array
#from datetime import datetime
ROOT.PyConfig.IgnoreCommandLineOptions = True
#from PhysicsTools.NanoAODTools.postprocessing.samples.samples import *
from PhysicsTools.NanoAODTools.postprocessing.framework.datamodel import Collection, Object
from PhysicsTools.NanoAODTools.postprocessing.framework.eventloop import Module
from PhysicsTools.NanoAODTools.postprocessing.tools_hotvr import *
#from PhysicsTools.NanoAODTools.postprocessing.skimtree_utils import *
import ROOT
ROOT.PyConfig.IgnoreCommandLineOptions = True


class categoryRanking(Module):
    def __init__(self, isMC=1):
        self.isMC = isMC
        pass

    def beginJob(self):
        pass

    def endJob(self):
        pass

    def beginFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):
        self.out = wrappedOutputTree
        
        self.out.branch("nCategoryRankedTopMixed", "I")
        self.out.branch("CategoryRankedTopMixed_idxHOTVRJet", "I", lenVar="nCategoryRankedTopMixed")
        self.out.branch("CategoryRankedTopMixed_idxFatJet", "I", lenVar="nCategoryRankedTopMixed")
        self.out.branch("CategoryRankedTopMixed_idxJet0", "I", lenVar="nCategoryRankedTopMixed")
        self.out.branch("CategoryRankedTopMixed_idxJet1", "I", lenVar="nCategoryRankedTopMixed")
        self.out.branch("CategoryRankedTopMixed_idxJet2", "I", lenVar="nCategoryRankedTopMixed")
        self.out.branch("CategoryRankedTopMixed_pt", "F", lenVar="nCategoryRankedTopMixed") 
        self.out.branch("CategoryRankedTopMixed_eta", "F", lenVar="nCategoryRankedTopMixed")
        self.out.branch("CategoryRankedTopMixed_phi", "F", lenVar="nCategoryRankedTopMixed")
        self.out.branch("CategoryRankedTopMixed_mass", "F", lenVar="nCategoryRankedTopMixed")
        self.out.branch("CategoryRankedTopMixed_truth", "F", lenVar="nCategoryRankedTopMixed")
        self.out.branch("CategoryRankedTopMixed_category", "F", lenVar="nCategoryRankedTopMixed")

        self.out.branch("nCategoryRankedTopResolved", "I")
        self.out.branch("CategoryRankedTopResolved_idxJet0", "I", lenVar="nCategoryRankedTopResolved")
        self.out.branch("CategoryRankedTopResolved_idxJet1", "I", lenVar="nCategoryRankedTopResolved")
        self.out.branch("CategoryRankedTopResolved_idxJet2", "I", lenVar="nCategoryRankedTopResolved")
        self.out.branch("CategoryRankedTopResolved_pt", "F", lenVar="nCategoryRankedTopResolved")
        self.out.branch("CategoryRankedTopResolved_eta", "F", lenVar="nCategoryRankedTopResolved")
        self.out.branch("CategoryRankedTopResolved_phi", "F", lenVar="nCategoryRankedTopResolved")
        self.out.branch("CategoryRankedTopResolved_mass", "F", lenVar="nCategoryRankedTopResolved")
        self.out.branch("CategoryRankedTopResolved_truth", "F", lenVar="nCategoryRankedTopResolved")
        self.out.branch("CategoryRankedTopResolved_category", "F", lenVar="nCategoryRankedTopResolved")


    def endFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):
        pass

    def analyze(self, event):
        """process event, return True (go to next module) or False (fail, go to next event)"""
        electrons = Collection(event, "Electron")
        muons = Collection(event, "Muon")
        jets = Collection(event, "Jet")
        fatJets = Collection(event, "FatJet")
        topmix = Collection(event, "TopMixed")
        topres = Collection(event, "TopResolved")

        topMixSel_idxjet0 = []
        topMixSel_idxjet1 = []
        topMixSel_idxjet2 = []
        topMixSel_idxhvrjet = []
        topMixSel_idxfatjet = []
        topMixSelPt = []
        topMixSelEta = []
        topMixSelPhi = []
        topMixSelMass = []
        topMixSelTruth = []
        topMixSelCategory = []
        topMixSelRank = []


        topResSel_idxjet0 = []
        topResSel_idxjet1 = []
        topResSel_idxjet2 = []
        topResSelPt = []
        topResSelEta = []
        topResSelPhi = []
        topResSelMass = []
        topResSelTruth = []
        topResSelCategory = []
        topResSelRank = []

        

        for t in topmix: 
            if t.category==0:
                topMixSel_idxjet0.append(t.idxjet0)
                topMixSel_idxjet1.append(t.idxjet1)
                topMixSel_idxjet2.append(t.idxjet2)
                topMixSel_idxhvrjet.append(t.idxhvrjet)
                topMixSel_idxfatjet.append(t.idxfatjet)
                topMixSelPt.append(t.pt)
                topMixSelEta.append(t.eta)
                topMixSelPhi.append(t.phi)
                topMixSelMass.append(t.mass)
                topMixSelCategory.append(t.category)
                if hasattr(t, "truth") and t.truth!=1:
                    topMixSelTruth.append(t.truth)

        for t in topres:
            if t.TopCategory>=score_res:
                topResSelPt.append(t.pt)
                topResSelEta.append(t.eta)
                topResSelPhi.append(t.phi)
                topResSelMass.append(t.mass)
                topResSelCategory.append(t.TopCategory)
                if t.truth==1:
                    topResSelTruth.append(t.truth)


        
        self.out.fillBranch("nCategoryRankedTopMixed", len(topMixSelPt))
        self.out.fillBranch("CategoryRankedTopMixed_idxHOTVRJet", topMixSel_idxhvrjet)
        self.out.fillBranch("CategoryRankedTopMixed_idxFatJet", topMixSel_idxfatjet)
        self.out.fillBranch("CategoryRankedTopMixed_idxJet0", topMixSel_idxjet0)
        self.out.fillBranch("CategoryRankedTopMixed_idxJet1", topMixSel_idxjet1)
        self.out.fillBranch("CategoryRankedTopMixed_idxJet2", topMixSel_idxjet2)
        self.out.fillBranch("CategoryRankedTopMixed_pt", topMixSelPt)
        self.out.fillBranch("CategoryRankedTopMixed_eta", topMixSelEta)
        self.out.fillBranch("CategoryRankedTopMixed_phi", topMixSelPhi)
        self.out.fillBranch("CategoryRankedTopMixed_mass", topMixSelMass)
        self.out.fillBranch("CategoryRankedTopMixed_truth", topMixSelTruth)
        self.out.fillBranch("CategoryRankedTopMixed_category", topMixSelCategory)

        self.out.fillBranch("nCategoryRankedTopResolved", len(topResSelPt))
        self.out.fillBranch("CategoryRankedTopResolved_idxJet0", topResSel_idxjet0)
        self.out.fillBranch("CategoryRankedTopResolved_idxJet1", topResSel_idxjet1)
        self.out.fillBranch("CategoryRankedTopResolved_idxJet2", topResSel_idxjet2)
        self.out.fillBranch("CategoryRankedTopResolved_pt", topResSelPt)
        self.out.fillBranch("CategoryRankedTopResolved_eta", topResSelEta)
        self.out.fillBranch("CategoryRankedTopResolved_phi", topResSelPhi)  
        self.out.fillBranch("CategoryRankedTopResolved_mass", topResSelMass)
        self.out.fillBranch("CategoryRankedTopResolved_truth", topResSelTruth)
        self.out.fillBranch("CategoryRankedTopResolved_category", topResSelCategory)

        return True



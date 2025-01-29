from PhysicsTools.NanoAODTools.postprocessing.framework.datamodel import Collection
from PhysicsTools.NanoAODTools.postprocessing.framework.eventloop import Module
import ROOT
ROOT.PyConfig.IgnoreCommandLineOptions = True


class scoreSelection(Module):
    def __init__(self, isMC=1):
        self.isMC = isMC
        pass

    def beginJob(self):
        pass

    def endJob(self):
        pass

    def beginFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):
        self.out = wrappedOutputTree
        
        self.out.branch("nSelectedTopMixed", "I")
        self.out.branch("SelectedTopMixed_pt", "F", lenVar="nSelectedTopMixed") 
        self.out.branch("SelectedTopMixed_eta", "F", lenVar="nSelectedTopMixed")
        self.out.branch("SelectedTopMixed_phi", "F", lenVar="nSelectedTopMixed")
        self.out.branch("SelectedTopMixed_mass", "F", lenVar="nSelectedTopMixed")
        self.out.branch("SelectedTopMixed_truth", "F", lenVar="nSelectedTopMixed")
        self.out.branch("SelectedTopMixed_score", "F", lenVar="nSelectedTopMixed")

        self.out.branch("nSelectedTopResolved", "I")
        self.out.branch("SelectedTopResolved_pt", "F", lenVar="nSelectedTopResolved")
        self.out.branch("SelectedTopResolved_eta", "F", lenVar="nSelectedTopResolved")
        self.out.branch("SelectedTopResolved_phi", "F", lenVar="nSelectedTopResolved")
        self.out.branch("SelectedTopResolved_mass", "F", lenVar="nSelectedTopResolved")
        self.out.branch("SelectedTopResolved_truth", "F", lenVar="nSelectedTopResolved")
        self.out.branch("SelectedTopResolved_score", "F", lenVar="nSelectedTopResolved")


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

        topMixSelPt = []
        topMixSelEta = []
        topMixSelPhi = []
        topMixSelMass = []
        topMixSelTruth = []
        topMixSelScore = []

        topResSelPt = []
        topResSelEta = []
        topResSelPhi = []
        topResSelMass = []
        topResSelTruth = []
        topResSelScore = []

        tresh = 0.001
        score_mix = 0
        score_res = 0

        if tresh == 0.001:
            score_mix = 0.905
            score_res = 0.685
        elif tresh == 0.01:
            score_mix = 0.565
            score_res = 0.425
        elif tresh == 0.05:
            score_mix = 0.135
            score_res = 0.165

        for t in topmix:
            if t.TopScore>=score_mix:
                topMixSelPt.append(t.pt)
                topMixSelEta.append(t.eta)
                topMixSelPhi.append(t.phi)
                topMixSelMass.append(t.mass)
                topMixSelScore.append(t.TopScore)
                if t.truth==1:
                    topMixSelTruth.append(t.truth)

        for t in topres:
            if t.TopScore>=score_res:
                topResSelPt.append(t.pt)
                topResSelEta.append(t.eta)
                topResSelPhi.append(t.phi)
                topResSelMass.append(t.mass)
                topResSelScore.append(t.TopScore)
                if t.truth==1:
                    topResSelTruth.append(t.truth)


        
        self.out.fillBranch("nSelectedTopMixed", len(topMixSelPt))
        self.out.fillBranch("SelectedTopMixed_pt", topMixSelPt)
        self.out.fillBranch("SelectedTopMixed_eta", topMixSelEta)
        self.out.fillBranch("SelectedTopMixed_phi", topMixSelPhi)
        self.out.fillBranch("SelectedTopMixed_mass", topMixSelMass)
        self.out.fillBranch("SelectedTopMixed_truth", topMixSelTruth)
        self.out.fillBranch("SelectedTopMixed_score", topMixSelScore)

        self.out.fillBranch("nSelectedTopResolved", len(topResSelPt))
        self.out.fillBranch("SelectedTopResolved_pt", topResSelPt)
        self.out.fillBranch("SelectedTopResolved_eta", topResSelEta)
        self.out.fillBranch("SelectedTopResolved_phi", topResSelPhi)  
        self.out.fillBranch("SelectedTopResolved_mass", topResSelMass)
        self.out.fillBranch("SelectedTopResolved_truth", topResSelTruth)
        self.out.fillBranch("SelectedTopResolved_score", topResSelScore)

        return True





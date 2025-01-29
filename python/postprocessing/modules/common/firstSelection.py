from PhysicsTools.NanoAODTools.postprocessing.framework.datamodel import Collection
from PhysicsTools.NanoAODTools.postprocessing.framework.eventloop import Module
import ROOT
ROOT.PyConfig.IgnoreCommandLineOptions = True


class firstSelection(Module):
    def __init__(self):
        pass

    def beginJob(self):
        pass

    def endJob(self):
        pass

    def beginFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):
        self.out = wrappedOutputTree
        #definire una branch che e' un intero nGoodJet""
        self.out.branch("nGoodJet", "I")
        self.out.branch("GoodJet_pt", "F", lenVar="nGoodJet") #questo deve avere una lenvar pari al numero di goodjet -- vedi come fa in top candidate
        self.out.branch("GoodJet_eta", "F", lenVar="nGoodJet")
        self.out.branch("GoodJet_phi", "F", lenVar="nGoodJet")
        self.out.branch("GoodJet_mass", "F", lenVar="nGoodJet")

        self.out.branch("nGoodFatJet", "I")
        self.out.branch("GoodFatJet_pt", "F", lenVar="nGoodFatJet") 
        self.out.branch("GoodFatJet_eta", "F", lenVar="nGoodFatJet")
        self.out.branch("GoodFatJet_phi", "F", lenVar="nGoodFatJet")
        self.out.branch("GoodFatJet_mass", "F", lenVar="nGoodFatJet")


    def endFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):
        pass

    def analyze(self, event):
        """process event, return True (go to next module) or False (fail, go to next event)"""
        electrons = Collection(event, "Electron")
        muons = Collection(event, "Muon")
        jets = Collection(event, "Jet")
        fatJets = Collection(event, "FatJet")

        goodJetsColl = list(filter(lambda j: j.pt > 30, jets))
        goodFatJetsColl = list(filter(lambda j: j.pt> 40, fatJets))

        if not ((len(goodJetsColl)>2) or (len(goodJetsColl)>1 and len(goodFatJetsColl)>0)): return False
        
        goodJetPt = []
        goodJetEta = []
        goodJetPhi = []
        goodJetMass = []

        goodFatJetPt = []
        goodFatJetEta = []
        goodFatJetPhi = []
        goodFatJetMass = []


        """if len(jets)>3:
            for j in jets:  
                if j.pt>40:
                    goodJetPt.append(j.pt)
                    goodJetEta.append(j.eta)
                    goodJetPhi.append(j.phi)
                    goodJetMass.append(j.mass)"""

        for j in goodJetsColl:
            goodJetPt.append(j.pt)
            goodJetEta.append(j.eta)
            goodJetPhi.append(j.phi)
            goodJetMass.append(j.mass)

        for j in goodFatJetsColl:
            goodFatJetPt.append(j.pt)
            goodFatJetEta.append(j.eta)
            goodFatJetPhi.append(j.phi)
            goodFatJetMass.append(j.mass)

        
        self.out.fillBranch("nGoodJet", len(goodJetPt))
        self.out.fillBranch("GoodJet_pt", goodJetPt)
        self.out.fillBranch("GoodJet_eta", goodJetEta)
        self.out.fillBranch("GoodJet_phi", goodJetPhi)
        self.out.fillBranch("GoodJet_mass", goodJetMass)

        self.out.fillBranch("nGoodFatJet", len(goodFatJetPt))
        self.out.fillBranch("GoodFatJet_pt", goodFatJetPt)
        self.out.fillBranch("GoodFatJet_eta", goodFatJetEta)
        self.out.fillBranch("GoodFatJet_phi", goodFatJetPhi)
        self.out.fillBranch("GoodFatJet_mass", goodFatJetMass)

        return True



firstSelectionConstr = lambda: firstSelection()

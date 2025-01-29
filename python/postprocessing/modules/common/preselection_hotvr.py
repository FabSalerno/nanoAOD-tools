import ROOT
import math
#from datetime import datetime
ROOT.PyConfig.IgnoreCommandLineOptions = True

from PhysicsTools.NanoAODTools.postprocessing.framework.datamodel import Collection, Object
from PhysicsTools.NanoAODTools.postprocessing.framework.eventloop import Module
from PhysicsTools.NanoAODTools.postprocessing.tools_hotvr import *


def get_electron(electrons):
    return list(filter(lambda x :  x.miniPFRelIso_all<0.1 and x.pt>35 and x.eta<2.5, electrons))
    
#tightRelIso_tightID_Muons_pfRelIso04_all constrains 03 ma perchè 0.3 e 0.4 sono i raggi dei coni in vui è definita l'isolation
#∆R = 0.2 when pT < 50 GeV, ∆R = 10 GeV/pT when 50 < pT < 200 GeV, and ∆R = 0.05

def get_muon(muons):
    return list(filter(lambda x : x.pfRelIso03_all<0.1 and x.pt>30 and x.eta<2.4, muons))


class preselection(Module):
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
        #t0 = datetime.now()
        goodEvent = False
        """process event, return True (go to next module) or False (fail, go to next event)"""
        met        = Object(event, "MET")
        electrons  = Collection(event,"loose_MVA_Electrons")
        muons      = Collection(event,"tightRelIso_tightID_Muons")
        jets       = Collection(event,"selectedJets_nominal")
        fatjets    = Collection(event,"selectedFatJets_nominal")
        hvrjets    = Collection(event,"selectedHOTVRJets_nominal")
        eventSum = ROOT.TLorentzVector()
        
        goodjets, goodfatjets, goodhvrjets = presel_hvr(jets, fatjets, hvrjets) 

        goodmuons = get_muon(muons)
        ngoodmuons = len(goodmuons)
        goodelectrons = get_electron(electrons)
        ngoodelectrons = len(goodelectrons)

        btagDeepB_mediumWP_2018  = 0.2783 
        isGoodEvent =   met.energy>50  and ngoodmuons==1 and ngoodelectrons==0 
        
        nbjets=0

        for goodjet in goodjets:
            if goodjet.btagDeepB>btagDeepB_mediumWP_2018:
                nbjets+=1
        
        goodEvent =  isGoodEvent and nbjets>=1

        #for j in goodJet:
        #    eventSum += j.p4()
            
        #self.out.fillBranch("HT_eventHT", eventSum.Pt())
        # t1 = datetime.now()
        # print("preselection module time :", t1-t0)
        return goodEvent

# define modules using the syntax 'name = lambda : constructor' to avoid having them loaded when not needed
#MySelectorModuleConstr = lambda : exampleProducer(jetetaSelection= lambda j : abs(j.eta)<2.4)

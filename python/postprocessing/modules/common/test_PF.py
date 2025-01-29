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






class PFCID(Module):
    def __init__(self, isMC=1):
        self.isMC = isMC
        pass
        
        
    def beginJob(self):
        pass
        
        
    def beginFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):
        self.out = wrappedOutputTree
        
        #self.out.branch("Jet_deltaR",      "F", lenVar="nJet") 
        self.out.branch("PFCands_JetIdx",         "I", lenVar="nPFCands")    #nJetPFCands"? 
        self.out.branch("PFCands_FatJetIdx",      "I", lenVar="nPFCands") 




    def endFile(self, inputFile, outputFile, inputTree,wrappedOutputTree):
        pass


    def analyze(self, event):
        #t0 = datetime.now()
        """process event, return True (go to next module) or False (fail, go to next event)"""        
        jets       = Collection(event,"Jet")
        Njets      = len(jets)
        PFCs       = Collection(event,"PFCands")
        NPFCs      = len(PFCs)
        jetPFCs    = Collection(event,"JetPFCands")
        fatjetPFCs = Collection(event,"FatJetPFCands")
        if self.isMC==1:
            #LHE     = Collection(event, "LHEPart")
            genpart = Collection(event, "GenPart")
        '''init variables to branch'''
        PFCs_jets_idx           = np.full(NPFCs,-1)
        PFCs_fat_jets_idx       = np.full(NPFCs,-1)



        for jPFC in jetPFCs:
            PFCs_jets_idx[jPFC.pFCandsIdx]=jPFC.jetIdx

        for fjPFC in fatjetPFCs:
            PFCs_fat_jets_idx[fjPFC.pFCandsIdx]=fjPFC.jetIdx


        self.out.fillBranch("PFCands_JetIdx", PFCs_jets_idx)
        self.out.fillBranch("PFCands_FatJetIdx", PFCs_fat_jets_idx)


        #self.out.fillBranch("Top_indFatJet", ind_fatjets) 
        #self.out.fillBranch("Top_indJet", ind_jets) 
        # t1 = datetime.now()
        # print("nanprepro module time :", t1-t0) 
        return True
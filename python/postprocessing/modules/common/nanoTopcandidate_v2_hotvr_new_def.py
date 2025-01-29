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
import keras.models 
from itertools import combinations, chain
from scipy.special import comb

def ncombs(n, k):  # return (n k) --> numero di k-ple dati n jets
    if (n-k)<0:
        return 0
    else:
        return factorial(n)/(factorial(n-k)*factorial(k))

def factorial(n):
    if n==0:
        return 1
    elif n<0:
        return 0
    else:
        return n*factorial(n-1)


# ========= UTILITIES =======================
###########################################################################
""" SE CI SONO SIA HOTVR CHE FAT USA PER LA RICOSTRUZIONE SOLO IL FAT"""
###########################################################################
"""take as argument a top candidate and return an int : 
0 = 3j1fj1hvrj = 3j1fj0hvrj =0
1 = 3j1fj0hvrj 
2 = 3j0fj1hvrj = 3j0fj1hj = 1
3 = 3j0fj0hvrj = 3j0fj0hvrj = 2
4 = 2j1fj1hvrj = 2j1fj =3
5 = 2j1fj0hvrj 
6 = 2j0fj1hvrj = 2J1hj =4
7 = full hj ricostruzione indipendente =5 per ora la escludiamo
"""
def topcategory(top): 

    #if top.idxHOTVRJet!=-1: #probabile overlap con altre categorie, lo metto all'inizio così se rientra in altre definizioni si sovrascrive
        #top_category = 5

    if top.idxJet0!=-1 and top.idxJet1!=-1 and top.idxJet2!=-1: #ci sono 3 jets
        if top.idxFatJet!=-1: #3j1fj
            top_category = 0 
        elif top.idxFatJet==-1: #3j0fj
            top_category = 1
    elif top.idxFatJet!=-1: #2j1fj
        top_category = 2
    if top.idxHOTVRJet!=-1:
        top_category = 3

    return top_category

def top_p4(category, top, jets, fatjets, hvrjets):
    if category == 0: 
        p4 = top3j1fj(hvrjets[top.idxHOTVRJets],fatjets[top.idxFatJet], jets[top.idxJet0], jets[top.idxJet1], jets[top.idxJet2])
    elif category == 1:
        p4 = jets[top.idxJet0].p4() + jets[top.idxJet1].p4() + jets[top.idxJet2].p4() 
    elif category == 2:
        p4 = top2j1fj(fatjets[top.idxFatJet], jets[top.idxJet0], jets[top.idxJet1])       
    elif category == 3:
        p4 = top1hvrj(hvrjets[top.idxFatJet], jets[top.idxJet0], jets[top.idxJet1])
    else:
        print("Error idx Top category not expected : ", category)
    return p4


def top3j0fj1hvrj(hvrj, j0, j1, j2, dr0=None, dr1=None, dr2=None):
    if dr0==None:
        dr0 = deltaR(hvrj,j0)<600/hvrj.pt
        dr1 = deltaR(hvrj,j1)<600/hvrj.pt
        dr2 = deltaR(hvrj,j2)<600/hvrj.pt
    if dr0*dr1*dr2:
        p4 = hvrj.p4()
    elif dr0*dr1:
        p4 = hvrj.p4()+j2.p4()
    elif dr0*dr2:
        p4 = hvrj.p4()+j1.p4()
    elif dr1*dr2:
        p4 = hvrj.p4()+j0.p4()
    elif dr0:
        p4 = hvrj.p4()+j1.p4()+j2.p4()
    elif dr1:
        p4 = hvrj.p4()+j0.p4()+j2.p4()
    elif dr2:
        p4 = hvrj.p4()+j0.p4()+j1.p4()
    else:
        p4 = (j0.p4()+j1.p4()+j2.p4()) #None      ###<--------------------to exclude 3j1fj not overlapping
    #print(p4, p4.M())
    return p4

def top1hvrj(hvrj):
    p4 = hvrj.p4()
    #print(p4, p4.M())
    return p4


def lowpt_top(j0, j1, j2):
    return j0.p4() + j1.p4() + j2.p4()



def highpt_top(j0, j1, j2, fj, hvrj): 
    if fj == None and hvrj==None:
        top = j0.p4()+j1.p4()+j2.p4()
    elif j2==None and hvrj==None:
        top = top2j1fj(fj, j0, j1)
    elif  fj!=None and j2!=None and hvrj==None:
        top = top3j1fj(fj, j0, j1, j2)
    if hvrj!=None:
        top = top1hvrj(hvrj)
    return top

def truth(j0=0, j1=0, j2=0, fj=0, hvrj=0):
    top_truth = 0
    if not hasattr(j2, "pt"): #non stiamo escludendo quelli in cui j2 c'è ma non è matchato? NO! perchè quando lo usiamo prendiamo tutte òe possibili combinazioni a prescindere da se ci sia j2 o no
        if (hasattr(fj, "pt")  and (j0.matched>0 and j1.matched>0 and fj.matched>0) and
            (j0.topMother== j1.topMother and j0.topMother== fj.topMother)): 
            #2j1fj 1
            flavs_j0, flavs_j1, flavs_fj = j0.pdgId, j1.pdgId, fj.pdgId
            jetflavs_list = get_pos_nums(flavs_j0) + get_pos_nums(flavs_j1) 
            fatjetflavs_list = get_pos_nums(flavs_fj)
            hotvrjetflavs_list = []

        else:
            jetflavs_list = []
            fatjetflavs_list = []
            hotvrjetflavs_list = []

    elif hasattr(j2, "pt"):
        if (hasattr(fj, "pt") and (not hasattr(hvrj, "pt")) and
           ((j0.matched>0 and j1.matched>0 and j2.matched>0 and fj.matched>0) and
           (j0.topMother== j1.topMother and j1.topMother== j2.topMother and j2.topMother==fj.topMother))):  
            #3j1fj 1 ok
            flavs_j0, flavs_j1, flavs_j2, flavs_fj = j0.pdgId, j1.pdgId, j2.pdgId, fj.pdgId
            jetflavs_list = get_pos_nums(flavs_j0) + get_pos_nums(flavs_j1) + get_pos_nums(flavs_j2)
            fatjetflavs_list = get_pos_nums(flavs_fj)
            hotvrjetflavs_list = []

        elif ((not hasattr(fj, "pt"))  and
            ((j0.matched>0 and j1.matched>0 and j2.matched>0) and
            (j0.topMother== j1.topMother and j1.topMother== j2.topMother))):  
            #3j0fj
            flavs_j0, flavs_j1, flavs_j2 = j0.pdgId, j1.pdgId, j2.pdgId
            jetflavs_list = get_pos_nums(flavs_j0) + get_pos_nums(flavs_j1) + get_pos_nums(flavs_j2)
            fatjetflavs_list = []
            hotvrjetflavs_list = []

        else: 
            jetflavs_list = []
            fatjetflavs_list = []
            hotvrjetflavs_list = []


    if (hasattr(hvrj, "pt") and (hvrj.matched>0)):  
            #3j0fj
            flavs_hvrj = hvrj.pdgId
            jetflavs_list = []
            fatjetflavs_list = []
            hotvrjetflavs_list = get_pos_nums(flavs_hvrj)

    else: 
        jetflavs_list = []
        fatjetflavs_list = []
        hotvrjetflavs_list = []
  
    
    if len(np.unique(jetflavs_list))==3:
        top_truth = 1
    elif len(np.unique(fatjetflavs_list))==3:
        top_truth = 1
    elif len(np.unique(hotvrjetflavs_list))==3:
        top_truth = 1 #veri solo se ce ne sono esattamente 3
    elif len(np.unique(jetflavs_list+fatjetflavs_list))==3:
        top_truth = 1
    else:
        top_truth = 0
        
    return top_truth

def quark_number(j0=0, j1=0, j2=0, fj=0, hvrj=0):
    n_quark_jets = 0
    n_quark_fatjets = 0  
    n_quark_hotvrjets = 0
    n_quark_tot = 0  
    if not hasattr(j2, "pt"): #non stiamo escludendo quelli in cui j2 c'è ma non è matchato? NO! perchè quando lo usiamo prendiamo tutte òe possibili combinazioni a prescindere da se ci sia j2 o no
        if (hasattr(fj, "pt")  and (j0.matched>0 and j1.matched>0 and fj.matched>0) and
            (j0.topMother== j1.topMother and j0.topMother== fj.topMother)): 
            #2j1fj 1
            flavs_j0, flavs_j1, flavs_fj = j0.pdgId, j1.pdgId, fj.pdgId
            jetflavs_list = get_pos_nums(flavs_j0) + get_pos_nums(flavs_j1) 
            fatjetflavs_list = get_pos_nums(flavs_fj)
            hotvrjetflavs_list = []

        else:
            jetflavs_list = []
            fatjetflavs_list = []
            hotvrjetflavs_list = []

    elif hasattr(j2, "pt"):
        if (hasattr(fj, "pt") and (not hasattr(hvrj, "pt")) and
           ((j0.matched>0 and j1.matched>0 and j2.matched>0 and fj.matched>0) and
           (j0.topMother== j1.topMother and j1.topMother== j2.topMother and j2.topMother==fj.topMother))):  
            #3j1fj 1 ok
            flavs_j0, flavs_j1, flavs_j2, flavs_fj = j0.pdgId, j1.pdgId, j2.pdgId, fj.pdgId
            jetflavs_list = get_pos_nums(flavs_j0) + get_pos_nums(flavs_j1) + get_pos_nums(flavs_j2)
            fatjetflavs_list = get_pos_nums(flavs_fj)
            hotvrjetflavs_list = []

        elif ((not hasattr(fj, "pt"))  and
            ((j0.matched>0 and j1.matched>0 and j2.matched>0) and
            (j0.topMother== j1.topMother and j1.topMother== j2.topMother))):  
            #3j0fj
            flavs_j0, flavs_j1, flavs_j2 = j0.pdgId, j1.pdgId, j2.pdgId
            jetflavs_list = get_pos_nums(flavs_j0) + get_pos_nums(flavs_j1) + get_pos_nums(flavs_j2)
            fatjetflavs_list = []
            hotvrjetflavs_list = []

        else: 
            jetflavs_list = []
            fatjetflavs_list = []
            hotvrjetflavs_list = []


    if (hasattr(hvrj, "pt") and (hvrj.matched>0)):  
            #3j0fj
            flavs_hvrj = hvrj.pdgId
            jetflavs_list = []
            fatjetflavs_list = []
            hotvrjetflavs_list = get_pos_nums(flavs_hvrj)

    else: 
        jetflavs_list = []
        fatjetflavs_list = []
        hotvrjetflavs_list = []
    
    
    n_quark_jets = len(jetflavs_list)
    #print("\nn_quark_jets",n_quark_jets, "jetflavs_list",jetflavs_list)
    n_quark_fatjets = len(fatjetflavs_list)
    #print("\nn_quark_Fatjets", n_quark_fatjets, "Fatjetflavs_list",fatjetflavs_list)
    n_quark_hotvrjets = len(hotvrjetflavs_list)
    #print("\nn_quark_hotvrjets",n_quark_hotvrjets, "hotvrjetflavs_list",hotvrjetflavs_list)
    n_quark_tot = len(np.unique(jetflavs_list+fatjetflavs_list+hotvrjetflavs_list))
    #print("\nn_quark_tot",n_quark_tot, "tot_list",(np.unique(jetflavs_list+fatjetflavs_list+hotvrjetflavs_list)))

    return n_quark_tot

def get_hvrjet(hvrjets):
    return list(filter(lambda x : x.pt , hvrjets))### provo a bypassare il fatto che non eista jetId
def presel_hvr(jets, fatjets,hvrjets): #returns 2 collections of jets and fatjets
    goodjets = get_jet(jets)
    goodfatjets = get_fatjet(fatjets)
    goodhvrjets = get_hvrjet(hvrjets)
    
    return goodjets, goodfatjets, goodhvrjets


#QUI FINISCONO LE FUNZIONI DI TOOLS DA MODIFICARE PER HOTVR





#ANDRA' DEFINITO UN ALTRO TIPO DI TOP O INTEGRATo HOTVR NEI DUE PRECEDENTI

def fill_mass(mass_dnn, idx_top, j0, j1, j2, fj, hvrj):
    if j2 != None:
        if fj == None and hvrj == None: 
        #3j0fj
            top = j0.p4()+j1.p4()+j2.p4()
            mass_dnn[idx_top, 0] = (j0.p4()+j1.p4()+j2.p4()).M()
            mass_dnn[idx_top, 1] = (j0.p4()+j1.p4()+j2.p4()).M()
        elif fj!=None:
        #3j1fj
            mass_dnn[idx_top, 0] = (j0.p4()+j1.p4()+j2.p4()).M()
            top = top3j1fj(fj, j0, j1, j2)
            mass_dnn[idx_top, 1] = top.M()
    elif j2 == None:
        if fj!=None:
        #2j1fj
            mass_dnn[idx_top, 0] = (j0.p4()+j1.p4()).M()
            top = top2j1fj(fj, j0, j1)
            mass_dnn[idx_top, 1] = top.M()
    if hvrj!=None: 
        #1hvrj
        mass_dnn[idx_top, 0] = (hvrj.p4()).M()
        top = top1hvrj(hvrj)
        mass_dnn[idx_top, 1] = top.M()

    return mass_dnn, top

def fill_fj(fj_dnn, fj, idx_top): 
    fj_dnn[idx_top, 0] = fj.area
    fj_dnn[idx_top, 1] = fj.btagDeepB
    fj_dnn[idx_top, 2] = fj.deepTagMD_TvsQCD
    fj_dnn[idx_top, 3] = fj.deepTagMD_WvsQCD
    fj_dnn[idx_top, 4] = fj.deepTag_QCD
    fj_dnn[idx_top, 5] = fj.deepTag_QCDothers
    fj_dnn[idx_top, 6] = fj.deepTag_TvsQCD
    fj_dnn[idx_top, 7] = fj.deepTag_WvsQCD
    fj_dnn[idx_top, 8] = fj.eta
    fj_dnn[idx_top, 9] = fj.mass
    fj_dnn[idx_top, 10] = fj.phi
    fj_dnn[idx_top, 11] = fj.pt
    return fj_dnn


def fill_HVRj(HVRj_dnn, HVRj, idx_top): 
    #le variabili sono placholders
    HVRj_dnn[idx_top, 0] = HVRj.area
    HVRj_dnn[idx_top, 1] = HVRj.eta
    HVRj_dnn[idx_top, 2] = HVRj.mass
    HVRj_dnn[idx_top, 3] = HVRj.phi
    HVRj_dnn[idx_top, 4] = HVRj.pt
    HVRj_dnn[idx_top, 5] = HVRj.nsubjets
    return HVRj_dnn

def fill_jets(jets_dnn, j0, j1, j2, sumjet, fj_phi, fj_eta, hvrj_phi, hvrj_eta, idx_top): 

    jets_dnn[idx_top, 0, 0] = j0.area
    jets_dnn[idx_top, 0, 1] = j0.btagDeepB
    jets_dnn[idx_top, 0, 2] = deltaEta(j0.eta, sumjet.Eta())#j0.#delta eta 3jets-jet
    jets_dnn[idx_top, 0, 3] = j0.mass
    jets_dnn[idx_top, 0, 4] = deltaPhi(j0.phi, sumjet.Phi())#j0.#delta phi 3jets-jet
    jets_dnn[idx_top, 0, 5] = j0.pt
    jets_dnn[idx_top, 0, 6] = deltaPhi(j0.phi, fj_phi)#j0.#deltaphi fj-jet
    jets_dnn[idx_top, 0, 7] = deltaEta(j0.eta, fj_eta)#j0.#deltaeta fj-jet
    jets_dnn[idx_top, 0, 8] = deltaPhi(j0.phi, hvrj_phi)#j0.#deltaphi hvrj-jet
    jets_dnn[idx_top, 0, 9] = deltaEta(j0.eta, hvrj_eta)#j0.#deltaeta hvrj-jet
    
    jets_dnn[idx_top, 1, 0] = j1.area
    jets_dnn[idx_top, 1, 1] = j1.btagDeepB
    jets_dnn[idx_top, 1, 2] = deltaEta(j1.eta, sumjet.Eta())
    jets_dnn[idx_top, 1, 3] = j1.mass
    jets_dnn[idx_top, 1, 4] = deltaPhi(j1.phi, sumjet.Phi())
    jets_dnn[idx_top, 1, 5] = j1.pt
    jets_dnn[idx_top, 1, 6] = deltaPhi(j1.phi, fj_phi)
    jets_dnn[idx_top, 1, 7] = deltaEta(j1.eta, fj_eta)
    jets_dnn[idx_top, 1, 8] = deltaPhi(j1.phi, hvrj_phi)
    jets_dnn[idx_top, 1, 9] = deltaEta(j1.eta, hvrj_eta)

    if hasattr(j2,"pt"):
        jets_dnn[idx_top, 2, 0] = j2.area
        jets_dnn[idx_top, 2, 1] = j2.btagDeepB
        jets_dnn[idx_top, 2, 2] = deltaEta(j2.eta, sumjet.Eta())#j2.#delta eta fj-jet
        jets_dnn[idx_top, 2, 3] = j2.mass
        jets_dnn[idx_top, 2, 4] = deltaPhi(j2.phi, sumjet.Phi())#j2.#delta phi fatjet-jet
        jets_dnn[idx_top, 2, 5] = j2.pt
        jets_dnn[idx_top, 2, 6] = deltaPhi(j2.phi, fj_phi)
        jets_dnn[idx_top, 2, 7] = deltaEta(j2.eta, fj_eta)
        jets_dnn[idx_top, 2, 8] = deltaPhi(j2.phi, hvrj_phi)
        jets_dnn[idx_top, 2, 9] = deltaEta(j2.eta, hvrj_eta)
    
    return jets_dnn

class nanoTopcand_hotvr_new_def(Module):
    def __init__(self, isMC=1, multiscore=1):
        self.isMC = isMC
        self.multiscore = multiscore
        pass
    def beginJob(self):
        pass
    def beginFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):
        self.out = wrappedOutputTree
        "branches Top candidate high pt"
        self.out.branch("nTopMixed", "I")
        self.out.branch("TopMixed_idxHOTVRJet", "I", lenVar="nTopMixed")
        self.out.branch("TopMixed_idxFatJet", "I", lenVar="nTopMixed")
        self.out.branch("TopMixed_idxJet0", "I", lenVar="nTopMixed")
        self.out.branch("TopMixed_idxJet1", "I", lenVar="nTopMixed")
        self.out.branch("TopMixed_idxJet2", "I", lenVar="nTopMixed")
        #self.out.branch("TopMixed_sumjetPt", "F", lenVar="nTopMixed")
        #self.out.branch("TopMixed_sumjetEta", "F", lenVar="nTopMixed")
        #self.out.branch("TopMixed_sumjetPhi", "F", lenVar="nTopMixed")
        #self.out.branch("TopMixed_sumjetMass", "F", lenVar="nTopMixed")
        self.out.branch("TopMixed_pt", "F", lenVar="nTopMixed")
        self.out.branch("TopMixed_eta", "F", lenVar="nTopMixed")
        self.out.branch("TopMixed_phi", "F", lenVar="nTopMixed")
        self.out.branch("TopMixed_mass", "F", lenVar="nTopMixed")
        self.out.branch("TopMixed_truth", "F", lenVar="nTopMixed")
        self.out.branch("TopMixed_category", "I", lenVar="nTopMixed")
        self.out.branch("TopMixed_nquark", "I", lenVar="nTopMixed")
        "branches Top candidate low pt"
        self.out.branch("nTopResolved", "I")
        self.out.branch("TopResolved_idxJet0", "I", lenVar="nTopResolved")
        self.out.branch("TopResolved_idxJet1", "I", lenVar="nTopResolved")
        self.out.branch("TopResolved_idxJet2", "I", lenVar="nTopResolved")
        self.out.branch("TopResolved_pt", "F", lenVar="nTopResolved")
        self.out.branch("TopResolved_eta", "F", lenVar="nTopResolved")
        self.out.branch("TopResolved_phi", "F", lenVar="nTopResolved")
        self.out.branch("TopResolved_mass", "F", lenVar="nTopResolved")
        self.out.branch("TopResolved_truth", "F", lenVar="nTopResolved")
        self.out.branch("TopResolved_category", "I", lenVar="nTopResolved")

    def endFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):
        pass

    def analyze(self, event):
        #print(event)
        #t0 = datetime.now()
        """process event, return True (go to next module) or False (fail, go to next event)"""

        jets       = Collection(event,"selectedJets_nominal")
        njets      = len(jets)
        fatjets    = Collection(event,"selectedFatJets_nominal")
        nfatjets   = len(fatjets)
        hvrjets    = Collection(event,"selectedHOTVRJets_nominal")
        nhvrjets   = len(hvrjets)
        goodjets, goodfatjets, goodhvrjets = presel_hvr(jets, fatjets, hvrjets) 
        ngoodjets = len(goodjets)
        ngoodfatjets = len(goodfatjets)
        ngoodhvrjets = len(goodhvrjets)

        pt_cut_low = 10000
        pt_cut_high = 0
        
        '''init variables to branch'''
        ntoplowpt = 0
        toplow_idxfatjet = []
        toplow_idxjet0 = []
        toplow_idxjet1 = []
        toplow_idxjet2 = []
        toplow_pt_ = []
        toplow_eta_ = []
        toplow_phi_ = []
        toplow_mass_ = []
        toplow_sumjetdeltarfatjet = []
        toplow_sumjetmaxdeltarjet = []
        toplow_truth = []
        toplow_category = []
        ntophighpt = 0
        tophigh_idxhvrjet = []
        tophigh_idxfatjet = []
        tophigh_idxjet0 = []
        tophigh_idxjet1 = []
        tophigh_idxjet2 = []
        tophigh_pt_ = []
        tophigh_eta_ = []
        tophigh_phi_ = []
        tophigh_mass_ = []
        tophigh_sumjetdeltarfatjet = []
        tophigh_sumjetmaxdeltarjet = []
        tophigh_truth = []
        tophigh_category = []
        tophigh_nquark = []
        #low pt top loop
        for idx_j0 in range(ngoodjets): #!Dalla preselezione idx_j0 tra tutti i jet
            for idx_j1 in range(idx_j0): #Fino al primo jet
                for idx_j2 in range(idx_j1): #fino al secondo jet
                    j0, j1, j2 = goodjets[idx_j0], goodjets[idx_j1], goodjets[idx_j2]
                    #print(j0.matched)
                    #print(j1.matched)
                    #print(j2.matched)
                    top_p4 = lowpt_top(j0, j1, j2)
                    if top_p4.Pt()<pt_cut_low:
                        ntoplowpt+=1
                        toplow_idxjet0.append(idx_j0)
                        toplow_idxjet1.append(idx_j1)
                        toplow_idxjet2.append(idx_j2)
                        toplow_pt_.append(top_p4.Pt())
                        toplow_eta_.append(top_p4.Eta())
                        toplow_phi_.append(top_p4.Phi())
                        toplow_mass_.append(top_p4.M())
                        toplow_category.append(2)
                        if self.isMC:
                            toplow_truth.append(truth(j0=j0, j1=j1, j2=j2))
                        else:
                            toplow_truth.append(0)
        
        for idx_j0 in range(ngoodjets):
                for idx_j1 in range(idx_j0):
                    for idx_fj in range(ngoodfatjets):
                        j0, j1 = goodjets[idx_j0],goodjets[idx_j1]
                        fj = goodfatjets[idx_fj]
                        top_p4 = highpt_top(j0=j0, j1=j1, j2=None, fj=fj, hvrj=None)  #2j1fj
                        if top_p4.Pt()>pt_cut_high:
                            ntophighpt += 1
                            tophigh_idxhvrjet.append(-1)
                            tophigh_idxfatjet.append(idx_fj)
                            tophigh_idxjet0.append(idx_j0)
                            tophigh_idxjet1.append(idx_j1)
                            tophigh_idxjet2.append(-1)
                            tophigh_pt_.append(top_p4.Pt())
                            tophigh_eta_.append(top_p4.Eta())
                            tophigh_phi_.append(top_p4.Phi())
                            tophigh_mass_.append(top_p4.M())
                            tophigh_category.append(2)
                            if self.isMC and self.multiscore==0:
                                tophigh_truth.append(truth(j0=j0, j1=j1, fj=fj)) 
                                tophigh_nquark.append(quark_number(j0=j0, j1=j1, fj=fj)) 

                            elif self.isMC and self.multiscore==1:
                                tophigh_nquark.append(quark_number(j0=j0, j1=j1, fj=fj)) 

                                if quark_number(j0=j0, j1=j1, fj=fj)==1 or quark_number(j0=j0, j1=j1, fj=fj)==2:
                                    tophigh_truth.append(-1)
                                
                                else:
                                    tophigh_truth.append(truth(j0=j0, j1=j1, fj=fj))                                
                            else:
                                tophigh_truth.append(0)

                    

                    for idx_j2 in range(idx_j1):
                        j0, j1, j2 = goodjets[idx_j0],goodjets[idx_j1],goodjets[idx_j2]
                        top_p4 = highpt_top(j0=j0, j1=j1, j2=j2, fj=None, hvrj=None) #3j0fj0hvrj
                        if top_p4.Pt()>pt_cut_high:
                            ntophighpt += 1
                            tophigh_idxhvrjet.append(-1)
                            tophigh_idxfatjet.append(-1)
                            tophigh_idxjet0.append(idx_j0)
                            tophigh_idxjet1.append(idx_j1)
                            tophigh_idxjet2.append(idx_j2)
                            tophigh_pt_.append(top_p4.Pt())
                            tophigh_eta_.append(top_p4.Eta())
                            tophigh_phi_.append(top_p4.Phi())
                            tophigh_mass_.append(top_p4.M())
                            tophigh_category.append(1)
                            #print("\n jet_0 id",idx_j0, "match_0", j0.matched, "pdgId_0", j0.pdgId, "jet_1 id", idx_j1, "match_1", j1.matched, "pdgId_1", j1.pdgId, "jet_1 id", idx_j2, "match_2", j2.matched, "pdgId_2", j2.pdgId)
                            #print("\n quark number",quark_number(j0=j0, j1=j1, j2=j2))
                            if self.isMC and self.multiscore==0:
                                tophigh_truth.append(truth(j0=j0, j1=j1, j2=j2))
                                tophigh_nquark.append(quark_number(j0=j0, j1=j1, j2=j2))
                            
                            elif self.isMC and self.multiscore==1:
                                tophigh_nquark.append(quark_number(j0=j0, j1=j1, j2=j2)) 

                                if quark_number(j0=j0, j1=j1, j2=j2)==1 or quark_number(j0=j0, j1=j1, j2=j2)==2:
                                    tophigh_truth.append(-1)

                                else:
                                    tophigh_truth.append(truth(j0=j0, j1=j1, j2=j2)) 
                                
                            else: 
                                tophigh_truth.append(0)


                        for idx_fj in range(ngoodfatjets):
                            j0, j1, j2 = goodjets[idx_j0],goodjets[idx_j1],goodjets[idx_j2]
                            fj = goodfatjets[idx_fj]
                            top_p4 = highpt_top(j0=j0, j1=j1, j2=j2, fj=fj, hvrj=None) #3j1fj0hvrj
                            if top_p4.Pt()>pt_cut_high:
                                ntophighpt += 1
                                tophigh_idxhvrjet.append(-1)
                                tophigh_idxfatjet.append(idx_fj)
                                tophigh_idxjet0.append(idx_j0)
                                tophigh_idxjet1.append(idx_j1)
                                tophigh_idxjet2.append(idx_j2)
                                tophigh_pt_.append(top_p4.Pt())
                                tophigh_eta_.append(top_p4.Eta())
                                tophigh_phi_.append(top_p4.Phi())
                                tophigh_mass_.append(top_p4.M())
                                tophigh_category.append(0)
                                if self.isMC and self.multiscore==0:
                                    tophigh_truth.append(truth(j0=j0, j1=j1, j2=j2, fj=fj))
                                    tophigh_nquark.append(quark_number(j0=j0, j1=j1, j2=j2, fj=fj))
                                
                                elif self.isMC and self.multiscore==1:
                                    tophigh_nquark.append(quark_number(j0=j0, j1=j1, j2=j2, fj=fj)) 
                                    
                                    if quark_number(j0=j0, j1=j1, j2=j2, fj=fj)==1 or quark_number(j0=j0, j1=j1, j2=j2, fj=fj)==2:
                                        tophigh_truth.append(-1)
                                                                      
                                    else:
                                        tophigh_truth.append(truth(j0=j0, j1=j1, j2=j2, fj=fj)) 

                                else: 
                                    tophigh_truth.append(0)

                                      
                        

        for idx_hvrj in range(ngoodhvrjets):
            hvrj = goodhvrjets[idx_hvrj]
            top_p4 = highpt_top(j0=None, j1=None, j2=None, fj=None, hvrj=hvrj) #1hvrj
            ntophighpt += 1
            print(idx_hvrj)
            tophigh_idxhvrjet.append(idx_hvrj)
            print(tophigh_idxhvrjet)
            tophigh_idxfatjet.append(-1)
            tophigh_idxjet0.append(-1)
            tophigh_idxjet1.append(-1)
            tophigh_idxjet2.append(-1)
            tophigh_pt_.append(top_p4.Pt())
            tophigh_eta_.append(top_p4.Eta())
            tophigh_phi_.append(top_p4.Phi())
            tophigh_mass_.append(top_p4.M())
            tophigh_category.append(3)
            if self.isMC and self.multiscore==0:
                tophigh_truth.append(truth(j0=None, j1=None, j2=None, fj=None, hvrj=hvrj))
                tophigh_nquark.append(quark_number(j0=None, j1=None, j2=None, fj=None, hvrj=hvrj))

            elif self.isMC and self.multiscore==1:
                tophigh_nquark.append(quark_number(j0=None, j1=None, j2=None, fj=None, hvrj=hvrj)) 
                
                if quark_number(j0=None, j1=None, j2=None, fj=None, hvrj=hvrj)==1 or quark_number(j0=None, j1=None, j2=None, fj=None, hvrj=hvrj)==2:
                    tophigh_truth.append(-1)

                else:
                    tophigh_truth.append(truth(j0=None, j1=None, j2=None, fj=None, hvrj=hvrj)) 
            else: 
                tophigh_truth.append(0)
        print("cat",tophigh_category)

        print("hvrj",tophigh_idxhvrjet)
        #print("saving branches")
        self.out.fillBranch("nTopResolved", ntoplowpt)
        self.out.fillBranch("TopResolved_idxJet0", toplow_idxjet0)
        self.out.fillBranch("TopResolved_idxJet1", toplow_idxjet1)
        self.out.fillBranch("TopResolved_idxJet2", toplow_idxjet2)
        self.out.fillBranch("TopResolved_pt", toplow_pt_)
        self.out.fillBranch("TopResolved_eta", toplow_eta_)
        self.out.fillBranch("TopResolved_phi", toplow_phi_)
        self.out.fillBranch("TopResolved_mass", toplow_mass_)
        self.out.fillBranch("TopResolved_truth", toplow_truth)
        self.out.fillBranch("TopResolved_category", toplow_category)
        self.out.fillBranch("nTopMixed", ntophighpt)
        self.out.fillBranch("TopMixed_idxHOTVRJet", tophigh_idxhvrjet)
        self.out.fillBranch("TopMixed_idxFatJet", tophigh_idxfatjet)
        self.out.fillBranch("TopMixed_idxJet0", tophigh_idxjet0)
        self.out.fillBranch("TopMixed_idxJet1", tophigh_idxjet1)
        self.out.fillBranch("TopMixed_idxJet2", tophigh_idxjet2)
        self.out.fillBranch("TopMixed_pt", tophigh_pt_)
        self.out.fillBranch("TopMixed_eta", tophigh_eta_)
        self.out.fillBranch("TopMixed_phi", tophigh_phi_)
        self.out.fillBranch("TopMixed_mass", tophigh_mass_)
        self.out.fillBranch("TopMixed_truth", tophigh_truth)
        self.out.fillBranch("TopMixed_category", tophigh_category)
        self.out.fillBranch("TopMixed_nquark", tophigh_nquark)

        #t1 = datetime.now()
        #print("TopCandidate module time :", t1-t0)
        #print("Fine evento")  
        return True


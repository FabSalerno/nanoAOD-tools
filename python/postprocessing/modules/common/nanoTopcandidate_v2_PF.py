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
#import keras.models 
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

def lowpt_top(j0, j1, j2):
    return j0.p4() + j1.p4() + j2.p4()

def highpt_top(j0, j1, j2, fj):
    if fj == None:
        top = j0.p4()+j1.p4()+j2.p4()
    elif j2==None:
        top = top2j1fj(fj, j0, j1)
    else:
        top = top3j1fj(fj, j0, j1, j2)
    return top


def fill_mass(mass_dnn, idx_top, j0, j1, j2, fj):
    if fj == None:#3j0fj
        top = j0.p4()+j1.p4()+j2.p4()
        mass_dnn[idx_top, 0] = (j0.p4()+j1.p4()+j2.p4()).M()
        mass_dnn[idx_top, 1] = (j0.p4()+j1.p4()+j2.p4()).M()
    elif j2 == None:#2j1fj
        mass_dnn[idx_top, 0] = (j0.p4()+j1.p4()).M()
        top = top2j1fj(fj, j0, j1)
        mass_dnn[idx_top, 1] = top.M()
    else: #3j1fj
        mass_dnn[idx_top, 0] = (j0.p4()+j1.p4()+j2.p4()).M()
        top = top3j1fj(fj, j0, j1, j2)
        mass_dnn[idx_top, 1] = top.M()
    return mass_dnn, top

#questa funzione conta il numero di quark matchati a un top, serviva per fare controlli sui vari tipi di fondo
def quark_number(j0=0, j1=0, j2=0, fj=0):
    n_quark_tot = 0 

    if not hasattr(j2, "pt"):
        if ((j0.matched>0 and j1.matched>0 and fj.matched>0) and
            (j0.topMother== j1.topMother and j0.topMother== fj.topMother)):
            flavs_j0, flavs_j1, flavs_fj = j0.pdgId, j1.pdgId, fj.pdgId
            jetflavs_list = get_pos_nums(flavs_j0) + get_pos_nums(flavs_j1) 
            fatjetflavs_list = get_pos_nums(flavs_fj)
        else: 
            jetflavs_list = []
            fatjetflavs_list = []
    else:
        if hasattr(fj, "pt"):
            if ((j0.matched>0 and j1.matched>0 and j2.matched>0 and fj.matched>0) and
                (j0.topMother== j1.topMother and j1.topMother== j2.topMother and
                   j2.topMother==fj.topMother)):
                flavs_j0, flavs_j1, flavs_j2, flavs_fj = j0.pdgId, j1.pdgId, j2.pdgId, fj.pdgId
                jetflavs_list = get_pos_nums(flavs_j0) + get_pos_nums(flavs_j1) + get_pos_nums(flavs_j2)
                fatjetflavs_list = get_pos_nums(flavs_fj)
            else: 
                jetflavs_list = []
                fatjetflavs_list = []
        else:
            if ((j0.matched>0 and j1.matched>0 and j2.matched>0) and
                ( j0.topMother== j1.topMother and j1.topMother== j2.topMother)): 
                flavs_j0, flavs_j1, flavs_j2 = j0.pdgId, j1.pdgId, j2.pdgId
                jetflavs_list = get_pos_nums(flavs_j0) + get_pos_nums(flavs_j1) + get_pos_nums(flavs_j2)
                fatjetflavs_list = []
            else: 
                jetflavs_list = []
                fatjetflavs_list = []

    n_quark_tot = len(np.unique(jetflavs_list+fatjetflavs_list))
    return n_quark_tot


class nanoTopcand(Module):
    def __init__(self, isMC=1, multiscore=0):
        self.isMC = isMC
        #questa variabile si inserisce da fuori e controlla se voglio distinguere i top falsi senza quark matchati da quelli con almeno un quark matchato
        self.multiscore = multiscore 
        pass
    def beginJob(self):
        pass
    def beginFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):
        self.out = wrappedOutputTree
        "branches Top candidate high pt"
        self.out.branch("nTopMixed", "I")
        self.out.branch("TopMixed_idxFatJet", "I", lenVar="nTopMixed")
        self.out.branch("TopMixed_idxJet0", "I", lenVar="nTopMixed")
        self.out.branch("TopMixed_idxJet1", "I", lenVar="nTopMixed")
        self.out.branch("TopMixed_idxJet2", "I", lenVar="nTopMixed")
        self.out.branch("Indexes_idxPFC", "I", lenVar="nIndexes")
        self.out.branch("nIndexes", "I") 
        #self.out.branch("TopMixed_idxPFC_3j1fj", "I", lenVar="nTopMixed") 
        #self.out.branch("TopMixed_idxPFC_3j0fj", "I", lenVar="nTopMixed")
        #self.out.branch("TopMixed_idxPFC_2j1fj", "I", lenVar="nTopMixed")
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

    def endFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):
        pass

    def analyze(self, event):
        #t0 = datetime.now()
        """process event, return True (go to next module) or False (fail, go to next event)"""
        
        jets        = Collection(event,"Jet")
        njets       = len(jets)
        fatjets     = Collection(event,"FatJet")
        nfatjets    = len(fatjets)
        goodjets, goodfatjets = presel(jets, fatjets)
        ngoodjets = len(goodjets)
        ngoodfatjets = len(goodfatjets)
        PFCands               = Collection(event,"PFCands")
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
        ntophighpt = 0
        tophigh_idxfatjet = []
        tophigh_idxjet0 = []
        tophigh_idxjet1 = []
        tophigh_idxjet2 = []
        tophigh_idxPFC = [] #questo vettore conterrà gli indici delle pfc che ci interessano per tutti i top, inizia con -1 e i vari pfc corrispondenti a top diversi sono separati tra loro da -ntop
        tophigh_category = []
        tophigh_nquark = []
        #tophigh_idxPFC_3j1fj = []
        #tophigh_idxPFC_3j0fj = []
        #tophigh_idxPFC_2j1fj = []
        tophigh_pt_ = []
        tophigh_eta_ = []
        tophigh_phi_ = []
        tophigh_mass_ = []
        tophigh_sumjetdeltarfatjet = []
        tophigh_sumjetmaxdeltarjet = []
        tophigh_truth = []
        n_idxPFC=0

        tophigh_idxPFC.append(-1) 
        n_idxPFC+=1         
#low pt top loop
        for idx_j0 in range(ngoodjets):
            for idx_j1 in range(idx_j0):
                for idx_j2 in range(idx_j1):
                    j0, j1, j2 = goodjets[idx_j0], goodjets[idx_j1], goodjets[idx_j2]
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
                        if self.isMC:
                            toplow_truth.append(truth(j0=j0, j1=j1, j2=j2))
                        else:
                            toplow_truth.append(0)
#high pt top loop       
        for idx_j0 in range(ngoodjets):
                for idx_j1 in range(idx_j0):
                    for idx_fj in range(ngoodfatjets): #2j1fj
                        j0, j1 = goodjets[idx_j0],goodjets[idx_j1]
                        fj = goodfatjets[idx_fj]
                        top_p4 = highpt_top(j0=j0, j1=j1, j2=None, fj=fj)
                        if top_p4.Pt()>pt_cut_high:
                            ntophighpt += 1
                            tophigh_idxfatjet.append(idx_fj)
                            tophigh_idxjet0.append(idx_j0)
                            tophigh_idxjet1.append(idx_j1)
                            tophigh_idxjet2.append(-1)
                            tophigh_pt_.append(top_p4.Pt())
                            tophigh_eta_.append(top_p4.Eta())
                            tophigh_phi_.append(top_p4.Phi())
                            tophigh_mass_.append(top_p4.M())
                            tophigh_category.append(2)
                            #loop sulle particelle, conserva gli indici delle particelle presenti nei jet e i fatjet usati per la definizone dei top
                            for particle in PFCands:
                                if idx_j0==particle.JetIdx:
                                    tophigh_idxPFC.append(particle.Idx)
                                    n_idxPFC+=1
                                elif idx_j1==particle.JetIdx:
                                    tophigh_idxPFC.append(particle.Idx)
                                    n_idxPFC+=1
                                elif idx_fj==particle.FatJetIdx:
                                    tophigh_idxPFC.append(particle.Idx) 
                                    n_idxPFC+=1         
                            #finita la lista per un top, per separarlo dal successivo inserisco l'opposto del numero di top fin'ora visti nell'evento                     
                            tophigh_idxPFC.append(-1*(ntophighpt+1))
                            n_idxPFC+=1 
                            #print("idxPFC final 2j1fj",tophigh_idxPFC)

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

                    for idx_j2 in range(idx_j1): #3j0fj
                        j0, j1, j2 = goodjets[idx_j0],goodjets[idx_j1],goodjets[idx_j2]
                        top_p4 = highpt_top(j0=j0, j1=j1, j2=j2, fj=None)
                        if top_p4.Pt()>pt_cut_high:
                            ntophighpt += 1
                            tophigh_idxfatjet.append(-1)
                            tophigh_idxjet0.append(idx_j0)
                            tophigh_idxjet1.append(idx_j1)
                            tophigh_idxjet2.append(idx_j2)
                            tophigh_pt_.append(top_p4.Pt())
                            tophigh_eta_.append(top_p4.Eta())
                            tophigh_phi_.append(top_p4.Phi())
                            tophigh_mass_.append(top_p4.M())
                            tophigh_category.append(1)
                            for particle in PFCands:
                                #print("\nsorted",particle.pt)
                                #print(particle.JetIdx,"j0", idx_j0,"j1", idx_j1,"j2", idx_j2)
                                #print("particle_idx",particle.Idx)
                                if idx_j0==particle.JetIdx:
                                    tophigh_idxPFC.append(particle.Idx)
                                    n_idxPFC+=1
                                elif idx_j1==particle.JetIdx:
                                    tophigh_idxPFC.append(particle.Idx)
                                    n_idxPFC+=1
                                elif idx_j2==particle.JetIdx:
                                    tophigh_idxPFC.append(particle.Idx)
                                    n_idxPFC+=1                                
                                #print("idxPFC",tophigh_idxPFC_3j0fj)
                            tophigh_idxPFC.append(-1*(ntophighpt+1))
                            n_idxPFC+=1 
                            #print("idxPFC_3j0fj final",tophigh_idxPFC)
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

                        for idx_fj in range(ngoodfatjets): #3j1fj
                            j0, j1, j2 = goodjets[idx_j0],goodjets[idx_j1],goodjets[idx_j2]
                            fj = goodfatjets[idx_fj]
                            top_p4 = highpt_top(j0=j0, j1=j1, j2=j2, fj=fj)
                            if top_p4.Pt()>pt_cut_high:
                                ntophighpt += 1
                                tophigh_idxfatjet.append(idx_fj)
                                tophigh_idxjet0.append(idx_j0)
                                tophigh_idxjet1.append(idx_j1)
                                tophigh_idxjet2.append(idx_j2)
                                tophigh_pt_.append(top_p4.Pt())
                                tophigh_eta_.append(top_p4.Eta())
                                tophigh_phi_.append(top_p4.Phi())
                                tophigh_mass_.append(top_p4.M())
                                tophigh_category.append(0)
                                for particle in PFCands:
                                    if idx_j0==particle.JetIdx:
                                        tophigh_idxPFC.append(particle.Idx)
                                        n_idxPFC+=1
                                    elif idx_j1==particle.JetIdx:
                                        tophigh_idxPFC.append(particle.Idx)
                                        n_idxPFC+=1
                                    elif idx_j2==particle.JetIdx:
                                        tophigh_idxPFC.append(particle.Idx) 
                                        n_idxPFC+=1 
                                    elif idx_fj==particle.FatJetIdx:
                                        tophigh_idxPFC.append(particle.Idx) 
                                        n_idxPFC+=1                              
                                tophigh_idxPFC.append(-1*(ntophighpt+1))
                                n_idxPFC+=1 
                                #print("idxPFC final 3j1fj",tophigh_idxPFC)
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

        #print("idxPFC final",tophigh_idxPFC)
        #print("idxj0 final",tophigh_idxjet0)
        self.out.fillBranch("nTopResolved", ntoplowpt)
        self.out.fillBranch("TopResolved_idxJet0", toplow_idxjet0)
        self.out.fillBranch("TopResolved_idxJet1", toplow_idxjet1)
        self.out.fillBranch("TopResolved_idxJet2", toplow_idxjet2)
        self.out.fillBranch("TopResolved_pt", toplow_pt_)
        self.out.fillBranch("TopResolved_eta", toplow_eta_)
        self.out.fillBranch("TopResolved_phi", toplow_phi_)
        self.out.fillBranch("TopResolved_mass", toplow_mass_)
        self.out.fillBranch("TopResolved_truth", toplow_truth)
        self.out.fillBranch("nTopMixed", ntophighpt)
        self.out.fillBranch("TopMixed_idxFatJet", tophigh_idxfatjet)
        self.out.fillBranch("TopMixed_idxJet0", tophigh_idxjet0)
        self.out.fillBranch("TopMixed_idxJet1", tophigh_idxjet1)
        self.out.fillBranch("TopMixed_idxJet2", tophigh_idxjet2)
        self.out.fillBranch("Indexes_idxPFC", tophigh_idxPFC)
        self.out.fillBranch("nIndexes", n_idxPFC) #nuovo nome
        #self.out.fillBranch("TopMixed_idxPFC_3j1fj", tophigh_idxPFC_3j1fj)
        #self.out.fillBranch("TopMixed_idxPFC_3j0fj", tophigh_idxPFC_3j0fj)
        #self.out.fillBranch("TopMixed_idxPFC_2j1fj", tophigh_idxPFC_2j1fj)
        self.out.fillBranch("TopMixed_category", tophigh_category)
        self.out.fillBranch("TopMixed_pt", tophigh_pt_)
        self.out.fillBranch("TopMixed_eta", tophigh_eta_)
        self.out.fillBranch("TopMixed_phi", tophigh_phi_)
        self.out.fillBranch("TopMixed_mass", tophigh_mass_)
        self.out.fillBranch("TopMixed_truth", tophigh_truth)
        self.out.fillBranch("TopMixed_nquark", tophigh_nquark)
        # t1 = datetime.now()
        # print("TopCandidate module time :", t1-t0)  
        return True


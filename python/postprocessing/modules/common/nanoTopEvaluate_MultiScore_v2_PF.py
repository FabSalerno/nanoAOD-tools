import ROOT
import math
import numpy as np
from array import array
ROOT.PyConfig.IgnoreCommandLineOptions = True
from PhysicsTools.NanoAODTools.postprocessing.framework.datamodel import Collection, Object
from PhysicsTools.NanoAODTools.postprocessing.framework.eventloop import Module
from PhysicsTools.NanoAODTools.postprocessing.tools import *
import tensorflow as tf
from itertools import combinations, chain
import os
import matplotlib.pyplot as plt
from sklearn.metrics import roc_curve, auc

###### UTILITIES ######
def fill_mass(mass_dnn, idx_top, j0, j1, j2, fj):
    if fj == None:#3j0fj
        mass_dnn[idx_top, 0] = (j0.p4()+j1.p4()+j2.p4()).M()
        mass_dnn[idx_top, 1] = (j0.p4()+j1.p4()+j2.p4()).M()
        mass_dnn[idx_top, 2] = (j0.p4()+j1.p4()+j2.p4()).Pt()
    elif j2 == None:#2j1fj
        mass_dnn[idx_top, 0] = (j0.p4()+j1.p4()).M()
        top                  = top2j1fj(fj, j0, j1)
        mass_dnn[idx_top, 1] = top.M()
        mass_dnn[idx_top, 2] = top.Pt()
    else: #3j1fj
        mass_dnn[idx_top, 0] = (j0.p4()+j1.p4()+j2.p4()).M()
        top                  = top3j1fj(fj, j0, j1, j2)
        mass_dnn[idx_top, 1] = top.M()
        mass_dnn[idx_top, 2] = top.Pt()
    # if isinstance(variables_cluster,list):
    #     mass_dnn[idx_top, 2] = variables_cluster[0]
    #     mass_dnn[idx_top, 3] = variables_cluster[1]
    #     mass_dnn[idx_top, 4] = variables_cluster[2]
    return mass_dnn

def fill_fj(fj_dnn, fj, idx_top):
    if year==2018: 
        fj_dnn[idx_top, 0]  = fj.area
        fj_dnn[idx_top, 1]  = fj.btagDeepB
        fj_dnn[idx_top, 2]  = fj.deepTagMD_TvsQCD
        fj_dnn[idx_top, 3]  = fj.deepTagMD_WvsQCD
        fj_dnn[idx_top, 4]  = fj.deepTag_QCD
        fj_dnn[idx_top, 5]  = fj.deepTag_QCDothers
        fj_dnn[idx_top, 6]  = fj.deepTag_TvsQCD
        fj_dnn[idx_top, 7]  = fj.deepTag_WvsQCD
        fj_dnn[idx_top, 8]  = fj.eta
        fj_dnn[idx_top, 9]  = fj.mass
        fj_dnn[idx_top, 10] = fj.phi
        fj_dnn[idx_top, 11] = fj.pt
    elif year==2022: 
        fj_dnn[idx_top, 0]  = fj.area
        fj_dnn[idx_top, 1]  = fj.btagDeepB
        fj_dnn[idx_top, 2]  = fj.particleNetWithMass_QCD
        fj_dnn[idx_top, 3]  = fj.particleNetWithMass_TvsQCD
        fj_dnn[idx_top, 4]  = fj.particleNetWithMass_WvsQCD
        fj_dnn[idx_top, 5]  = fj.eta
        fj_dnn[idx_top, 6]  = fj.mass
        fj_dnn[idx_top, 7]  = fj.phi
        fj_dnn[idx_top, 8]  = fj.pt
    return fj_dnn

def fill_jets(jets_dnn, j0, j1, j2, sumjet, fj_phi, fj_eta, idx_top): 
    if year==2018:
        jets_dnn[idx_top, 0, 0] = j0.area
        jets_dnn[idx_top, 0, 1] = j0.btagDeepB
        jets_dnn[idx_top, 0, 2] = deltaEta(j0.eta, sumjet.Eta())#j0.#delta eta 3jets-jet
        jets_dnn[idx_top, 0, 3] = j0.mass
        jets_dnn[idx_top, 0, 4] = deltaPhi(j0.phi, sumjet.Phi())#j0.#delta phi 3jets-jet
        jets_dnn[idx_top, 0, 5] = j0.pt
        jets_dnn[idx_top, 0, 6] = deltaPhi(j0.phi, fj_phi)#j0.#deltaphi fj-jet
        jets_dnn[idx_top, 0, 7] = deltaEta(j0.eta, fj_eta)#j0.#deltaeta fj-jet
        
        jets_dnn[idx_top, 1, 0] = j1.area
        jets_dnn[idx_top, 1, 1] = j1.btagDeepB
        jets_dnn[idx_top, 1, 2] = deltaEta(j1.eta, sumjet.Eta())
        jets_dnn[idx_top, 1, 3] = j1.mass
        jets_dnn[idx_top, 1, 4] = deltaPhi(j1.phi, sumjet.Phi())
        jets_dnn[idx_top, 1, 5] = j1.pt
        jets_dnn[idx_top, 1, 6] = deltaPhi(j1.phi, fj_phi)
        jets_dnn[idx_top, 1, 7] = deltaEta(j1.eta, fj_eta)
        if hasattr(j2,"pt"):
            jets_dnn[idx_top, 2, 0] = j2.area
            jets_dnn[idx_top, 2, 1] = j2.btagDeepB
            jets_dnn[idx_top, 2, 2] = deltaEta(j2.eta, sumjet.Eta())#j2.#delta eta fj-jet
            jets_dnn[idx_top, 2, 3] = j2.mass
            jets_dnn[idx_top, 2, 4] = deltaPhi(j2.phi, sumjet.Phi())#j2.#delta phi fatjet-jet
            jets_dnn[idx_top, 2, 5] = j2.pt
            jets_dnn[idx_top, 2, 6] = deltaPhi(j2.phi, fj_phi)
            jets_dnn[idx_top, 2, 7] = deltaEta(j2.eta, fj_eta)
    elif year==2022:
        jets_dnn[idx_top, 0, 0] = j0.area
        jets_dnn[idx_top, 0, 1] = j0.btagPNetB
        jets_dnn[idx_top, 0, 2] = deltaEta(j0.eta, sumjet.Eta())#j0.#delta eta 3jets-jet
        jets_dnn[idx_top, 0, 3] = j0.mass
        jets_dnn[idx_top, 0, 4] = deltaPhi(j0.phi, sumjet.Phi())#j0.#delta phi 3jets-jet
        jets_dnn[idx_top, 0, 5] = j0.pt
        jets_dnn[idx_top, 0, 6] = deltaPhi(j0.phi, fj_phi)#j0.#deltaphi fj-jet
        jets_dnn[idx_top, 0, 7] = deltaEta(j0.eta, fj_eta)#j0.#deltaeta fj-jet
        
        jets_dnn[idx_top, 1, 0] = j1.area
        jets_dnn[idx_top, 1, 1] = j1.btagPNetB
        jets_dnn[idx_top, 1, 2] = deltaEta(j1.eta, sumjet.Eta())
        jets_dnn[idx_top, 1, 3] = j1.mass
        jets_dnn[idx_top, 1, 4] = deltaPhi(j1.phi, sumjet.Phi())
        jets_dnn[idx_top, 1, 5] = j1.pt
        jets_dnn[idx_top, 1, 6] = deltaPhi(j1.phi, fj_phi)
        jets_dnn[idx_top, 1, 7] = deltaEta(j1.eta, fj_eta)
        if hasattr(j2,"pt"):
            jets_dnn[idx_top, 2, 0] = j2.area
            jets_dnn[idx_top, 2, 1] = j2.btagPNetB
            jets_dnn[idx_top, 2, 2] = deltaEta(j2.eta, sumjet.Eta())#j2.#delta eta fj-jet
            jets_dnn[idx_top, 2, 3] = j2.mass
            jets_dnn[idx_top, 2, 4] = deltaPhi(j2.phi, sumjet.Phi())#j2.#delta phi fatjet-jet
            jets_dnn[idx_top, 2, 5] = j2.pt
            jets_dnn[idx_top, 2, 6] = deltaPhi(j2.phi, fj_phi)
            jets_dnn[idx_top, 2, 7] = deltaEta(j2.eta, fj_eta)
    return jets_dnn

def boost_PFC(pt_top,eta_top,phi_top,M_top,pt_PFC,eta_PFC,phi_PFC,M_PFC):
    pt_old = pt_PFC
    eta_old = eta_PFC
    phi_old = phi_PFC
    mass_old = M_PFC
    
    particle_old = ROOT.TLorentzVector()
    particle_old.SetPtEtaPhiM(pt_old, eta_old, phi_old, mass_old)

    pt_new_frame = pt_top
    eta_new_frame = eta_top
    phi_new_frame = phi_top
    mass_new_frame = M_top

    new_frame = ROOT.TLorentzVector()
    new_frame.SetPtEtaPhiM(pt_new_frame, eta_new_frame, phi_new_frame, mass_new_frame)

    boost_vector = new_frame.BoostVector()


    particle_old.Boost(-boost_vector.X(), -boost_vector.Y(), -boost_vector.Z())  


    pt_new = particle_old.Pt()
    eta_new = particle_old.Eta()
    phi_new = particle_old.Phi()
    mass_new = particle_old.M()

    return pt_new, eta_new, phi_new, mass_new

def fill_PFCs(n_PFCs, PFCs_dnn, PFCs, idx_top, pt_top, eta_top, phi_top, M_top): 
    for i,particle in enumerate(PFCs):
        if i<n_PFCs: #minore e non minore e uguale perchè parte da 0
            pt_boost, eta_boost, phi_boost, mass_boost = boost_PFC(pt_top, eta_top, phi_top, M_top, particle.pt ,particle.eta, particle.phi, particle.mass)
            PFCs_dnn[idx_top, i, 0] = pt_boost
            PFCs_dnn[idx_top, i, 1] = eta_boost
            PFCs_dnn[idx_top, i, 2] = phi_boost
            PFCs_dnn[idx_top, i, 3] = mass_boost
            PFCs_dnn[idx_top, i, 4] = particle.charge
            PFCs_dnn[idx_top, i, 5] = particle.pdgId
            PFCs_dnn[idx_top, i, 6] = particle.d0
            PFCs_dnn[idx_top, i, 7] = particle.dz
            PFCs_dnn[idx_top, i, 8] = particle.pvAssocQuality  
            PFCs_dnn[idx_top, i, 9] = particle.JetDeltaR
            PFCs_dnn[idx_top, i, 10] = particle.FatJetDeltaR
            PFCs_dnn[idx_top, i, 11] = particle.IsInJet
            PFCs_dnn[idx_top, i, 12] = particle.IsInFatJet
    return PFCs_dnn






# Leo's models #
# path_to_model_folder    = "/afs/cern.ch/user/l/lfavilla/CMSSW_12_6_0/src/PhysicsTools/NanoAODTools/python/postprocessing/my_analysis/my_framework/MLstudies/Training/Train/saved_models"
# path_to_model_folder    = "%s/src/PhysicsTools/NanoAODTools/python/postprocessing/my_analysis/my_framework/MLstudies/Training/Train/saved_models" % os.environ["CMSSW_BASE"]
path_to_model_folder    = "/eos/user/f/fsalerno/framework/MachineLearning/models/"
folder_model_antimo     = "%s/src/PhysicsTools/NanoAODTools/python/postprocessing/data/dict_tresholds/" % os.environ["CMSSW_BASE"]
antimo_model_name_H     = "model.h5"#"DNN_withtopmass_phase2.h5"
antimo_model_name_L     = "DNN_phase1_test_lowpt_DNN.h5"
# model_highpt_p2         = tf.keras.models.load_model(folder_model_antimo+model2_name)

# keys                    = ["base", "base_pt_g250", "base_pt_l250", "base_3j0fj", "base_pt_l250_3j0fj", "pt_flatten", "pt_flatten_pt_g250", "pt_flatten_pt_l250"]
mods                    = ["CNN","CNN_2D","CNN_conc","CNN_2D_conc","transformer","LSTM","LSTM_DNN","CNN_2D_LSTM","CNN_2D_LSTM_conc","CNN_2D_LSTM","TROTA"]
cuts                    = ["","_0_pt","_200_pt","_300_pt"]
n_PFCs                  = 20
models                  = {}
# models["base"]          = tf.keras.models.load_model(f"{path_to_model_folder}/model_base.h5")
# print(path_to_model_folder+"model_base2.h5")

#models["base"]         = tf.keras.models.load_model(path_to_model_folder+"model.h5")
# models["score2"]        = tf.keras.models.load_model(folder_model_antimo+antimo_model_name_H)
models["scoreDNN"]      = tf.keras.models.load_model(folder_model_antimo+antimo_model_name_L)

keys=[]
for mod in mods:
    for cut in cuts:
        key=f"{n_PFCs}_{mod}{cut}"
        if os.path.isfile(f"{path_to_model_folder}/model_{key}.h5"):
            keys.append(key)

for key in keys:
    if os.path.isfile(f"{path_to_model_folder}/model_{key}.h5"):
        models[key]         = tf.keras.models.load_model(f"{path_to_model_folder}/model_{key}.h5")


year=2022




class nanoTopevaluate_MultiScore(Module):
    def __init__(self, isMC=1):
        self.isMC = isMC
        pass


    def beginJob(self):
        pass


    def beginFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):
        self.out = wrappedOutputTree
        
        "Branch scores to tree"
        # High Pt
        # self.out.branch("TopMixed_score2", "F", lenVar="nTopMixed")
        for key in keys:
            self.out.branch(f"TopMixed_TopScore_{key}", "F", lenVar="nTopMixed")

        # Low Pt
        self.out.branch("TopResolved_TopScore", "F", lenVar="nTopResolved")


    def endFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):
        pass


    def analyze(self, event):
        """process event, return True (go to next module) or False (fail, go to next event)"""
        
        jets     = Collection(event,"Jet")
        njets    = len(jets)
        fatjets  = Collection(event,"FatJet")
        nfatjets = len(fatjets)

        goodjets, goodfatjets = presel(jets, fatjets)
        ngoodjets             = len(goodjets)
        ngoodfatjets          = len(goodfatjets)

        PFCands               = Collection(event,"PFCands")
        top_PFC_idx           = Collection(event,"Indexes")
        #n_PFCs                = 20
        tophighpt             = Collection(event, "TopMixed")
        toplowpt              = Collection(event, "TopResolved")

        
        # loop su High Pt candidates per valutare lo score con i modelli corrispondenti
        fj_dnn      = np.zeros((int(len(tophighpt)), 9)) 
        jets_dnn    = np.zeros((int(len(tophighpt)), 3, 8))   
        PFC_dnn     = np.zeros((int(len(tophighpt)),n_PFCs,13))     
        mass_dnn    = np.zeros((len(tophighpt), 3))

         

        for i, top in enumerate(tophighpt):
            PFCs=[]
            indexes=[]
            for idx in top_PFC_idx:    
                #print(idx.idxPFC)
                indexes.append(idx.idxPFC)

            #print(indexes)
            #print(idx.idxPFC)

            start_index = indexes.index(-(i+1))
            end_index = indexes.index(-(i+2))
            idx_to_append = indexes[start_index+1:end_index]
            for particle in PFCands: #ciclo sulle particles
                if particle.Idx in idx_to_append:
                    PFCs.append(particle)
            
            PFC_dnn    = fill_PFCs(n_PFCs=n_PFCs,
                                    PFCs_dnn=PFC_dnn, 
                                    PFCs=PFCs, 
                                    idx_top=i,
                                    pt_top=top.pt,
                                    eta_top=top.eta,
                                    phi_top=top.phi,
                                    M_top=top.mass)
            if top.idxJet2==-1:
                j0, j1      = goodjets[top.idxJet0],goodjets[top.idxJet1]
                fj          = goodfatjets[top.idxFatJet]
                sumjet      = j0.p4()+j1.p4()
                jets_dnn    = fill_jets(jets_dnn = jets_dnn, j0=j0, j1=j1, j2=0, sumjet = sumjet,  fj_phi= fj.phi, fj_eta=fj.eta, idx_top=i)
                fj_dnn      = fill_fj(fj_dnn, fj, i)
                mass_dnn    = fill_mass(mass_dnn=mass_dnn, idx_top=i, j0=j0, j1=j1, j2 =None, fj = fj)
            elif top.idxFatJet==-1:
                j0, j1, j2  = goodjets[top.idxJet0],goodjets[top.idxJet1],goodjets[top.idxJet2]
                fj          = ROOT.TLorentzVector()
                fj.SetPtEtaPhiM(0,0,0,0)
                sumjet      = j0.p4()+j1.p4()+j2.p4()
                jets_dnn    = fill_jets(jets_dnn, j0, j1, j2, sumjet, fj.Phi(), fj.Eta(), i)
                mass_dnn    = fill_mass(mass_dnn=mass_dnn, idx_top=i, j0=j0, j1=j1, j2 =j2, fj = None)
            else:
                j0, j1, j2  = goodjets[top.idxJet0],goodjets[top.idxJet1],goodjets[top.idxJet2]
                fj          = goodfatjets[top.idxFatJet]
                sumjet      = j0.p4() + j1.p4() +j2.p4()
                jets_dnn    = fill_jets(jets_dnn, j0, j1, j2, sumjet, fj.phi, fj.eta, i)
                fj_dnn      = fill_fj(fj_dnn, fj, i)
                mass_dnn    = fill_mass(mass_dnn=mass_dnn, idx_top=i, j0=j0, j1=j1, j2 =j2, fj = fj)



        ####### SCORES ####### 
        # Calculate Scores for several models #
        scores = {}
        
        
        if len(tophighpt)!=0:
            # top_score2      = models["score2"].predict({"fatjet":fj_dnn, "jet": jets_dnn,  "top_mass": mass_dnn[:,:2]}).flatten().tolist()
            for key in keys:
                scores[key] = models[key]({"fatjet": fj_dnn, "jet": jets_dnn, "PFC":PFC_dnn, "top": mass_dnn}).numpy().flatten().tolist()

        else:
            # top_score2  = []
            for key in keys:
                scores[key] = []

        # Branch the scores calculated #
        # self.out.fillBranch("TopHighPt_score2", top_score2)
        for key in keys:
            self.out.fillBranch(f"TopMixed_TopScore_{key}", scores[key])


        # loop su Low Pt candidates per valutare lo score con i modelli corrispondenti
        
        jets_dnn = np.zeros((int(len(toplowpt)), 3, 8))        
        for i, top in enumerate(toplowpt):
            j0, j1, j2 = goodjets[top.idxJet0],goodjets[top.idxJet1],goodjets[top.idxJet2]
            fj = ROOT.TLorentzVector()
            fj.SetPtEtaPhiM(0,0,0,0)
            sumjet = j0.p4()+j1.p4()+j2.p4()
            jets_dnn = fill_jets(jets_dnn, j0, j1, j2, sumjet, fj.Phi(), fj.Eta(), i)
        if len(toplowpt)!=0:
            top_score_DNN = models["scoreDNN"]({"jet0": jets_dnn[:,0,:-2], "jet1": jets_dnn[:,1,:-2], "jet2": jets_dnn[:,2,:-2]}).numpy().flatten().tolist()
        else:
            top_score_DNN = []

        self.out.fillBranch("TopResolved_TopScore", top_score_DNN)
        return True



from concurrent.futures import thread
import os
import sys
import ROOT
import math
from array import array
import numpy as np
import ROOT
import numpy as np
from PhysicsTools.NanoAODTools.postprocessing.framework.datamodel import Collection, Object, Event
from PhysicsTools.NanoAODTools.postprocessing.framework.eventloop import Module
from PhysicsTools.NanoAODTools.postprocessing.tools import *
from PhysicsTools.NanoAODTools.postprocessing.framework.treeReaderArrayTools import *
import pickle as pkl
import matplotlib.pyplot as plt
import mplhep as hep
hep.style.use(hep.style.CMS)
import json
from tqdm import tqdm


######### Create arguments to insert from shell #########
from argparse import ArgumentParser
parser                      = ArgumentParser()
parser.add_argument("-year",                                dest="year",                                default=2018,               required=False,         type=int,       help="year of the dataset, to select the correct variables")
parser.add_argument("-component",                           dest="component",                           default=None,               required=True,          type=str,       help="component to run")
parser.add_argument("-inFile_to_open",                      dest="inFile_to_open",                      default=None,               required=True,          type=str,       help="path to root file to run")
parser.add_argument("-path_to_pkl",                         dest="path_to_pkl",                         default="trainingSet.py",   required=False,         type=str,       help="path where save pkl to")
parser.add_argument("-nev",                                 dest="nev",                                 default=-1,                 required=False,         type=int,       help="number of events to run (defalut nev=-1, meand all events)")
parser.add_argument("-select_top_over_threshold",           dest="select_top_over_threshold",           default=False,              action="store_true",                    help="Default do not select tops above threshold")
parser.add_argument("-thr",                                 dest="thr",                                 default=0,                  required=False,         type=float,     help="score threshold to select tops above it")
parser.add_argument("-verbose",                             dest="verbose",                             default=False,              action="store_true",                    help="Default do not print")

options                     = parser.parse_args()

### ARGS ###
year                        = options.year
component                   = options.component
inFile_to_open              = options.inFile_to_open
nev                         = options.nev    
path_to_pkl                 = options.path_to_pkl
select_top_over_threshold   = options.select_top_over_threshold
thr                         = options.thr
verbose                     = options.verbose

if verbose:
    print(f"year:                           {year}")
    print(f"component:                      {component}")
    print(f"inFile_to_open:                 {inFile_to_open}")
    print(f"nev:                            {nev}")
    print(f"path_to_pkl:                    {path_to_pkl}")
    print(f"select_top_over_threshold:      {select_top_over_threshold}")
    print(f"thr:                            {thr}")
    print(f"verbose:                        {verbose}")

###### UTILITIES ######

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
def get_hvrjet(hvrjets):
    return list(filter(lambda x : x.pt , hvrjets))### provo a bypassare il fatto che non eista jetId
def presel_hvr(jets, fatjets,hvrjets): #returns 2 collections of jets and fatjets
    goodjets = get_jet(jets)
    goodfatjets = get_fatjet(fatjets)
    goodhvrjets = get_hvrjet(hvrjets)
    
    return goodjets, goodfatjets, goodhvrjets
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

def top1hvrj(hvrj):
    p4 = hvrj.p4()
    #print(p4, p4.M())
    return p4

def fill_mass(mass_dnn, idx_top, j0, j1, j2, fj, hvrj, variables_cluster):
    if j2 != None:
        if fj == None and hvrj == None: 
        #3j0fj
            top = j0.p4()+j1.p4()+j2.p4()
            mass_dnn[idx_top, 0] = (j0.p4()+j1.p4()+j2.p4()).M()
            mass_dnn[idx_top, 1] = (j0.p4()+j1.p4()+j2.p4()).M()
            mass_dnn[idx_top, 2] = (j0.p4()+j1.p4()+j2.p4()).Pt()
        elif fj!=None and hvrj == None:
        #3j1fj
            mass_dnn[idx_top, 0] = (j0.p4()+j1.p4()+j2.p4()).M()
            top = top3j1fj(fj, j0, j1, j2)
            mass_dnn[idx_top, 1] = top.M()
            mass_dnn[idx_top, 2] = top.Pt()
      
    elif j2 == None:
        if fj!=None and hvrj == None:
        #2j1fj
            mass_dnn[idx_top, 0] = (j0.p4()+j1.p4()).M()
            top = top2j1fj(fj, j0, j1)
            mass_dnn[idx_top, 1] = top.M()
            mass_dnn[idx_top, 2] = top.Pt()

    if hvrj!=None:
    #1hvrj
        mass_dnn[idx_top, 0] = (hvrj.p4()).M()
        top = top1hvrj(hvrj)
        mass_dnn[idx_top, 1] = top.M()
        mass_dnn[idx_top, 2] = top.Pt()

    return mass_dnn

def fill_fj(fj_dnn, fj, idx_top):
    if year==2018: 
        fj_dnn[idx_top, 0]  = fj.area
        fj_dnn[idx_top, 1]  = fj.btagDeepB
        fj_dnn[idx_top, 2]  = fj.particleNet_TvsQCD #li metto 
        fj_dnn[idx_top, 3]  = fj.particleNet_WvsQCD
        fj_dnn[idx_top, 4]  = fj.particleNet_QCD
        fj_dnn[idx_top, 5]  = fj.deepTag_QCDothers
        fj_dnn[idx_top, 6]  = fj.eta
        fj_dnn[idx_top, 7]  = fj.mass
        fj_dnn[idx_top, 8]  = fj.phi
        fj_dnn[idx_top, 9]  = fj.pt
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

def fill_hvrj(hvrj_dnn, hvrj, idx_top):
    if year==2018: 
        hvrj_dnn[idx_top, 0]  = hvrj.area
        hvrj_dnn[idx_top, 1]  = hvrj.scoreBDT
        hvrj_dnn[idx_top, 2]  = hvrj.tau3_over_tau2
        hvrj_dnn[idx_top, 3]  = hvrj.tau2_over_tau1
        hvrj_dnn[idx_top, 4]  = hvrj.nsubjets
        hvrj_dnn[idx_top, 5]  = hvrj.eta
        hvrj_dnn[idx_top, 6]  = hvrj.mass
        hvrj_dnn[idx_top, 7] = hvrj.phi
        hvrj_dnn[idx_top, 8] = hvrj.pt
    elif year==2022: 
        hvrj_dnn[idx_top, 0]  = hvrj.area
        hvrj_dnn[idx_top, 1]  = hvrj.btagDeepB
        hvrj_dnn[idx_top, 2]  = hvrj.particleNetWithMass_QCD
        hvrj_dnn[idx_top, 3]  = hvrj.particleNetWithMass_TvsQCD
        hvrj_dnn[idx_top, 4]  = hvrj.particleNetWithMass_WvsQCD
        hvrj_dnn[idx_top, 5]  = hvrj.eta
        hvrj_dnn[idx_top, 6]  = hvrj.mass
        hvrj_dnn[idx_top, 7]  = hvrj.phi
        hvrj_dnn[idx_top, 8]  = hvrj.pt
    return hvrj_dnn

def fill_jets(jets_dnn, j0, j1, j2, sumjet, fj_phi, fj_eta, hvrj_phi, hvrj_eta, idx_top): 
    if year==2018:
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
            jets_dnn[idx_top, 2, 8] = deltaPhi(j2.phi, hvrj_phi)#j0.#deltaphi hvrj-jet
            jets_dnn[idx_top, 2, 9] = deltaEta(j2.eta, hvrj_eta)#j0.#deltaeta hvrj-jet
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




######### INIT #########
categories    = ["3j1fj", "3j0fj", "2j1fj", "1hvrj"]
rfile         = ROOT.TFile.Open(inFile_to_open)
#tree          = InputTree(rfile.Get("Events"))
tree          = InputTree(rfile.Get("Friends"))
doLoop        = True
# Skip if empty file
if tree.GetEntries()==0:
    doLoop    = False
# Set number of events to run    
if nev==-1:
    nev       = tree.GetEntries()
# Initialize output dataset
output        = {component: {cat: 0 for cat in categories}}


###### LOOP on single tree ######
if doLoop:
    if year==2018:
        data_jets      = np.zeros((1,3,10))
        data_fatjets   = np.zeros((1,10))
        data_hvrjets   = np.zeros((1,9))

    elif year==2022:
        data_jets      = np.zeros((1,3,8))
        data_fatjets   = np.zeros((1,9))
    data_mass      = np.zeros((1,3)) #2 di mass e 1 di top
    data_label     = np.zeros((1,1))
    event_category = np.zeros((1,1))
    if verbose:
        print(f"Starting event loop for component:\t{component}")
    for i in range(nev):
        print(f"Event:\t{i}")
        if verbose:
            print(f"Event:\t{i}")
        event      = Event(tree, i)
        jets       = Collection(event,"selectedJets_nominal")
        fatjets    = Collection(event,"selectedFatJets_nominal")
        hvrjets    = Collection(event,"selectedHOTVRJets_nominal")
        # tops       = Collection(event, "TopHighPt")
        tops       = Collection(event, "TopMixed")
        ntops      = len(tops)
        goodjets, goodfatjets, goodhvrjets = presel_hvr(jets, fatjets, hvrjets) 
        variables_cluster     = None
        if verbose:
            print(f"len(goodjets):\t{len(goodjets)}\tlen(goodfatjets):\t{len(goodfatjets)}\tlen(goodhvtjets):\t{len(goodhvrjets)}")
            print(f"ntops:\t{ntops}")
        if ntops==0: 
            continue    
        for t in tops:
            if select_top_over_threshold: # AGGIUSTA NOME DATO ALLO SCORE, ALTRIMENTI DA ERRORE
                if t.score_base<thr:
                    continue
                # pass
            best_top_category       = topcategory(t)
            print(t.idxHOTVRJet)
            if year==2018:
                jet_toappend            = np.zeros((1,3,10))
                fatjet_toappend         = np.zeros((1,10))
                hvrjet_toappend         = np.zeros((1,9))
            elif year==2022:
                jet_toappend            = np.zeros((1,3,8))
                fatjet_toappend         = np.zeros((1,9))
            mass_toappend           = np.zeros((1,3))
            label_toappend          = np.zeros((1,1))
            event_category_toappend = np.zeros((1,1))
            if t.truth!=-1:
                print("top cat",best_top_category)
                if best_top_category == 0: #3j1fj0hvrj
                    #print(t.idxHOTVRJet)
                    hvrj            = ROOT.TLorentzVector()
                    hvrj.SetPtEtaPhiM(0,0,0,0)
                    fj              = goodfatjets[t.idxFatJet]
                    j0, j1, j2      = goodjets[t.idxJet0], goodjets[t.idxJet1], goodjets[t.idxJet2]
                   
                    fatjet_toappend = fill_fj(fj_dnn=fatjet_toappend,
                                            fj=fj,
                                            idx_top=0
                                            )
                    jet_toappend    = fill_jets(jets_dnn=jet_toappend,
                                                j0=j0,
                                                j1=j1,
                                                j2=j2,
                                                sumjet=(j0.p4()+j1.p4()+j2.p4()),
                                                fj_phi=fj.phi,
                                                fj_eta=fj.eta,
                                                hvrj_phi=hvrj.Phi(),
                                                hvrj_eta=hvrj.Eta(),
                                                idx_top=0
                                                )
                    mass_toappend   = fill_mass(mass_dnn=mass_toappend,
                                                idx_top=0,
                                                j0=j0,
                                                j1=j1,
                                                j2=j2,
                                                fj=fj,
                                                hvrj=None,
                                                variables_cluster=variables_cluster
                                                )
                    if not "QCD" in component :
                        label_toappend[0] = truth(fj=fj,
                                                j0=j0,
                                                j1=j1,
                                                j2=j2
                                                ) 
                    event_category_toappend[0] = best_top_category

               
                

                elif best_top_category == 1: #3j0fj0hvrj
                    #print(t.idxHOTVRJet)
                    hvrj            = ROOT.TLorentzVector()
                    hvrj.SetPtEtaPhiM(0,0,0,0)
                    fj              = ROOT.TLorentzVector()
                    fj.SetPtEtaPhiM(0,0,0,0)
                    j0, j1, j2      = goodjets[t.idxJet0], goodjets[t.idxJet1], goodjets[t.idxJet2]
                    jet_toappend    = fill_jets(jets_dnn=jet_toappend,
                                                j0=j0,
                                                j1=j1,
                                                j2=j2,
                                                sumjet=(j0.p4()+j1.p4()+j2.p4()),
                                                fj_phi=fj.Phi(),
                                                fj_eta=fj.Eta(),
                                                hvrj_phi=hvrj.Phi(),
                                                hvrj_eta=hvrj.Eta(),
                                                idx_top=0
                                                )
                    mass_toappend   = fill_mass(mass_dnn=mass_toappend,
                                                idx_top=0,
                                                j0=j0,
                                                j1=j1,
                                                j2=j2,
                                                fj=None,
                                                hvrj=None,
                                                variables_cluster=variables_cluster
                                                )
                    if not "QCD" in component: 
                        label_toappend[0] = truth(
                                                j0=j0,
                                                j1=j1,
                                                j2=j2
                                                ) 
                    event_category_toappend[0] = best_top_category
                
                


                elif best_top_category == 2: #2j1fj0hvrj
                    #print(t.idxHOTVRJet)
                    hvrj            = ROOT.TLorentzVector()
                    hvrj.SetPtEtaPhiM(0,0,0,0)
                    fj              = goodfatjets[t.idxFatJet]
                    j0, j1      = goodjets[t.idxJet0], goodjets[t.idxJet1]
                   
                    fatjet_toappend = fill_fj(fj_dnn=fatjet_toappend,
                                            fj=fj,
                                            idx_top=0
                                            )
                    jet_toappend    = fill_jets(jets_dnn=jet_toappend,
                                                j0=j0,
                                                j1=j1,
                                                j2=0,
                                                sumjet=(j0.p4()+j1.p4()),
                                                fj_phi=fj.phi,
                                                fj_eta=fj.eta,
                                                hvrj_phi=hvrj.Phi(),
                                                hvrj_eta=hvrj.Eta(),
                                                idx_top=0
                                                )
                    mass_toappend   = fill_mass(mass_dnn=mass_toappend,
                                                idx_top=0,
                                                j0=j0,
                                                j1=j1,
                                                j2=None,
                                                fj=fj,
                                                hvrj=None,
                                                variables_cluster=variables_cluster
                                                )
                    if not "QCD" in component: 
                        label_toappend[0] = truth(fj=fj,
                                                j0=j0,
                                                j1=j1,
                                                ) 
                    event_category_toappend[0] = best_top_category

                elif best_top_category == 3: #1hvrj
                    #print(t.idxHOTVRJet)
                    hvrj            = goodhvrjets[t.idxHOTVRJet]
                    fj              = ROOT.TLorentzVector()
                    fj.SetPtEtaPhiM(0,0,0,0)
                    j0           = ROOT.TLorentzVector()
                    j1           = ROOT.TLorentzVector()
                    j0.SetPtEtaPhiM(0,0,0,0)
                    j1.SetPtEtaPhiM(0,0,0,0)
                    
                    hvrjet_toappend = fill_hvrj(hvrj_dnn=hvrjet_toappend, 
                                                hvrj=hvrj,  
                                                idx_top=0
                                                )
                    
                    mass_toappend   = fill_mass(mass_dnn=mass_toappend,
                                                idx_top=0,
                                                j0=None,
                                                j1=None,
                                                j2=None,
                                                fj=None,
                                                hvrj=hvrj,
                                                variables_cluster=variables_cluster
                                                )
                    if not "QCD" in component: 
                        label_toappend[0] = truth(hvrj=hvrj) 
                    event_category_toappend[0] = best_top_category
            
            # append single-top information to all-tops information
            data_jets       = np.append(data_jets,      jet_toappend,            axis = 0)
            data_fatjets    = np.append(data_fatjets,   fatjet_toappend,         axis = 0)
            data_hvrjets    = np.append(data_hvrjets,   hvrjet_toappend,         axis = 0)
            #print("data", data_mass,"\nto append", mass_toappend)
            data_mass       = np.append(data_mass,      mass_toappend,           axis = 0)
            if (label_toappend[0]==2 and verbose): 
                print(component, i, label_toappend)
            data_label      = np.append(data_label,     label_toappend,          axis=0)
            event_category  = np.append(event_category, event_category_toappend, axis=0)
            if (data_jets[0, 0, 0]==0):
                data_jets       = np.delete(data_jets,      0, axis = 0)
                data_fatjets    = np.delete(data_fatjets,   0, axis = 0)
                data_hvrjets    = np.delete(data_hvrjets,   0, axis = 0)
                data_mass       = np.delete(data_mass,      0, axis = 0)
                data_label      = np.delete(data_label,     0, axis = 0)
                event_category  = np.delete(event_category, 0, axis = 0)
                
    # fill output
    event_category = event_category.flatten()
    for cat in categories:
        if "3j1fj" in cat :
            n = 0
        elif "3j0fj" in cat :
            n = 1
        elif "2j1fj" in cat :
            n = 2
        elif "1hvrj" in cat :
            n = 3
            
        output[component][cat] = [data_jets[event_category == n], data_fatjets[event_category == n], data_hvrjets[event_category == n], data_mass[event_category == n], data_label[event_category == n]]
        print(f"Component: {component}, Category: {cat}")
        print(f"Number of True Tops:    {len([i for i, x in enumerate(output[component][cat][4]==1) if x==True])}")
        print(f"Number of False Tops:   {len([i for i, x in enumerate(output[component][cat][4]==0) if x==True])}")
        print(f"Number of Jets:         {len(output[component][cat][0])}")
        print(f"Number of FatJets:      {len(output[component][cat][1])}")
        print(f"Number of HOTVRJets:    {len(output[component][cat][2])}")
        print(f"Number of Tops:         {len(output[component][cat][3])}")
        print("\n")
    rfile.Close()
    
if path_to_pkl is not None:
    print(path_to_pkl)
    with open(path_to_pkl, "wb") as f:
        pkl.dump(obj=output, file=f)

        
'''elif best_top_category == 2 and truth(j0=j0, j1=j1, j2=j2)!=-1: #3j0fj
                hvrj            = ROOT.TLorentzVector()
                hvrj.SetPtEtaPhiM(0,0,0,0)
                fj              = ROOT.TLorentzVector()
                fj.SetPtEtaPhiM(0,0,0,0)
                j0, j1, j2      = goodjets[t.idxJet0], goodjets[t.idxJet1], goodjets[t.idxJet2]
                jet_toappend    = fill_jets(jets_dnn=jet_toappend,
                                            j0=j0,
                                            j1=j1,
                                            j2=j2,
                                            sumjet=(j0.p4()+j1.p4()+j2.p4()),
                                            fj_phi=fj.Phi(),
                                            fj_eta=fj.Eta(),
                                            hvrj_phi=hvrj.Phi(),
                                            hvrj_eta=hvrj.Eta(),
                                            idx_top=0
                                            )
                mass_toappend   = fill_mass(mass_dnn=mass_toappend,
                                            idx_top=0,
                                            j0=j0,
                                            j1=j1,
                                            j2=j2,
                                            fj=None,
                                            hvrj=None,
                                            variables_cluster=variables_cluster
                                            )
                if not "QCD" in component: 
                    label_toappend[0] = truth(j0=j0,
                                              j1=j1,
                                              j2=j2
                                              ) 
                event_category_toappend[0] = best_top_category'''
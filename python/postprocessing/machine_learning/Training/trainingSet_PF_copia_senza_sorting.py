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
import time

start_time = time.time()
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
parser.add_argument('-n', '--n_PFCs',                       dest = 'n_PFCs',                            required = True,            default = 20,           type = int,     help = 'number of particles used for training (default "20")')
parser.add_argument('-pt', '--pt_cut',                      dest = 'pt_cut',                            required = True,            default = 0,            type = float,   help = 'pt cut for particles used for training (default "0")')

options                     = parser.parse_args()

### ARGS ###
year                        = options.year
component                   = options.component
inFile_to_open              = options.inFile_to_open
nev                         = options.nev    
path_to_pkl                 = options.path_to_pkl
select_top_over_threshold   = options.select_top_over_threshold
thr                         = options.thr
n_PFCs                      = options.n_PFCs
pt_cut                      = options.pt_cut
verbose                     = options.verbose

if verbose:
    print(f"year:                           {year}")
    print(f"component:                      {component}")
    print(f"inFile_to_open:                 {inFile_to_open}")
    print(f"nev:                            {nev}")
    print(f"path_to_pkl:                    {path_to_pkl}")
    print(f"select_top_over_threshold:      {select_top_over_threshold}")
    print(f"thr:                            {thr}")
    print(f"n_PFCs:                         {n_PFCs}")
    print(f"pt_cut:                         {pt_cut}")
    print(f"verbose:                        {verbose}")

###### UTILITIES ######
def fill_mass(mass_dnn, idx_top, j0, j1, j2, fj, variables_cluster):
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

#fai un boost e porta eta e phi nel sistema di riferimento del top
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
            PFCs_dnn[idx_top, i, 4] = particle.d0
            PFCs_dnn[idx_top, i, 5] = particle.dz
            PFCs_dnn[idx_top, i, 6] = particle.JetDeltaR
            PFCs_dnn[idx_top, i, 7] = particle.FatJetDeltaR
            PFCs_dnn[idx_top, i, 8] = particle.charge
            PFCs_dnn[idx_top, i, 9] = particle.pdgId
            PFCs_dnn[idx_top, i, 10] = particle.pvAssocQuality  
            PFCs_dnn[idx_top, i, 11] = particle.IsInJet
            PFCs_dnn[idx_top, i, 12] = particle.IsInFatJet
    return PFCs_dnn
    


######### INIT #########
categories    = ["3j0fj", "3j1fj", "2j1fj"]
rfile         = ROOT.TFile.Open(inFile_to_open)
#print("\nprova type tree\n",type(rfile.Get("Events")),"\n")
tree          = InputTree(rfile.Get("Events"))
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
        data_jets      = np.zeros((1,3,8))
        data_fatjets   = np.zeros((1,12))
    elif year==2022:        
        data_jets           = np.zeros((1,3,8))
        data_fatjets        = np.zeros((1,9))
        #mergia jet e fatjet e salvane sui 40 !!senza overlap e controlla l'ordinamento in pt eindice di distanza e se appatriene ejet fgj o entrambi
        data_PFC         = np.zeros((1,n_PFCs,13)) #!! setta il masssimo delle 20 da prendere e andranno usate LSTM
    data_mass      = np.zeros((1,3))
    data_label     = np.zeros((1,1))
    event_category = np.zeros((1,1))
    if verbose:
        print(f"Starting event loop for component:\t{component}")
    for i in range(nev):
        #print(f"Event:\t{i}")
        if verbose:
            print(f"Event:\t{i}")
        event        = Event(tree, i)
        jets         = Collection(event, "Jet")
        fatjets      = Collection(event, "FatJet")
        # tops       = Collection(event, "TopHighPt")
        tops         = Collection(event, "TopMixed")
        ntops        = len(tops)
        PFCands      = Collection(event,"PFCands")
        top_PFC_idx  = Collection(event,"Indexes")
        #presel toglibile se vogliamo
        goodjets, goodfatjets = presel(jets, fatjets)
        variables_cluster     = None
        if verbose:
            print(f"len(goodjets):\t{len(goodjets)}\tlen(goodfatjets):\t{len(goodfatjets)}")
            print(f"ntops:\t{ntops}")
        if ntops==0: 
            continue   
        for top_num, t in enumerate(tops):
            if t.pt>=pt_cut:
                if select_top_over_threshold: # AGGIUSTA NOME DATO ALLO SCORE, ALTRIMENTI DA ERRORE
                    if t.score_base<thr:
                        continue
                    # pass
                best_top_category       = topcategory(t)
                
                if year==2018:
                    jet_toappend            = np.zeros((1,3,8))
                    fatjet_toappend         = np.zeros((1,12))
                elif year==2022:
                    jet_toappend            = np.zeros((1,3,8))
                    fatjet_toappend         = np.zeros((1,9))
                    PFC_toappend         = np.zeros((1,n_PFCs,13))
                mass_toappend           = np.zeros((1,3))
                label_toappend          = np.zeros((1,1))
                event_category_toappend = np.zeros((1,1))

                PFCs=[]
                indexes=[]
                for idx in top_PFC_idx:    
                    #print(idx.idxPFC)
                    indexes.append(idx.idxPFC)

                #print(indexes)
                #print(idx.idxPFC)

                start_index = indexes.index(-(top_num+1))
                end_index = indexes.index(-(top_num+2))
                idx_to_append = indexes[start_index+1:end_index]
                for particle in PFCands: #ciclo sulle particles
                    if particle.Idx in idx_to_append:
                        PFCs.append(particle)
                if t.truth!=-1:
                    PFC_toappend    = fill_PFCs(n_PFCs=n_PFCs,
                                            PFCs_dnn=PFC_toappend, 
                                            PFCs=PFCs, 
                                            idx_top=0,
                                            pt_top=t.pt,
                                            eta_top=t.eta,
                                            phi_top=t.phi,
                                            M_top=t.mass)        
                    
                    if best_top_category == 0: #3j1fj
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
                                                    idx_top=0
                                                    )
                        mass_toappend   = fill_mass(mass_dnn=mass_toappend,
                                                    idx_top=0,
                                                    j0=j0,
                                                    j1=j1,
                                                    j2=j2,
                                                    fj=fj,
                                                    variables_cluster=variables_cluster
                                                    )
                        
                        if not "QCD" in component:
                            label_toappend[0] = truth(fj=fj,
                                                    j0=j0,
                                                    j1=j1,
                                                    j2=j2
                                                    ) 
                        event_category_toappend[0] = best_top_category
                        
                    elif best_top_category == 1: #3j0fj
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
                                                    idx_top=0
                                                    )
                        mass_toappend   = fill_mass(mass_dnn=mass_toappend,
                                                    idx_top=0,
                                                    j0=j0,
                                                    j1=j1,
                                                    j2=j2,
                                                    fj=None,
                                                    variables_cluster=variables_cluster
                                                    )
                        if not "QCD" in component: 
                            label_toappend[0] = truth(j0=j0,
                                                    j1=j1,
                                                    j2=j2
                                                    ) 
                        event_category_toappend[0] = best_top_category
                    else: #2j1fj
                        fj              = goodfatjets[t.idxFatJet]
                        j0, j1          = goodjets[t.idxJet0], goodjets[t.idxJet1]

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
                                                    idx_top=0
                                                    )
                        mass_toappend   = fill_mass(mass_dnn=mass_toappend,
                                                    idx_top=0,
                                                    j0=j0,
                                                    j1=j1,
                                                    j2=None,
                                                    fj=fj,
                                                    variables_cluster=variables_cluster
                                                    )
                        if not "QCD" in component: 
                            label_toappend[0] = truth(fj=fj,
                                                    j0=j0,
                                                    j1=j1
                                                    ) 
                        event_category_toappend[0] = best_top_category
                
                # append single-top information to all-tops information
                data_jets         = np.append(data_jets,      jet_toappend,            axis = 0)
                data_fatjets      = np.append(data_fatjets,   fatjet_toappend,         axis = 0)
                data_PFC          = np.append(data_PFC,       PFC_toappend,            axis = 0)
                #print("data", data_mass,"\nto append", mass_toappend)
                data_mass       = np.append(data_mass,      mass_toappend,           axis = 0)
                if (label_toappend[0]==2 and verbose): 
                    print(component, i, label_toappend)
                data_label      = np.append(data_label,     label_toappend,          axis=0)
                event_category  = np.append(event_category, event_category_toappend, axis=0)
                if (data_jets[0, 0, 0]==0):
                    data_jets       = np.delete(data_jets,      0, axis = 0)
                    data_fatjets    = np.delete(data_fatjets,   0, axis = 0)
                    data_PFC        = np.delete(data_PFC,       0, axis = 0)
                    data_mass       = np.delete(data_mass,      0, axis = 0)
                    data_label      = np.delete(data_label,     0, axis = 0)
                    event_category  = np.delete(event_category, 0, axis = 0)
                    
    # fill output
    event_category = event_category.flatten()
    for cat in categories:
        if "0fj" in cat :
            n = 1
        elif "2j" in cat :
            n = 2
        else:
            n = 0
        output[component][cat] = [data_jets[event_category == n], data_fatjets[event_category == n], data_PFC[event_category == n],  data_mass[event_category == n], data_label[event_category == n]]
        #output[component][cat] = [data_PFC[event_category == n], data_fatPFC[event_category == n], data_mass[event_category == n], data_label[event_category == n]]

    rfile.Close()
    
if path_to_pkl is not None:
    print(path_to_pkl)
    with open(path_to_pkl, "wb") as f:
        pkl.dump(obj=output, file=f)

end_time = time.time()
execution_time = end_time - start_time
print(f"Tempo di esecuzione: {execution_time:.5f} secondi")
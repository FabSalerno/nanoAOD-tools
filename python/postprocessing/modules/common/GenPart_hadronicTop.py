import ROOT
import math
import numpy as np
#from datetime import datetime
ROOT.PyConfig.IgnoreCommandLineOptions = True
#from PhysicsTools.NanoAODTools.postprocessing.samples.samples import *
from PhysicsTools.NanoAODTools.postprocessing.framework.datamodel import Collection, Object
from PhysicsTools.NanoAODTools.postprocessing.framework.eventloop import Module
from PhysicsTools.NanoAODTools.postprocessing.tools import *
#from PhysicsTools.NanoAODTools.postprocessing.skimtree_utils import *

def Conversion_bitwise(num):
    k=15
    a=np.ones(k)
    for j in range(k,0):
        conv=0
        for i in range(0,k): 
            conv = conv + a[i]*pow(2,i)
        if num<conv: a[j]=0
        else:
            a[j+1]=1
            a[j]=0
    return a

class GenPart_hadronicTop(Module):
    def __init__(self,isMC=1,flavour=None):
        self.isMC = isMC
        self.flavour=flavour
        pass
    def beginJob(self):
        pass
    def endJob(self):
        pass
    def beginFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):
        self.out = wrappedOutputTree
        self.out.branch("GenPart_hadronicTop","I", lenVar="nGenPart")

    def endFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):
        pass

    def analyze(self, event):
        #t0 = datetime.now()
        """process event, return True (go to next module) or False (fail, go to next event)"""
        if self.isMC==0: return False
        genpart = Collection(event, "GenPart")
        hadronic_top = np.zeros(len(genpart), dtype=int)
        quark_flavs = [int(1),int(2),int(3),int(4)]
        tops_gen = list(filter(lambda x : abs(int(x.pdgId))==6, genpart))
        w_gen = list(filter(lambda x : abs(int(x.pdgId))==24, genpart))
        for particle in genpart:
            #Print("la particella analizzata è", particle.pdgId)
            mom_id = particle.genPartIdxMother
            #se è un quark nella catena del top
            if abs(int(particle.pdgId)) in quark_flavs and mom_id!=-1: 
                #Print("è un quark")
                #se non è la propagazione di sè stessa
                if int(genpart[mom_id].pdgId) != int(particle.pdgId):
                    mom = genpart[mom_id] 
                    grandmom_id = mom.genPartIdxMother
                    #Print("non è propagato e la madre è:",mom.pdgId)
                    #se la madre è un w
                    if abs(int(mom.pdgId))==24 and grandmom_id!=-1:
                        #Print("la madre è un w prodotto di decadimento")
                        grandmom = genpart[grandmom_id]
                        #Print("la nonna è:",grandmom.pdgId)
                        #se non è la propagazione di sè stessa
                        if int(grandmom.pdgId) != int(mom.pdgId):
                            #se la madre della w è un top
                            #Print("non è propagato")
                            if abs(grandmom.pdgId) == 6:
                                #Print("la nonna è un top")
                                top = grandmom
                                top_mom = genpart[top.genPartIdxMother]
                                #metti 1 nella posizione corrispondete al top
                                hadronic_top[top.genPartIdx]=int(1)
                                #Print("salvato indice:",hadronic_top)
                                #fai lo stesso per i top da cui è stato propagato
                                while top_mom.pdgId==top.pdgId:
                                    top=top_mom
                                    top_mom=genpart[top_mom.genPartIdxMother]
                                    hadronic_top[top.genPartIdx]=int(1)
                                    #Print("salvato indice:",hadronic_top)

                        else:
                           #Print("è propagato")
                           while (grandmom.pdgId==mom.pdgId): 
                                mom=grandmom
                                grandmom= genpart[mom.genPartIdxMother]  
                                #Print("la nuova nonna è:",grandmom.pdgId)
                                #se la madre della w è un top
                                if abs(grandmom.pdgId) == 6:
                                    top = grandmom
                                    top_mom = genpart[top.genPartIdxMother]
                                    #Print("la nonna era un top e la madre del top è:",top_mom.pdgId)
                                    #metti 1 nella posizione corrispondete al top
                                    hadronic_top[top.genPartIdx]=int(1)
                                    #Print("salvato indice:",hadronic_top)
                                    #fai lo stesso per i top da cui è stato propagato
                                    while top_mom.pdgId==top.pdgId:
                                        top=top_mom
                                        #Print("il nuovo top è:",top.pdgId)
                                        top_mom=genpart[top_mom.genPartIdxMother]
                                        #Print("la nuova madre è:",top_mom.pdgId)
                                        hadronic_top[top.genPartIdx]=int(1)
                                        #Print("salvato indice:",hadronic_top)

           
                        

                



        self.out.fillBranch("GenPart_hadronicTop", hadronic_top ) 
       
        return True



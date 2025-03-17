import ROOT
import math
#from datetime import datetime
ROOT.PyConfig.IgnoreCommandLineOptions = True

from PhysicsTools.NanoAODTools.postprocessing.framework.datamodel import Collection, Object
from PhysicsTools.NanoAODTools.postprocessing.framework.eventloop import Module
from PhysicsTools.NanoAODTools.postprocessing.tools import *

    
class pt_cut_top_gen_lvl(Module):
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
        save = False
        genpart = Collection(event, "GenPart")
        tops = list(filter(lambda x : int(x.pdgId)==6 and int(x.hadronicTop)==1, genpart))
        antitops = list(filter(lambda x : int(x.pdgId)==-6 and int(x.hadronicTop)==1, genpart))
        n_tops = len(tops)
        n_antitops = len(antitops)
        #print("event is ",event.event)
        #print("n_tops = ",n_tops)
        #print("primo top is ",tops[0].pt)
        #print("secondo top is ",tops[1].pt)
        #print("n_antitops = ",n_antitops)
        #print("primo antitop is ",antitops[0].pt)
        #print("secondo antitop is ",antitops[1].pt)
        if n_tops==0 and n_antitops==0:
            save = True
        elif (n_tops!=0 and n_antitops==0):
            for top in tops:
                if top.Pt>200 and top.genPartIdxMother==0: 
                    save = True
        elif (n_tops==0 and n_antitops!=0):
            for antitop in antitops:
                if antitop.Pt>200 and antitop.genPartIdxMother==0: 
                    save = True
        else:   
            top = ROOT.TLorentzVector()
            for t in tops:
                if t.genPartIdxMother==0:
                    top.SetPtEtaPhiM(t.pt, t.eta, t.phi, t.mass)

            antitop = ROOT.TLorentzVector()
            for antit in antitops:
                if antit.genPartIdxMother==0:
                    antitop.SetPtEtaPhiM(antit.pt, antit.eta, antit.phi, antit.mass)
                
        
            
            if top.pt>400 or antitop.pt>400:
                save = True
            else:
                save = False

        return save
    
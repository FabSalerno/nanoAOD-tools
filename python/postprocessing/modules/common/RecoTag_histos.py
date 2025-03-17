from PhysicsTools.NanoAODTools.postprocessing.framework.eventloop import Module
from PhysicsTools.NanoAODTools.postprocessing.framework.datamodel import Collection, Object
from PhysicsTools.NanoAODTools.postprocessing.framework.postprocessor import PostProcessor
from importlib import import_module
import os
import sys
import ROOT
import json
from PhysicsTools.NanoAODTools.postprocessing.tools import *
ROOT.PyConfig.IgnoreCommandLineOptions = True


class Efficiency_plot(Module):
    def __init__(self):
        self.writeHistFile = True

    def beginJob(self, histFile=None, histDirName=None):
        Module.beginJob(self, histFile, histDirName)

        self.keys = ["60_CNN_2D_0_pt","60_CNN_2D_LSTM_0_pt","60_CNN_2D_2_0_pt","60_CNN_2D_LSTM_2_0_pt"]
        self.h_recoNumber_merged = ROOT.TH1F('h_recoNumber_merged', 'h_recoNumber_merged', 20, 0, 1000)
        self.h_recoNumber_mixed = {}
        for key in self.keys:
            self.h_recoNumber_mixed[key] = ROOT.TH1F(f'h_recoNumber_mixed_{key}', f'h_recoNumber_mixed_{key}', 20, 0, 1000)
        self.h_recoNumber_resolved = ROOT.TH1F('h_recoNumber_resolved', 'h_recoNumber_resolved', 20, 0, 1000)
        self.h_hadronic_top_gen = ROOT.TH1F('h_hadronic_top_gen', 'h_hadronic_top_gen', 20, 0, 1000)
        self.h_recoTagNumber_merged = ROOT.TH1F('h_recoTagNumber_merged', 'h_recoTagNumber_merged', 20, 0, 1000)
        self.h_recoTagNumber_merged_high_pt_thr = ROOT.TH1F('h_recoTagNumber_merged_high_pt_thr', 'h_recoTagNumber_merged_high_pt_thr', 20, 0, 1000)
        self.h_recoTagNumber_merged_Antimo_thr = ROOT.TH1F('h_recoTagNumber_merged_Antimo_thr', 'h_recoTagNumber_merged_Antimo_thr', 20, 0, 1000)
        self.h_recoTagNumber_mixed = {}
        for key in self.keys:
            self.h_recoTagNumber_mixed[key] = ROOT.TH1F(f'h_recoTagNumber_mixed_{key}', f'h_recoTagNumber_mixed_{key}', 20, 0, 1000)
        self.h_recoTagNumber_resolved = ROOT.TH1F('h_recoTagNumber_resolved', 'h_recoTagNumber_resolved', 20, 0, 1000)

        self.addObject(self.h_recoNumber_merged)
        for key in self.keys:
            self.addObject(self.h_recoNumber_mixed[key])
        self.addObject(self.h_recoNumber_resolved)
        self.addObject(self.h_hadronic_top_gen)
        self.addObject(self.h_recoTagNumber_merged)
        self.addObject(self.h_recoTagNumber_merged_high_pt_thr)
        self.addObject(self.h_recoTagNumber_merged_Antimo_thr)
        for key in self.keys:
            self.addObject(self.h_recoTagNumber_mixed[key])
        self.addObject(self.h_recoTagNumber_resolved)

    def best_top_mixed(self,tops_mixed,key):
        best_top_list = []
        attr_name = f"TopScore_{key}"  
        for top in tops_mixed:
            score = getattr(top, attr_name)
            if len(best_top_list)==0:
                best_top_list.append(top)
            elif score > getattr(best_top_list[0], attr_name):
                best_top_list.append(top)
            best_top_list.sort(key=lambda x: getattr(x, attr_name), reverse=True)
            #scelgo la lista per eventualmente scegliere anche il altri top con il punteggio più alto (ad esempio per Z->4top)
        return best_top_list
    
    def best_top_resolved(self,tops_resolved):
        best_top_list = []
        for top in tops_resolved:
            if len(best_top_list)==0:
                best_top_list.append(top)
            elif top.TopScore > best_top_list[0].TopScore:
                best_top_list.append(top)
            best_top_list.sort(key=lambda x: x.TopScore, reverse=True)
            #scelgo la lista per eventualmente scegliere anche il altri top con il punteggio più alto (ad esempio per Z->4top)
        return best_top_list
    
    def best_top_merged(self,tops_merged):
        best_top_list = []
        for top in tops_merged:
            if len(best_top_list)==0:
                best_top_list.append(top)
            elif top.particleNetWithMass_TvsQCD > best_top_list[0].particleNetWithMass_TvsQCD:
                best_top_list.append(top)
            best_top_list.sort(key=lambda x: x.particleNetWithMass_TvsQCD, reverse=True)
        #scelgo la lista per eventualmente scegliere anche il altri top con il punteggio più alto (ad esempio per Z->4top)
        return best_top_list
    
    def match_best_top(self,hadronic_tops_gen,best_top):
        #in questo caso stiamo matchando un singolo top, la differenza tra top_gen pre e post gluone è minima
        radius = 0.4
        for top_gen in hadronic_tops_gen:
            delta_R = deltaR(best_top, top_gen)
            if delta_R < radius:
                return True, top_gen
            else:
                return False, None

    def match_best_top_list(self,hadronic_tops_gen,best_top_list):
        #ci sono dei potenziali problemi di doppio conteggio dei hadronic_tops_gen dovuti all'emissione di un gluone 
        radius = 0.4
        for best_top in best_top_list:
            dr_list = []
            for top_gen in hadronic_tops_gen:
                delta_R = deltaR(best_top, top_gen)
                dr_list.append(delta_R)
                if delta_R < radius:
                    return True
                else:
                    return False
                

           

    def analyze(self, event):
        #Funziona solo perchè ho un semilep, con più top adronici bisogna stare attenti
        genpart = Collection(event, "GenPart")
        hadronic_tops_gen = list(filter(lambda x : abs(int(x.pdgId))==6 and x.hadronicTop==1 and x.genPartIdxMother==0, genpart))
        ntops_gen = len(hadronic_tops_gen)
        #print(ntops_gen)
        tops_resolved = Collection(event, "TopResolved")
        ntops_resolved = len(tops_resolved)
        tops_mixed = Collection(event, "TopMixed")
        ntops_resolved = len(tops_resolved)
        tops_merged = Collection(event, "FatJet")
        ntops_merged = len(tops_merged)

        thr                = "1%"  
        threshold = {}
        for key in self.keys:    
            score_thresholds = f"/eos/user/f/fsalerno/framework/MachineLearning/thresholds/score_thresholds_{key}.json"                                          
            with open(score_thresholds, "r") as fjson:
                thresholds  = json.load(fjson)
            threshold[key]   = thresholds[thr]["thr"]


        
        best_top_list_resolved = self.best_top_resolved(tops_resolved=tops_resolved)
        match_resolved=0
        if len(best_top_list_resolved)>0:
            best_top_resolved = best_top_list_resolved[0]
            match_resolved, hadr_top_gen_matched_resolved = self.match_best_top(hadronic_tops_gen=hadronic_tops_gen,best_top=best_top_resolved)

        
        best_top_mixed={}
        best_top_list_mixed={}
        match_mixed = {}
        hadr_top_gen_matched_mixed = {}
        for key in self.keys:
            match_mixed[key]=0
            best_top_list_mixed[key] = self.best_top_mixed(tops_mixed=tops_mixed, key=key)
            if len(best_top_list_mixed[key])>0:
                best_top_mixed[key] = best_top_list_mixed[key][0]
                match_mixed[key], hadr_top_gen_matched_mixed[key] = self.match_best_top(hadronic_tops_gen=hadronic_tops_gen,best_top=best_top_mixed[key])

        best_top_list_merged = self.best_top_merged(tops_merged=tops_merged)
        match_merged=0
        if len(best_top_list_merged)>0:
            best_top_merged = best_top_list_merged[0]
            match_merged, hadr_top_gen_matched_merged = self.match_best_top(hadronic_tops_gen=hadronic_tops_gen,best_top=best_top_merged)



        TopRes_trsMed   =  0.5411276
        TopMer_trsMed =  0.8
        TopMer_trsMedAll =  0.695
        TopMer_trsMedHighPt =  0.785

        if match_merged:
            self.h_recoNumber_merged.Fill(hadr_top_gen_matched_merged.pt)
            if best_top_merged.particleNetWithMass_TvsQCD>TopMer_trsMedAll:
                self.h_recoTagNumber_merged.Fill(hadr_top_gen_matched_merged.pt)
            if best_top_merged.particleNetWithMass_TvsQCD>TopMer_trsMedHighPt:
                self.h_recoTagNumber_merged_high_pt_thr.Fill(hadr_top_gen_matched_merged.pt)
            if best_top_merged.particleNetWithMass_TvsQCD>TopMer_trsMed:
                self.h_recoTagNumber_merged_Antimo_thr.Fill(hadr_top_gen_matched_merged.pt)

        for key in self.keys:
            if match_mixed[key]:
                self.h_recoNumber_mixed[key].Fill(hadr_top_gen_matched_mixed[key].pt)
                attr_name = f"TopScore_{key}"
                if getattr(best_top_mixed[key], attr_name)>threshold[key]:
                    self.h_recoTagNumber_mixed[key].Fill(hadr_top_gen_matched_mixed[key].pt)

        if match_resolved:
            self.h_recoNumber_resolved.Fill(hadr_top_gen_matched_resolved.pt)
            if best_top_resolved.TopScore>TopRes_trsMed:
                self.h_recoTagNumber_resolved.Fill(hadr_top_gen_matched_resolved.pt)


        for had_top in hadronic_tops_gen:
            self.h_hadronic_top_gen.Fill(had_top.pt)
        return True

  


#files = ["/eos/user/f/fsalerno/Data/PF/topevaluate/nano_mcRun3_TT_semilep_MC2022_topeval_PF.root"]
files = ["/eos/user/f/fsalerno/Data/PF/topevaluate/nano_mcRun3_TT_inclusive_MC2022_topeval_PF_presel_100000.root"]
file_path="/eos/user/f/fsalerno/Evaluation/Prelim"
p = PostProcessor(".", files, cut=None, branchsel=None, modules=[
                  Efficiency_plot()], noOut=True, histFileName=f"{file_path}/recoTagNumber_histos_presel.root", histDirName="recoTagNumber")
p.run()
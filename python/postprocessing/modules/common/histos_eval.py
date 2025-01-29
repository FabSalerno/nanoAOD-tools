import ROOT
ROOT.PyConfig.IgnoreCommandLineOptions = True

from PhysicsTools.NanoAODTools.postprocessing.framework.datamodel import Collection, Object 
from PhysicsTools.NanoAODTools.postprocessing.framework.eventloop import Module

class histos_eval(Module):
    def __init__(self):
        self.writeHistFile=True
        pass

    def beginJob(self,histFile,histDirName):
        
        #self.objs = []
        #print("\n e ora?", dir(self))
        Module.beginJob(self,histFile,histDirName+"_evaluation")
        self.h_score_top_mixed_true = ROOT.TH1F("score_top_mixed_true","score_top_mixed_true",100,0,1)
        self.h_score_top_mixed_false_qcd = ROOT.TH1F("score_top_mixed_false_qcd","score_top_mixed_false_qcd",100,0,1)
        self.h_score_top_mixed_false_other = ROOT.TH1F("score_top_mixed_false_other","score_top_mixed_false_other",100,0,1)
        self.h_score_top_mixed_false_all = ROOT.TH1F("score_top_mixed_false_all","score_top_mixed_false_all",100,0,1)
        self.h_pt_top_mixed_true = ROOT.TH1F("pt_top_mixed_true","pt_top_mixed_true",100,0,1000)
        self.h_pt_top_mixed_false_qcd = ROOT.TH1F("pt_top_mixed_false_qcd","pt_top_mixed_false_qcd",100,0,1000)
        self.h_pt_top_mixed_false_other = ROOT.TH1F("pt_top_mixed_false_other","pt_top_mixed_false_other",100,0,1000)
        self.h_pt_top_mixed_false_all = ROOT.TH1F("pt_top_mixed_false_all","pt_top_mixed_false_all",100,0,1000)
        self.h_mass_top_mixed_true = ROOT.TH1F("mass_top_mixed_true","mass_top_mixed_true",100,0,1000)
        self.h_mass_top_mixed_false_qcd = ROOT.TH1F("mass_top_mixed_false_qcd","mass_top_mixed_false_qcd",100,0,1000)
        self.h_mass_top_mixed_false_other = ROOT.TH1F("mass_top_mixed_false_other","mass_top_mixed_false_other",100,0,1000)
        self.h_mass_top_mixed_false_all = ROOT.TH1F("mass_top_mixed_false_all","mass_top_mixed_false_all",100,0,1000)
        self.h_ntops_tot = ROOT.TH1F("ntops_tot","ntops_tot",6,0,6)
        self.h_score_3j1fj0hvrj_true = ROOT.TH1F("score_3j1fj0hvrj_true","score_3j1fj0hvrj_true",100,0,1)
        self.h_score_3j0fj1hvrj_true = ROOT.TH1F("score_3j0fj1hvrj_true","score_3j0fj1hvrj_true",100,0,1)
        self.h_score_3j0fj0hvrj_true = ROOT.TH1F("score_3j0fj0hvrj_true","score_3j0fj0hvrj_true",100,0,1)
        self.h_score_2j0fj1hvrj_true = ROOT.TH1F("score_2j0fj1hvrj_true","score_2j0fj1hvrj_true",100,0,1)
        self.h_score_2j1fj0hvrj_true = ROOT.TH1F("score_2j1fj0hvrj_true","score_2j1fj0hvrj_true",100,0,1)
        self.h_score_3j1fj0hvrj_false = ROOT.TH1F("score_3j1fj0hvrj_false","score_3j1fj0hvrj_false",100,0,1)
        self.h_score_3j0fj1hvrj_false = ROOT.TH1F("score_3j0fj1hvrj_false","score_3j0fj1hvrj_false",100,0,1)
        self.h_score_3j0fj0hvrj_false = ROOT.TH1F("score_3j0fj0hvrj_false","score_3j0fj0hvrj_false",100,0,1)
        self.h_score_2j0fj1hvrj_false = ROOT.TH1F("score_2j0fj1hvrj_false","score_2j0fj1hvrj_false",100,0,1)
        self.h_score_2j1fj0hvrj_false = ROOT.TH1F("score_2j1fj0hvrj_false","score_2j1fj0hvrj_false",100,0,1)
        self.addObject(self.h_score_top_mixed_true)
        self.addObject(self.h_score_top_mixed_false_qcd)
        self.addObject(self.h_score_top_mixed_false_other)
        self.addObject(self.h_score_top_mixed_false_all)
        self.addObject(self.h_pt_top_mixed_true)
        self.addObject(self.h_pt_top_mixed_false_qcd)
        self.addObject(self.h_pt_top_mixed_false_other)
        self.addObject(self.h_pt_top_mixed_false_all)
        self.addObject(self.h_mass_top_mixed_true)
        self.addObject(self.h_mass_top_mixed_false_qcd)
        self.addObject(self.h_mass_top_mixed_false_other)
        self.addObject(self.h_mass_top_mixed_false_all)
        self.addObject(self.h_ntops_tot)
        self.addObject(self.h_score_3j1fj0hvrj_true)
        self.addObject(self.h_score_3j0fj1hvrj_true)
        self.addObject(self.h_score_3j0fj0hvrj_true)
        self.addObject(self.h_score_2j0fj1hvrj_true)
        self.addObject(self.h_score_2j1fj0hvrj_true)
        self.addObject(self.h_score_3j1fj0hvrj_false)
        self.addObject(self.h_score_3j0fj1hvrj_false)
        self.addObject(self.h_score_3j0fj0hvrj_false)
        self.addObject(self.h_score_2j0fj1hvrj_false)
        self.addObject(self.h_score_2j1fj0hvrj_false)

        

    def analyze(self, event):
        """process event, return True (go to next module) or False (fail, go to next event)"""
        tops_mixed = Collection(event, "TopMixed")

        for top in tops_mixed:
            #print("nquark",top.nquark)
            #print("truth",top.truth)
            self.h_ntops_tot.Fill(1)
            best_tops=[]

            if (top.truth==1):
                self.h_score_top_mixed_true.Fill(top.TopScore_standard)
                self.h_pt_top_mixed_true.Fill(top.pt)
                self.h_mass_top_mixed_true.Fill(top.mass)
                if top.category==0:
                    self.h_score_3j1fj0hvrj_true.Fill(top.TopScore_standard)
                elif top.category==1:
                    self.h_score_3j0fj1hvrj_true.Fill(top.TopScore_standard)
                elif top.category==2:
                    self.h_score_3j0fj0hvrj_true.Fill(top.TopScore_standard)
                elif top.category==3:
                    self.h_score_2j1fj0hvrj_true.Fill(top.TopScore_standard)
                elif top.category==4:
                    self.h_score_2j0fj1hvrj_true.Fill(top.TopScore_standard)

            if top.truth!=1:
                self.h_score_top_mixed_false_all.Fill(top.TopScore_standard)
                self.h_pt_top_mixed_false_all.Fill(top.pt)
                self.h_mass_top_mixed_false_all.Fill(top.mass)
                if top.category==0:
                    self.h_score_3j1fj0hvrj_false.Fill(top.TopScore_standard)
                elif top.category==1:
                    self.h_score_3j0fj1hvrj_false.Fill(top.TopScore_standard)
                elif top.category==2:
                    self.h_score_3j0fj0hvrj_false.Fill(top.TopScore_standard)
                elif top.category==3:
                    self.h_score_2j1fj0hvrj_false.Fill(top.TopScore_standard)
                elif top.category==4:
                    self.h_score_2j0fj1hvrj_false.Fill(top.TopScore_standard)
            if top.truth==0:
                self.h_score_top_mixed_false_qcd.Fill(top.TopScore_standard)
                self.h_pt_top_mixed_false_qcd.Fill(top.pt)
                self.h_mass_top_mixed_false_qcd.Fill(top.mass)

            if top.truth==-1:
                self.h_score_top_mixed_false_other.Fill(top.TopScore_standard)
                self.h_pt_top_mixed_false_other.Fill(top.pt)
                self.h_mass_top_mixed_false_other.Fill(top.mass)
            

        return True

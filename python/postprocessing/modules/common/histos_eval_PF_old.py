import ROOT
import os
ROOT.PyConfig.IgnoreCommandLineOptions = True

from PhysicsTools.NanoAODTools.postprocessing.framework.datamodel import Collection, Object 
from PhysicsTools.NanoAODTools.postprocessing.framework.eventloop import Module


path_to_model_folder    = "/eos/user/f/fsalerno/framework/MachineLearning/models/"
path_to_graphics_folder    = "/eos/user/f/fsalerno/framework/MachineLearning/"
mods                    = ["CNN","CNN_2D","CNN_conc","CNN_2D_conc","transformer","LSTM","LSTM_DNN","CNN_2D_LSTM","CNN_2D_LSTM_conc","CNN_2D_LSTM","TROTA"]
cuts                    = ["","_0_pt","_200_pt","_300_pt"]
n_PFCs                  = 20
models                  = {}

keys=[]
for mod in mods:
    for cut in cuts:
        key=f"{n_PFCs}_{mod}{cut}"
        if os.path.isfile(f"{path_to_model_folder}/model_{key}.h5"):
            keys.append(key)







class histos_eval(Module):
    def __init__(self):
        self.writeHistFile=True
        pass

    def beginJob(self,histFile,histDirName):
        
        #self.objs = []
        #print("\n e ora?", dir(self))
        Module.beginJob(self,histFile,histDirName+"_evaluation")
        self.h_score_top_mixed_true = {}
        self.h_score_top_mixed_false_qcd = {}
        self.h_score_top_mixed_false_other = {}
        self.h_score_top_mixed_false_all = {}
        self.h_score_top_mixed_true_cut_200_pt = {}
        self.h_score_top_mixed_false_qcd_cut_200_pt = {}
        self.h_score_top_mixed_false_other_cut_200_pt = {}
        self.h_score_top_mixed_false_all_cut_200_pt = {}
        self.h_score_top_mixed_true_cut_300_pt = {}
        self.h_score_top_mixed_false_qcd_cut_300_pt = {}
        self.h_score_top_mixed_false_other_cut_300_pt = {}
        self.h_score_top_mixed_false_all_cut_300_pt = {}
        self.h_pt_top_mixed_true = {}
        self.h_pt_top_mixed_false_qcd = {}
        self.h_pt_top_mixed_false_other = {}
        self.h_pt_top_mixed_false_all = {}
        self.h_mass_top_mixed_true = {}
        self.h_mass_top_mixed_false_qcd = {}
        self.h_mass_top_mixed_false_other = {}
        self.h_mass_top_mixed_false_all = {}
        self.h_ntops_tot = {}
        self.h_score_3j1fj_true = {}
        self.h_score_3j0fj_true = {}
        self.h_score_2j1fj_true = {}
        self.h_score_3j1fj_false = {}
        self.h_score_3j0fj_false = {}
        self.h_score_2j1fj_false = {}
        for key in keys:
            self.h_score_top_mixed_true[key] = ROOT.TH1F(f"score_top_mixed_true_{key}", f"score_top_mixed_true_{key}", 100, 0, 1)
            self.h_score_top_mixed_false_qcd[key] = ROOT.TH1F(f"score_top_mixed_false_qcd_{key}", f"score_top_mixed_false_qcd_{key}", 100, 0, 1)
            self.h_score_top_mixed_false_other[key] = ROOT.TH1F(f"score_top_mixed_false_other_{key}", f"score_top_mixed_false_other_{key}", 100, 0, 1)
            self.h_score_top_mixed_false_all[key] = ROOT.TH1F(f"score_top_mixed_false_all_{key}", f"score_top_mixed_false_all_{key}", 100, 0, 1)
            self.h_score_top_mixed_true_cut_200_pt[key] = ROOT.TH1F(f"score_top_mixed_true_cut_200_pt_{key}", f"score_top_mixed_true_cut_200_pt_{key}", 100, 0, 1)
            self.h_score_top_mixed_false_qcd_cut_200_pt[key] = ROOT.TH1F(f"score_top_mixed_false_qcd_cut_200_pt_{key}", f"score_top_mixed_false_qcd_cut_200_pt_{key}", 100, 0, 1)
            self.h_score_top_mixed_false_other_cut_200_pt[key] = ROOT.TH1F(f"score_top_mixed_false_other_cut_200_pt_{key}", f"score_top_mixed_false_other_cut_200_pt_{key}", 100, 0, 1)
            self.h_score_top_mixed_false_all_cut_200_pt[key] = ROOT.TH1F(f"score_top_mixed_false_all_cut_200_pt_{key}", f"score_top_mixed_false_all_cut_200_pt_{key}", 100, 0, 1)
            self.h_score_top_mixed_true_cut_300_pt[key] = ROOT.TH1F(f"score_top_mixed_true_cut_300_pt_{key}", f"score_top_mixed_true_cut_300_pt_{key}", 100, 0, 1)
            self.h_score_top_mixed_false_qcd_cut_300_pt[key] = ROOT.TH1F(f"score_top_mixed_false_qcd_cut_300_pt_{key}", f"score_top_mixed_false_qcd_cut_300_pt_{key}", 100, 0, 1)
            self.h_score_top_mixed_false_other_cut_300_pt[key] = ROOT.TH1F(f"score_top_mixed_false_other_cut_300_pt_{key}", f"score_top_mixed_false_other_cut_300_pt_{key}", 100, 0, 1)
            self.h_score_top_mixed_false_all_cut_300_pt[key] = ROOT.TH1F(f"score_top_mixed_false_all_cut_300_pt_{key}", f"score_top_mixed_false_all_cut_300_pt_{key}", 100, 0, 1)
            self.h_pt_top_mixed_true[key] = ROOT.TH1F(f"pt_top_mixed_true_{key}", f"pt_top_mixed_true_{key}", 100, 0, 1000)
            self.h_pt_top_mixed_false_qcd[key] = ROOT.TH1F(f"pt_top_mixed_false_qcd_{key}", f"pt_top_mixed_false_qcd_{key}", 100, 0, 1000)
            self.h_pt_top_mixed_false_other[key] = ROOT.TH1F(f"pt_top_mixed_false_other_{key}", f"pt_top_mixed_false_other_{key}", 100, 0, 1000)
            self.h_pt_top_mixed_false_all[key] = ROOT.TH1F(f"pt_top_mixed_false_all_{key}", f"pt_top_mixed_false_all_{key}", 100, 0, 1000)
            self.h_mass_top_mixed_true[key] = ROOT.TH1F(f"mass_top_mixed_true_{key}", f"mass_top_mixed_true_{key}", 100, 0, 1000)
            self.h_mass_top_mixed_false_qcd[key] = ROOT.TH1F(f"mass_top_mixed_false_qcd_{key}", f"mass_top_mixed_false_qcd_{key}", 100, 0, 1000)
            self.h_mass_top_mixed_false_other[key] = ROOT.TH1F(f"mass_top_mixed_false_other_{key}", f"mass_top_mixed_false_other_{key}", 100, 0, 1000)
            self.h_mass_top_mixed_false_all[key] = ROOT.TH1F(f"mass_top_mixed_false_all_{key}", f"mass_top_mixed_false_all_{key}", 100, 0, 1000)
            self.h_ntops_tot[key] = ROOT.TH1F(f"ntops_tot_{key}", f"ntops_tot_{key}", 6, 0, 6)
            self.h_score_3j1fj_true[key] = ROOT.TH1F(f"score_3j1fj_true_{key}", f"score_3j1fj_true_{key}", 100, 0, 1)
            self.h_score_3j0fj_true[key] = ROOT.TH1F(f"score_3j0fj_true_{key}", f"score_3j0fj_true_{key}", 100, 0, 1)
            self.h_score_2j1fj_true[key] = ROOT.TH1F(f"score_2j1fj_true_{key}", f"score_2j1fj_true_{key}", 100, 0, 1)
            self.h_score_3j1fj_false[key] = ROOT.TH1F(f"score_3j1fj_false_{key}", f"score_3j1fj_false_{key}", 100, 0, 1)
            self.h_score_3j0fj_false[key] = ROOT.TH1F(f"score_3j0fj_false_{key}", f"score_3j0fj_false_{key}", 100, 0, 1)
            self.h_score_2j1fj_false[key] = ROOT.TH1F(f"score_2j1fj_false_{key}", f"score_2j1fj_false_{key}", 100, 0, 1)

            # Add histograms to the framework
            self.addObject(self.h_score_top_mixed_true[key])
            self.addObject(self.h_score_top_mixed_false_qcd[key])
            self.addObject(self.h_score_top_mixed_false_other[key])
            self.addObject(self.h_score_top_mixed_false_all[key])
            self.addObject(self.h_score_top_mixed_true_cut_200_pt[key])
            self.addObject(self.h_score_top_mixed_false_qcd_cut_200_pt[key])
            self.addObject(self.h_score_top_mixed_false_other_cut_200_pt[key])
            self.addObject(self.h_score_top_mixed_false_all_cut_200_pt[key])
            self.addObject(self.h_score_top_mixed_true_cut_300_pt[key])
            self.addObject(self.h_score_top_mixed_false_qcd_cut_300_pt[key])
            self.addObject(self.h_score_top_mixed_false_other_cut_300_pt[key])
            self.addObject(self.h_score_top_mixed_false_all_cut_300_pt[key])
            self.addObject(self.h_pt_top_mixed_true[key])
            self.addObject(self.h_pt_top_mixed_false_qcd[key])
            self.addObject(self.h_pt_top_mixed_false_other[key])
            self.addObject(self.h_pt_top_mixed_false_all[key])
            self.addObject(self.h_mass_top_mixed_true[key])
            self.addObject(self.h_mass_top_mixed_false_qcd[key])
            self.addObject(self.h_mass_top_mixed_false_other[key])
            self.addObject(self.h_mass_top_mixed_false_all[key])
            self.addObject(self.h_ntops_tot[key])
            self.addObject(self.h_score_3j1fj_true[key])
            self.addObject(self.h_score_3j0fj_true[key])
            self.addObject(self.h_score_2j1fj_true[key])
            self.addObject(self.h_score_3j1fj_false[key])
            self.addObject(self.h_score_3j0fj_false[key])
            self.addObject(self.h_score_2j1fj_false[key])

        

    def analyze(self, event):
        """Process event, return True (go to next module) or False (fail, go to next event)."""
        tops_mixed = Collection(event, "TopMixed")

        for key in keys:
            for top in tops_mixed:
                
                top_score_key = f"TopScore_{key}"  
                if hasattr(top, top_score_key):
                    TopScore = getattr(top, top_score_key) 

                if key in self.h_ntops_tot:
                    self.h_ntops_tot[key].Fill(1)

                if top.truth == 1:
                    if key in self.h_score_top_mixed_true:
                        self.h_score_top_mixed_true[key].Fill(TopScore)
                        self.h_pt_top_mixed_true[key].Fill(top.pt)
                        self.h_mass_top_mixed_true[key].Fill(top.mass)
                        if top.pt>=200:
                            self.h_score_top_mixed_true_cut_200_pt[key].Fill(TopScore)
                        if top.pt>=300:
                            self.h_score_top_mixed_true_cut_300_pt[key].Fill(TopScore)

                    if top.category == 0 and key in self.h_score_3j1fj_true:
                        self.h_score_3j1fj_true[key].Fill(TopScore)
                    elif top.category == 1 and key in self.h_score_3j0fj_true:
                        self.h_score_3j0fj_true[key].Fill(TopScore)
                    elif top.category == 2 and key in self.h_score_2j1fj_true:
                        self.h_score_2j1fj_true[key].Fill(TopScore)

                if top.truth != 1:
                    if key in self.h_score_top_mixed_false_all:
                        self.h_score_top_mixed_false_all[key].Fill(TopScore)
                        self.h_pt_top_mixed_false_all[key].Fill(top.pt)
                        self.h_mass_top_mixed_false_all[key].Fill(top.mass)
                    if top.category == 0 and key in self.h_score_3j1fj_false:
                        self.h_score_3j1fj_false[key].Fill(TopScore)
                    elif top.category == 1 and key in self.h_score_3j0fj_false:
                        self.h_score_3j0fj_false[key].Fill(TopScore)
                    elif top.category == 2 and key in self.h_score_2j1fj_false:
                        self.h_score_2j1fj_false[key].Fill(TopScore)
                    if top.pt>=200:
                        self.h_score_top_mixed_false_all_cut_200_pt[key].Fill(TopScore)
                    if top.pt>=300:
                        self.h_score_top_mixed_false_all_cut_300_pt[key].Fill(TopScore)

                if top.truth == 0:
                    if key in self.h_score_top_mixed_false_qcd:
                        self.h_score_top_mixed_false_qcd[key].Fill(TopScore)
                        self.h_pt_top_mixed_false_qcd[key].Fill(top.pt)
                        self.h_mass_top_mixed_false_qcd[key].Fill(top.mass)
                    if top.pt>=200:
                        self.h_score_top_mixed_false_qcd_cut_200_pt[key].Fill(TopScore)
                    if top.pt>=300:
                        self.h_score_top_mixed_false_qcd_cut_300_pt[key].Fill(TopScore)

                if top.truth == -1:
                    if key in self.h_score_top_mixed_false_other:
                        self.h_score_top_mixed_false_other[key].Fill(TopScore)
                        self.h_pt_top_mixed_false_other[key].Fill(top.pt)
                        self.h_mass_top_mixed_false_other[key].Fill(top.mass)
                    if top.pt>=200:
                        self.h_score_top_mixed_false_other_cut_200_pt[key].Fill(TopScore)
                    if top.pt>=300:
                        self.h_score_top_mixed_false_other_cut_300_pt[key].Fill(TopScore)

        return True


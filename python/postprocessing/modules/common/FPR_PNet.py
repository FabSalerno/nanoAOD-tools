#!/usr/bin/env python
from PhysicsTools.NanoAODTools.postprocessing.framework.eventloop import Module
from PhysicsTools.NanoAODTools.postprocessing.framework.datamodel import Collection
from PhysicsTools.NanoAODTools.postprocessing.framework.postprocessor import PostProcessor
from importlib import import_module
import os
import sys
import ROOT
ROOT.PyConfig.IgnoreCommandLineOptions = True


class thr_PNet(Module):
    def __init__(self):
        self.writeHistFile = True

    def beginJob(self, histFile=None, histDirName=None):
        Module.beginJob(self, histFile, histDirName)

        self.score = ROOT.TH1F('score', 'score', 100, 0, 1)
        self.score_res = ROOT.TH1F('score_res', 'score_res', 1000, 0, 1)
        self.ntop = ROOT.TH1F('ntop', 'ntop', 3, 0, 3)
        self.addObject(self.score)
        self.addObject(self.score_res)
        self.addObject(self.ntop)

    def analyze(self, event):
        tops_merged = Collection(event,"FatJet")
        ntopmerged = len(tops_merged)
        #nessuna presel su top_merged
        for top in tops_merged:
            self.score.Fill(top.particleNetWithMass_TvsQCD)
            self.score_res.Fill(top.particleNetWithMass_TvsQCD)
            #self.score.Fill(top.particleNet_TvsQCD)
            #self.score_res.Fill(top.particleNet_TvsQCD)
            self.ntop.Fill(1)

        return True

HT="800_1000"
files=[f"/eos/user/f/fsalerno/Data/PF/nano_mcRun3_QCD_HT_{HT}_MC2022.root"]

#files = [" root://cms-xrd-global.cern.ch//store/mc/Run3Summer22NanoAODv11/QCD-4Jets_HT-200to400_TuneCP5_13p6TeV_madgraphMLM-pythia8/NANOAODSIM/126X_mcRun3_2022_realistic_v2-v2/2810000/0121789a-f0e9-46fb-9cb5-e489a0a4db8b.root"]
p = PostProcessor(".", files, cut=None, branchsel=None, modules=[
                  thr_PNet()], noOut=True, histFileName=f"fpr_PNet_{HT}.root", histDirName=f"plots_{HT}")
p.run()

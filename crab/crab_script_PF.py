#!/usr/bin/env python3
import os

from PhysicsTools.NanoAODTools.postprocessing.framework.postprocessor import *

# this takes care of converting the input files from CRAB
from PhysicsTools.NanoAODTools.postprocessing.framework.crabhelper import inputFiles, runsAndLumis
from PhysicsTools.NanoAODTools.postprocessing.modules.common.Mtt_cut_gen_lvl import *

from PhysicsTools.NanoAODTools.postprocessing.modules.common.deltaR_PF import *
from PhysicsTools.NanoAODTools.postprocessing.modules.common.MCweight_writer import *
from PhysicsTools.NanoAODTools.postprocessing.modules.common.MET_Filter import *
from PhysicsTools.NanoAODTools.postprocessing.modules.common.preselection_PF import *
#from PhysicsTools.NanoAODTools.postprocessing.modules.common.puWeightProducer import *
from PhysicsTools.NanoAODTools.postprocessing.modules.common.GenPart_MomFirstCp_PF import *
from PhysicsTools.NanoAODTools.postprocessing.modules.common.nanoprepro_v2_PF import *
from PhysicsTools.NanoAODTools.postprocessing.modules.common.nanoTopcandidate_v2_PF import *
from PhysicsTools.NanoAODTools.postprocessing.modules.common.nanoTopEvaluate_MultiScore_v2_PF import *
#from PhysicsTools.NanoAODTools.postprocessing.modules.common.GenPart_MomFirstCp import *
#from PhysicsTools.NanoAODTools.postprocessing.modules.common.nanoprepro_v2 import *
#from PhysicsTools.NanoAODTools.postprocessing.modules.common.nanoTopcandidate_v2 import *
#from PhysicsTools.NanoAODTools.postprocessing.modules.common.nanoTopEvaluate_MultiScore_v2 import *
from PhysicsTools.NanoAODTools.postprocessing.modules.common.score_selection import *
from PhysicsTools.NanoAODTools.postprocessing.modules.common.test_PF import *
from PhysicsTools.NanoAODTools.postprocessing.modules.common.Idx_PF import *
from PhysicsTools.NanoAODTools.postprocessing.modules.common.collectionMerger import *
from PhysicsTools.NanoAODTools.postprocessing.modules.common.countHistogramsModule import *
from PhysicsTools.NanoAODTools.postprocessing.modules.common.histos_eval_PF import *
from PhysicsTools.NanoAODTools.postprocessing.modules.common.preselection_PF import *
from PhysicsTools.NanoAODTools.postprocessing.modules.common.event_counter_pre_presel_PF import *
from PhysicsTools.NanoAODTools.postprocessing.modules.common.event_counter_post_presel_PF import *
from PhysicsTools.NanoAODTools.postprocessing.modules.common.event_counter_5_per_100_PF import *
from PhysicsTools.NanoAODTools.postprocessing.modules.common.event_counter_1_per_100_PF import *
from PhysicsTools.NanoAODTools.postprocessing.modules.common.event_counter_1_per_1000_PF import *
from PhysicsTools.NanoAODTools.postprocessing.modules.common.GenPart_hadronicTop import*
from PhysicsTools.NanoAODTools.postprocessing.modules.common.pt_cut_top_gen_lvl import*

'''
from PhysicsTools.NanoAODTools.postprocessing.modules.jme.jetmetHelperRun2 import *
from PhysicsTools.NanoAODTools.postprocessing.framework.crabhelper import inputFiles,runsAndLumis
from PhysicsTools.NanoAODTools.postprocessing.modules.common.puWeightProducer import *
'''


from argparse import ArgumentParser
parser                      = ArgumentParser()
parser.add_argument("-dirpath",                                 dest="dirpath",                                  default="/eos/user/f/fsalerno/Data/HOTVR/ttX_ntuplizer/tt_mtt-700to1000_MC2018_ntuplizer/",               required=True,         type=str,       help="path to file")
parser.add_argument("-component",                               dest="component",                                default="tt_mtt-700to1000_MC2018",                                                                        required=False,        type=str,       help="component considered")

options                     = parser.parse_args()

### ARGS ###
dirpath                        = options.dirpath
component                      = options.component


filepath=["/eos/user/f/fsalerno/Data/PF/nano_mcRun3_TT_semilep_MC2022.root"]
out_path = "/eos/user/f/fsalerno/Data/PF/topevaluate/"
histo_name = "histos_evaluation_PF_2022_1_jets_20_"+component+".root"
histo_dir = "histograms"

#p=PostProcessor(out_path, inputFiles=filepath, modules=[event_counter_pre(),preselection(),event_counter_post(),#histos_eval(),event_counter_5_100(),event_counter_1_100(),event_counter_1_1000(),close_histos()], friend=False, postfix="_topeval_PF_"+component, provenance=True, fwkJobReport=True,histFileName=histo_name, histDirName=histo_dir) # histFileName=histo_name, histDirName=histo_dir maxEntries=10000
#p=PostProcessor(out_path, inputFiles=filepath, modules=[event_counter_pre(),preselection(),event_counter_post(),histos_eval(),event_counter_5_100(),event_counter_1_100(),event_counter_1_1000(),close_histos()], friend=False, postfix="_topeval_PF_presel_"+component, provenance=True, fwkJobReport=True,histFileName=histo_name, histDirName=histo_dir) # histFileName=histo_name, histDirName=histo_dir maxEntries=10000
#p=PostProcessor(out_path, inputFiles=filepath, modules=[GenPart_MomFirstCp(flavour='-5,-4,-3,-2,-1,1,2,3,4,5,6,-6,24,-24'), Idx_PF(), deltaR_PF(),collectionMerger(input=["PFCands"], output="PFCands", sortkey=lambda x: x.pt, reverse=True, selector=None, maxObjects=None), nanoprepro(isMC=1),nanoTopcand(isMC=1)], friend=False, postfix=f"_topcand_prova_mio_{component}", provenance=True, fwkJobReport=True, maxEntries=10000) # histFileName=histo_name, histDirName=histo_dir maxEntries=10000
#p=PostProcessor(out_path, inputFiles=filepath, modules=[event_counter_pre(),preselection(),event_counter_post(),GenPart_MomFirstCp(flavour='-5,-4,-3,-2,-1,1,2,3,4,5,6,-6,24,-24'), Idx_PF(), deltaR_PF(),collectionMerger(input=["PFCands"], output="PFCands", sortkey=lambda x: x.pt, reverse=True, selector=None, maxObjects=None), nanoprepro(isMC=1),nanoTopcand(isMC=1),nanoTopevaluate_MultiScore(),histos_eval(),event_counter_5_100(),event_counter_1_100(),event_counter_1_1000()], friend=False, postfix=f"_topeval_prova_mio", provenance=True, fwkJobReport=True, maxEntries=10000) # histFileName=histo_name, histDirName=histo_dir maxEntries=10000
#### PER TOPEVAL###
p=PostProcessor(out_path, inputFiles=filepath, modules=[event_counter_pre(),Mtt_cut_gen_lvl(minMtt=1000,maxMtt=100000),event_counter_post(),GenPart_MomFirstCp(flavour='-5,-4,-3,-2,-1,1,2,3,4,5,6,-6,24,-24'),GenPart_hadronicTop(), Idx_PF(), deltaR_PF(),collectionMerger(input=["PFCands"], output="PFCands", sortkey=lambda x: x.pt, reverse=True, selector=None, maxObjects=None), nanoprepro(isMC=1),nanoTopcand(isMC=1),nanoTopevaluate_MultiScore(),event_counter_5_100(),event_counter_1_100(),event_counter_1_1000()], friend=False, postfix=f"_topeval_PF_presel", provenance=True, fwkJobReport=True, maxEntries=1000) # histFileName=histo_name, histDirName=histo_dir maxEntries=10000
####PER MTT#####
#p=PostProcessor(out_path, inputFiles=filepath, modules=[event_counter_pre(), Mtt_cut_gen_lvl(), event_counter_post(),GenPart_MomFirstCp(flavour='-5,-4,-3,-2,-1,1,2,3,4,5,6,-6,24,-24'),GenPart_hadronicTop(), Idx_PF(), deltaR_PF(),collectionMerger(input=["PFCands"], output="PFCands", sortkey=lambda x: x.pt, reverse=True, selector=None, maxObjects=None), nanoprepro(isMC=1),nanoTopcand(isMC=1)], friend=False, postfix=f"_topcand_PF_Mtt_700_1000", provenance=True, fwkJobReport=True,maxEntries=10000) # histFileName=histo_name, histDirName=histo_dir maxEntries=10000
p.run()
print('DONE')
#/eos/user/f/fsalerno/Data/TT_Mtt-1000toInf.root
#!/usr/bin/env python3
import os

from PhysicsTools.NanoAODTools.postprocessing.framework.postprocessor import *

# this takes care of converting the input files from CRAB
from PhysicsTools.NanoAODTools.postprocessing.framework.crabhelper import inputFiles, runsAndLumis


from PhysicsTools.NanoAODTools.postprocessing.modules.common.deltaR_PF import *
from PhysicsTools.NanoAODTools.postprocessing.modules.common.MCweight_writer import *
from PhysicsTools.NanoAODTools.postprocessing.modules.common.MET_Filter import *
from PhysicsTools.NanoAODTools.postprocessing.modules.common.preselectionPF import *
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
from PhysicsTools.NanoAODTools.postprocessing.modules.common.histos_eval_PF import *
from PhysicsTools.NanoAODTools.postprocessing.modules.common.preselection_PF import *
from PhysicsTools.NanoAODTools.postprocessing.modules.common.event_counter_pre_presel_PF import *
from PhysicsTools.NanoAODTools.postprocessing.modules.common.event_counter_post_presel_PF import *
from PhysicsTools.NanoAODTools.postprocessing.modules.common.event_counter_5_per_100_PF import *
from PhysicsTools.NanoAODTools.postprocessing.modules.common.event_counter_1_per_100_PF import *
from PhysicsTools.NanoAODTools.postprocessing.modules.common.event_counter_1_per_1000_PF import *
from PhysicsTools.NanoAODTools.postprocessing.modules.common.close_histos import *

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


filepath=[]
for f, file_name in enumerate(os.listdir(dirpath)):
    #print("file_name is ",file_name)
    if not file_name.startswith('.') and file_name.endswith(".root") and component in file_name and f in range(0,20):
        filepath.append(dirpath+file_name)
print("filepath is ===== ",filepath)




 
out_path = "/eos/user/f/fsalerno/Data/PF/topcand/prova/"
histo_name = "histos_evaluation_PF_2022_1_jets_20_"+component+"_presel.root"
histo_dir = "histograms"

#p=PostProcessor(out_path, inputFiles=filepath, modules=[event_counter_pre(),preselection(),event_counter_post(),#histos_eval(),event_counter_5_100(),event_counter_1_100(),event_counter_1_1000(),close_histos()], friend=False, postfix="_topeval_PF_"+component, provenance=True, fwkJobReport=True,histFileName=histo_name, histDirName=histo_dir) # histFileName=histo_name, histDirName=histo_dir maxEntries=10000
#p=PostProcessor(out_path, inputFiles=filepath, modules=[event_counter_pre(),preselection(),event_counter_post(),histos_eval(),event_counter_5_100(),event_counter_1_100(),event_counter_1_1000(),close_histos()], friend=False, postfix="_topeval_PF_presel_"+component, provenance=True, fwkJobReport=True,histFileName=histo_name, histDirName=histo_dir) # histFileName=histo_name, histDirName=histo_dir maxEntries=10000
p=PostProcessor(out_path, inputFiles=filepath, modules=[GenPart_MomFirstCp(flavour='-5,-4,-3,-2,-1,1,2,3,4,5,6,-6,24,-24'), Idx_PF(), deltaR_PF(),collectionMerger(input=["PFCands"], output="PFCands", sortkey=lambda x: x.pt, reverse=True, selector=None, maxObjects=None), nanoprepro(isMC=1),nanoTopcand(isMC=1)], friend=False, postfix=f"_topcand_prova_mio_{component}", provenance=True, fwkJobReport=True, maxEntries=10000) # histFileName=histo_name, histDirName=histo_dir maxEntries=10000
#p=PostProcessor(out_path, inputFiles=filepath, modules=[GenPart_MomFirstCp(flavour='-5,-4,-3,-2,-1,1,2,3,4,5,6,-6,24,-24'),nanoprepro(isMC=1),nanoTopcand(isMC=1)], friend=False, postfix="_topcand_TROTA_"+component, provenance=True, fwkJobReport=True, histFileName=histo_name, histDirName=histo_dir, maxEntries=100000) # histFileName=histo_name, histDirName=histo_dir maxEntries=10000
p.run()
print('DONE')
#/eos/user/f/fsalerno/Data/TT_Mtt-1000toInf.root
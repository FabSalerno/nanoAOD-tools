#!/usr/bin/env python3
import os
from PhysicsTools.NanoAODTools.postprocessing.framework.postprocessor import *

# this takes care of converting the input files from CRAB
from PhysicsTools.NanoAODTools.postprocessing.framework.crabhelper import inputFiles, runsAndLumis
#modules
from PhysicsTools.NanoAODTools.postprocessing.modules.common.firstSelection import *
from PhysicsTools.NanoAODTools.postprocessing.modules.common.histos_eval import *
from PhysicsTools.NanoAODTools.postprocessing.modules.common.event_counter_pre_presel import *
from PhysicsTools.NanoAODTools.postprocessing.modules.common.event_counter_post_presel import *
from PhysicsTools.NanoAODTools.postprocessing.modules.common.event_counter_5_per_100 import *
from PhysicsTools.NanoAODTools.postprocessing.modules.common.event_counter_1_per_100 import *
from PhysicsTools.NanoAODTools.postprocessing.modules.common.event_counter_1_per_1000 import *
from PhysicsTools.NanoAODTools.postprocessing.modules.common.close_histos import *


#from PhysicsTools.NanoAODTools.postprocessing.modules.common.nanoprepro_v2 import *
from PhysicsTools.NanoAODTools.postprocessing.modules.common.MCweight_writer import *
from PhysicsTools.NanoAODTools.postprocessing.modules.common.MET_Filter import *
from PhysicsTools.NanoAODTools.postprocessing.modules.common.preselection_hotvr import *
from PhysicsTools.NanoAODTools.postprocessing.modules.common.GenPart_MomFirstCp_hotvr import *
#from PhysicsTools.NanoAODTools.postprocessing.modules.common.GenPart_MomFirstCp import *
from PhysicsTools.NanoAODTools.postprocessing.modules.common.nanoprepro_v2_hotvr import *
#from PhysicsTools.NanoAODTools.postprocessing.modules.common.nanoprepro_v2 import *
#from PhysicsTools.NanoAODTools.postprocessing.modules.common.nanoTopcandidate_v2_hotvr_debug import *
from PhysicsTools.NanoAODTools.postprocessing.modules.common.nanoTopcandidate_v2_hotvr import *
from PhysicsTools.NanoAODTools.postprocessing.modules.common.nanoTopcandidate_v2_hotvr_new_def import *
#from PhysicsTools.NanoAODTools.postprocessing.modules.common.nanoTopcandidate_v2 import *
#from PhysicsTools.NanoAODTools.postprocessing.modules.common.nanoTopcandidate_v2_prova import *
#from PhysicsTools.NanoAODTools.postprocessing.modules.common.nanoTopEvaluate_MultiScore_v2_fab import *
from PhysicsTools.NanoAODTools.postprocessing.modules.common.globalvar import *
#from PhysicsTools.NanoAODTools.postprocessing.modules.common.SampleIdx import *
#from PhysicsTools.NanoAODTools.postprocessing.modules.common.nanoTopevaluate import *
#from PhysicsTools.NanoAODTools.postprocessing.modules.common.topselection import *
from PhysicsTools.NanoAODTools.postprocessing.modules.common.score_selection import *
#'''
from PhysicsTools.NanoAODTools.postprocessing.modules.jme.jetmetHelperRun2 import *
from PhysicsTools.NanoAODTools.postprocessing.framework.crabhelper import inputFiles,runsAndLumis
from PhysicsTools.NanoAODTools.postprocessing.modules.common.puWeightProducer import *
#'''

from argparse import ArgumentParser
parser                      = ArgumentParser()
parser.add_argument("-dirpath",                                 dest="dirpath",                                  default="/eos/user/f/fsalerno/Data/HOTVR/ttX_ntuplizer/tt_mtt-700to1000_MC2018_ntuplizer/",               required=True,         type=str,       help="path to file")
parser.add_argument("-component",                               dest="component",                                default="tt_mtt-700to1000_MC2018",                                                                        required=False,        type=str,       help="component considered")

options                     = parser.parse_args()

### ARGS ###
dirpath                        = options.dirpath
component                      = options.component

'''
filepath=[]
for f, file_name in enumerate(os.listdir(dirpath)):
    if not file_name.startswith('.') and f in range(0,10):
        filepath.append(dirpath+file_name)
print("filepath is ===== ",filepath)


import random
seed_value= 0
filepath=[]
random.seed(seed_value)
n = random.sample(range(0, len(os.listdir(dirpath))),len(os.listdir(dirpath)))
for f, file_name in enumerate(os.listdir(dirpath)):
    if not file_name.startswith('.') and f in n:
        filepath.append(dirpath+file_name)
    if len(filepath)==10:
        break
print("filepath is ===== ",filepath)

'''


import random
seed_value= 0
filepath=[]
random.seed(seed_value)
#semilep 2, tt-mtt 1, qcd_1000 70, qcd_1500 50, qcd_2000 15, qcd_inf 20
k=0
n = random.sample(range(0, len(os.listdir(dirpath))),len(os.listdir(dirpath)))
if component == "tt_mtt-700to1000_MC2018" or component=="tt_mtt-1000toInf_MC2018":
    num=5
elif component == "qcd_ht_1000_MC2018":
    num=-1
elif component == "qcd_ht_1500_MC2018":
    num=-1
elif component == "qcd_ht_2000_MC2018":
    num=-1
elif component == "qcd_ht_inf_MC2018":
    num=-1
elif component == "tt_semilepton_MC2018":
    num=10
for f, file_name in enumerate(os.listdir(dirpath)):
    if num!=-1:
        if not file_name.startswith('.') and f in n and k<=num:
            filepath.append(dirpath+file_name)
            k+=1
        if k==num:
            break
    if num==-1:
        if not file_name.startswith('.') and f in n:
            filepath.append(dirpath+file_name)
print("filepath is ===== ",filepath)




from PhysicsTools.NanoAODTools.postprocessing.modules.common.nanoTopEvaluate_MultiScore_v2_HOTVR import *


out_path = "/eos/user/f/fsalerno/Data/HOTVR/evaluate_j_in_HVRj_1_"+component+"_topeval/"
#out_path = "/eos/user/f/fsalerno/Data/HOTVR/training_new_def/"+component+"_topcand/"
#out_path = "/eos/user/f/fsalerno/Data/HOTVR/training_FINAL/QCD_inf"
#out_path = "/eos/user/f/fsalerno/Data/PF/prova/"

histo_name = "histos_evaluation_HOTVR_2018_j_in_HVRj_1_"+component+"_presel.root"
#histo_name = ["prova1", "prova_2","prova3","prova4","prova5"]
histo_dir = "histograms"
# preselection(),
p=PostProcessor(out_path, inputFiles=filepath, modules=[event_counter_pre(), preselection(), event_counter_post(), GenPart_MomFirstCp(flavour='-5,-4,-3,-2,-1,1,2,3,4,5,6,-6,24,-24'),  nanoprepro(), nanoTopcand(isMC=1, multiscore=1), nanoTopevaluate_MultiScore(isMC=1), histos_eval(),event_counter_5_100(),event_counter_1_100(),event_counter_1_1000(),close_histos()], friend=False, postfix="_topeval_HOTVR_2_"+component, provenance=True, fwkJobReport=True, histFileName=histo_name, histDirName=histo_dir) # , maxEntries=10000 , 
#p=PostProcessor(out_path, inputFiles=filepath, modules=[GenPart_MomFirstCp(flavour='-5,-4,-3,-2,-1,1,2,3,4,5,6,-6,24,-24'), nanoprepro(), nanoTopcand_hotvr_new_def(isMC=1, multiscore=0)], friend=False, postfix="topcand_HOTVR_10000_new_def_"+component, provenance=True, fwkJobReport=True, maxEntries=10000) # histFileName=histo_name, histDirName=histo_dir maxEntries=10000
#p=PostProcessor(out_path, inputFiles=filepath, modules=[SampleIdx(20003), GenPart_MomFirstCp(flavour='-5,-4,-3,-2,-1,1,2,3,4,5,6,-6,24,-24')], friend=False, postfix="_genpart_PF_prova_"+component, provenance=True, fwkJobReport=True, maxEntries=10000) # histFileName=histo_name, histDirName=histo_dir maxEntries=10000
#MET_Filter(year = 2018), nanoTopcand(isMC=1), nanoTopevaluate_MultiScore(), firstSelectionConstr(), 
p.run()
print('DONE')
#/eos/user/f/fsalerno/Data/TT_Mtt-1000toInf.root
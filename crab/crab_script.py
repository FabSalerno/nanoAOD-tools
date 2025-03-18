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

#prima commentati
from PhysicsTools.NanoAODTools.postprocessing.modules.jme.jetmetHelperRun2 import *
from PhysicsTools.NanoAODTools.postprocessing.framework.crabhelper import inputFiles,runsAndLumis
from PhysicsTools.NanoAODTools.postprocessing.modules.common.puWeightProducer import *

###### questo posprocessor è per fare il topcand dopo il taglio taglio su Mtt sul dataset TT_inclusive i range di massa sono 700-1000 e 1000-inf#####
#p=PostProcessor('.', inputFiles(), '', modules=[Mtt_cut_gen_lvl(minMtt=1000,maxMtt=100000),GenPart_MomFirstCp(flavour='-5,-4,-3,-2,-1,1,2,3,4,5,6,-6,24,-24'),GenPart_hadronicTop(), Idx_PF(), deltaR_PF(),collectionMerger(input=["PFCands"], output="PFCands", sortkey=lambda x: x.pt, reverse=True, selector=None, maxObjects=None), nanoprepro(isMC=1),nanoTopcand(isMC=1)], friend=False, postfix=f"_topcand_PF", provenance=True, fwkJobReport=True, outputbranchsel='keep_and_drop.txt') # histFileName=histo_name, histDirName=histo_dir maxEntries=10000
###### questo è per il topcand su tutti gli altri dataset #####
p=PostProcessor('.', inputFiles(), '', modules=[GenPart_MomFirstCp(flavour='-5,-4,-3,-2,-1,1,2,3,4,5,6,-6,24,-24'),GenPart_hadronicTop(), Idx_PF(), deltaR_PF(),collectionMerger(input=["PFCands"], output="PFCands", sortkey=lambda x: x.pt, reverse=True, selector=None, maxObjects=None), nanoprepro(isMC=1),nanoTopcand(isMC=1)], friend=False, postfix=f"_topcand_PF", provenance=True, fwkJobReport=True, outputbranchsel='keep_and_drop.txt') # histFileName=histo_name, histDirName=histo_dir maxEntries=10000
p.run()
print('DONE')

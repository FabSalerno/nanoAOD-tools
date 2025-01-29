#!/usr/bin/bash
cd /afs/cern.ch/user/f/fsalerno/CMSSW_13_2_11/src/PhysicsTools/NanoAODTools/python/postprocessing/machine_learning/Training/
cmsenv
export XRD_NETWORKSTACK=IPv4
python3 training_Run3_hotvr_new_def.py -s QCD_HT1000_2018,QCD_HT1500_2018,QCD_HT2000_2018,QCD_HTInf_2018,TT_Mtt1000toInf_2018,TT_Mtt700to1000_2018,TT_semilep_2018 -i /eos/user/f/fsalerno/framework/MachineLearning/Training_HOTVR_2018_2_new_def/trainingSet.pkl -m /eos/user/f/fsalerno/framework/MachineLearning/Training_HOTVR_2018_2_new_def/model.h5 -j /eos/user/f/fsalerno/framework/MachineLearning/Training_HOTVR_2018_2_new_def/score_thresholds.json -g /eos/user/f/fsalerno/framework/MachineLearning/Training_HOTVR_2018_2_new_def/graphics

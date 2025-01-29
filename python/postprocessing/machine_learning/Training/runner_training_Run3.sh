#!/usr/bin/bash
cd /afs/cern.ch/user/f/fsalerno/CMSSW_13_2_11/src/PhysicsTools/NanoAODTools/python/postprocessing/machine_learning/Training/
cmsenv
export XRD_NETWORKSTACK=IPv4
python3 training_Run3.py -s QCD_HT1000to1200_2022,QCD_HT1200to1500_2022,QCD_HT1500to2000_2022,TT_semilep_2022 -i /eos/user/f/fsalerno/framework/MachineLearning/Training_PF_2022_1_prova_TROTA_full/trainingSet.pkl -m /eos/user/f/fsalerno/framework/MachineLearning/Training_PF_2022_1_prova_TROTA_full_300_pt/model.h5 -j /eos/user/f/fsalerno/framework/MachineLearning/Training_PF_2022_1_prova_TROTA_full_300_pt/score_thresholds.json -g /eos/user/f/fsalerno/framework/MachineLearning/Training_PF_2022_1_prova_TROTA_full_300_pt/graphics

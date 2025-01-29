#!/usr/bin/bash
cd /afs/cern.ch/user/f/fsalerno/CMSSW_13_2_11/src/PhysicsTools/NanoAODTools/python/postprocessing/machine_learning/Training/
cmsenv
export XRD_NETWORKSTACK=IPv4
python3 training_Run3_PF_jets_CNN.py -s QCD_HT1000to1200_2022,QCD_HT1200to1500_2022,QCD_HT1500to2000_2022,TT_semilep_2022 -i /eos/user/f/fsalerno/framework/MachineLearning/Training_PF_2022_1_jets_20_boosted/trainingSet.pkl -m /eos/user/f/fsalerno/framework/MachineLearning/Training_PF_2022_1_jets_20_boosted_CNN_morefeatures_300_pt/model.h5 -j /eos/user/f/fsalerno/framework/MachineLearning/Training_PF_2022_1_jets_20_boosted_CNN_morefeatures_300_pt/score_thresholds_20_CNN_300_pt.json -g /eos/user/f/fsalerno/framework/MachineLearning/Training_PF_2022_1_jets_20_boosted_CNN_morefeatures_300_pt/graphics -n 20 -d True -c 300 

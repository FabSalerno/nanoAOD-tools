#!/usr/bin/bash
cd /afs/cern.ch/user/f/fsalerno/CMSSW_13_2_11/src/PhysicsTools/NanoAODTools/python/postprocessing/machine_learning/Training/
cmsenv
export XRD_NETWORKSTACK=IPv4
python3 training_Run3_PF_jets_CNN_1D.py -s TT_semilep_2022 -i /eos/user/f/fsalerno/framework/MachineLearning/Training_PF_2022_1_jets_20_boosted/trainingSet.pkl -m /eos/user/f/fsalerno/framework/MachineLearning/Training_PF_2022_1_jets_20_boosted_CNN_1D/model.h5 -j /eos/user/f/fsalerno/framework/MachineLearning/Training_PF_2022_1_jets_20_boosted_CNN_1D/score_thresholds_20_CNN_1D.json -g /eos/user/f/fsalerno/framework/MachineLearning/Training_PF_2022_1_jets_20_boosted_CNN_1D/graphics -n 20

#!/usr/bin/bash
cd /afs/cern.ch/user/f/fsalerno/CMSSW_13_2_11/src/PhysicsTools/NanoAODTools/python/postprocessing/machine_learning/Training/
cmsenv
export XRD_NETWORKSTACK=IPv4
python3 training_Run3_PF_no_kinematics.py -s TT_semilep_2022 -i /eos/user/f/fsalerno/framework/MachineLearning/Training_PF_2022_1_jets_20_no_kinematics/trainingSet.pkl -m /eos/user/f/fsalerno/framework/MachineLearning/Training_PF_2022_1_jets_20_no_kinematics/model.h5 -j /eos/user/f/fsalerno/framework/MachineLearning/Training_PF_2022_1_jets_20_no_kinematics/score_thresholds.json -g /eos/user/f/fsalerno/framework/MachineLearning/Training_PF_2022_1_jets_20_no_kinematics/graphics

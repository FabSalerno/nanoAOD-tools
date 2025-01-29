#!/usr/bin/bash
cd /afs/cern.ch/user/f/fsalerno/CMSSW_12_5_2/src/PhysicsTools/NanoAODTools/python/postprocessing/machine_learning/Training/
cmsenv
export XRD_NETWORKSTACK=IPv4
python3 evaluate_graphics.py -s all -i /eos/user/f/fsalerno/Data/HOTVR/multiscore_evaluate/Merged_Friend_nanotopeval_HOTVR_1000_multiscore.root -g /eos/user/f/fsalerno/framework/MachineLearning/Training_HOTVR_2018_1_standard_old/plots/

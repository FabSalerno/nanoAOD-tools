#!/usr/bin/bash
cd /afs/cern.ch/user/l/lfavilla/CMSSW_12_6_0/src/PhysicsTools/NanoAODTools/python/postprocessing/my_analysis/my_framework/MLstudies/Training/Evaluate
cmsenv
export XRD_NETWORKSTACK=IPv4
python3 Evaluation.py -key base -eval_keys base -path_to_eval_folder /eos/user/f/fsalerno/framework/MachineLearning/Training_HOTVR_2018_1_standard/eval -path_to_model_folder /eos/user/f/fsalerno/framework/MachineLearning/Training_HOTVR_2018_1_standard -path_to_graphics_folder /eos/user/f/fsalerno/framework/MachineLearning/Training_HOTVR_2018_1_standard/plots/base

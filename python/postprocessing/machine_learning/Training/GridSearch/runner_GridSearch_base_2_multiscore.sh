#!/usr/bin/bash
cd /afs/cern.ch/user/f/fsalerno/CMSSW_12_5_2/src/PhysicsTools/NanoAODTools/python/postprocessing/machine_learning/Training/GridSearch
cmsenv
export XRD_NETWORKSTACK=IPv4
python3 grid_search_hotvr.py -save_graphics True -pt_flatten False -path_to_pkl_folder /eos/user/f/fsalerno/framework/MachineLearning/Training_HOTVR_2018_2_multiscore -pklName trainingSet.pkl -path_to_graphics_folder /eos/user/f/fsalerno/framework/MachineLearning/Grid_search_2/graphics_gridsearch/multiscore -path_to_model_folder /eos/user/f/fsalerno/framework/MachineLearning/Grid_search_2/grid_search_models/multiscore -modelName model_base_2_multiscore_balanced

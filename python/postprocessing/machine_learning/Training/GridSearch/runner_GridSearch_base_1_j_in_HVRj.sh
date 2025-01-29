#!/usr/bin/bash
cd /afs/cern.ch/user/f/fsalerno/CMSSW_13_2_11/src/PhysicsTools/NanoAODTools/python/postprocessing/machine_learning/Training/GridSearch
cmsenv
export XRD_NETWORKSTACK=IPv4
python3 grid_search_hotvr.py -save_graphics True -pt_flatten False -path_to_pkl_folder /eos/user/f/fsalerno/framework/MachineLearning/Training_HOTVR_2018_1_j_in_HVRj -pklName trainingSet.pkl -path_to_graphics_folder /eos/user/f/fsalerno/framework/MachineLearning/Grid_search_1/graphics_gridsearch/HOTVR_j_in_HVRj -path_to_model_folder /eos/user/f/fsalerno/framework/MachineLearning/Grid_search_1/grid_search_models/HOTVR_j_in_HVRj -modelName model_base_1_j_in_HVRj

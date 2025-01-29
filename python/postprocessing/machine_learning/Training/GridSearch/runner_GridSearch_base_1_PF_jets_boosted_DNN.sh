#!/usr/bin/bash
cd /afs/cern.ch/user/f/fsalerno/CMSSW_13_2_11/src/PhysicsTools/NanoAODTools/python/postprocessing/machine_learning/Training/GridSearch/
cmsenv
export XRD_NETWORKSTACK=IPv4
python3 grid_search_PF_jets_DNN.py -save_graphics True -pt_flatten False -path_to_pkl_folder /eos/user/f/fsalerno/framework/MachineLearning/Training_PF_2022_1_jets_20_boosted -pklName trainingSet.pkl -path_to_graphics_folder /eos/user/f/fsalerno/framework/MachineLearning/Grid_search_1/graphics_gridsearch/PF_jets_boosted_LSTM -path_to_model_folder /eos/user/f/fsalerno/framework/MachineLearning/Grid_search_1/grid_search_models/PF_jets_boosted_LSTM -modelName model_base_1

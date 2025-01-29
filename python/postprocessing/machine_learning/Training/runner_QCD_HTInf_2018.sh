#!/usr/bin/bash
cd /afs/cern.ch/user/f/fsalerno/CMSSW_13_2_11/src/PhysicsTools/NanoAODTools/python/postprocessing/machine_learning/Training/
cmsenv
export XRD_NETWORKSTACK=IPv4
python3 trainingSetHotvr_new_def.py -year 2018 -component QCD_HTInf_2018 -inFile_to_open /eos/user/f/fsalerno/Data/HOTVR/training_new_def/Merged_Friend_HOTVR_qcd_ht_inf_MC2018.root -nev -1 -path_to_pkl /eos/user/f/fsalerno/framework/MachineLearning/Training_HOTVR_2018_1_new_def/pkls/trainingSet_QCD_HTInf_2018.pkl

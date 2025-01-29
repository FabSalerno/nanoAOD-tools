#!/usr/bin/bash
cd /afs/cern.ch/user/f/fsalerno/CMSSW_13_2_11/src/PhysicsTools/NanoAODTools/python/postprocessing/machine_learning/Training/
cmsenv
export XRD_NETWORKSTACK=IPv4
python3 trainingSet.py -year 2022 -component TT_semilep_2022 -inFile_to_open /eos/user/f/fsalerno/Data/TROTA/topcand/nano_mcRun3_ttsl1_topcand_TROTA_semilelp.root -nev -1 -path_to_pkl /eos/user/f/fsalerno/framework/MachineLearning/Training_PF_2022_1_prova_TROTA_full/pkls/trainingSet_TT_semilep_2022_100000.pkl

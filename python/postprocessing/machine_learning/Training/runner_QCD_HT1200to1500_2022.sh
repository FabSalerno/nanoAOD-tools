#!/usr/bin/bash
cd /afs/cern.ch/user/f/fsalerno/CMSSW_13_2_11/src/PhysicsTools/NanoAODTools/python/postprocessing/machine_learning/Training/
cmsenv
export XRD_NETWORKSTACK=IPv4
python3 trainingSet.py -year 2022 -component QCD_HT1200to1500_2022 -inFile_to_open /eos/user/f/fsalerno/Data/TROTA/topcand/nano_mcRun3_qcd_1200_1500_topcand_TROTA_qcd_1200_1500.root -nev -1 -path_to_pkl /eos/user/f/fsalerno/framework/MachineLearning/Training_PF_2022_1_prova_TROTA_full/pkls/trainingSet_QCD_HT1200to1500_2022.pkl

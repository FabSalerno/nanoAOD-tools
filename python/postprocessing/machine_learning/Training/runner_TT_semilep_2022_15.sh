#!/usr/bin/bash
cd /afs/cern.ch/user/f/fsalerno/CMSSW_13_2_11/src/PhysicsTools/NanoAODTools/python/postprocessing/machine_learning/Training/
cmsenv
export XRD_NETWORKSTACK=IPv4
python3 trainingSet_PF.py -year 2022 -component TT_semilep_2022 -inFile_to_open /eos/user/f/fsalerno/Data/PF/topcand/nano_mcRun3_ttsl1_topcand_PF_semilelp.root -nev -1 -path_to_pkl /eos/user/f/fsalerno/framework/MachineLearning/Training_PF_2022_1_jets_15_no_kinematics/pkls/trainingSet_TT_semilep_2022.pkl

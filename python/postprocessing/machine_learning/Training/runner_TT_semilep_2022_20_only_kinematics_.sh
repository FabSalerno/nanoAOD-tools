#!/usr/bin/bash
cd /afs/cern.ch/user/f/fsalerno/CMSSW_13_2_11/src/PhysicsTools/NanoAODTools/python/postprocessing/machine_learning/Training/
cmsenv
export XRD_NETWORKSTACK=IPv4
python3 trainingSet_PF_only_kinematics_.py -year {year} -component {component} -inFile_to_open {inFile_to_open} -nev {nev} -path_to_pkl {path_to_pkl}

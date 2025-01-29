#!/usr/bin/bash
cd /afs/cern.ch/user/f/fsalerno/CMSSW_13_2_11/src/PhysicsTools/NanoAODTools/crab/
cmsenv
export XRD_NETWORKSTACK=IPv4
python3 merging_trees.py -d /eos/user/f/fsalerno/Data/HOTVR/training_j_in_HVRj/qcd_ht_1000_MC2018_topcand/ -f qcd_ht_1000_MC2018.root -o /eos/user/f/fsalerno/Data/HOTVR/training_j_in_HVRj/ -n Merged_Friends_qcd_ht_1000_MC2018_HOTVR.root

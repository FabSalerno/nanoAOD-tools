#!/usr/bin/bash
cd /afs/cern.ch/user/f/fsalerno/CMSSW_12_5_2/src/PhysicsTools/NanoAODTools/python/postprocessing/machine_learning/Training/
cmsenv
export XRD_NETWORKSTACK=IPv4
python3 merging_trees.py -d /eos/user/g/gmilella/ttX_ntuplizer/tt_semilepton_MC2018_ntuplizer/ -f .root -o /eos/user/f/fsalerno/Data/HOTVR/tt_semilep_base/ -n Merged_Friends_all_tt_semilep_MC2018_3000.root

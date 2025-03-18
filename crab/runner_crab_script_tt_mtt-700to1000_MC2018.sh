#!/usr/bin/bash
cd /afs/cern.ch/user/f/fsalerno/CMSSW_13_2_11/src/PhysicsTools/NanoAODTools/crab/
cmsenv
export XRD_NETWORKSTACK=IPv4
python3 crab_script.py -dirpath /eos/user/f/fsalerno/Data/HOTVR/ttx_ntuplizer/tt_mtt-700to1000_MC2018_ntuplizer/ -component tt_mtt-700to1000_MC2018 

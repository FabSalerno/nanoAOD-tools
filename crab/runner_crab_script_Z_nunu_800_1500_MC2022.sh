#!/usr/bin/bash
cd /afs/cern.ch/user/f/fsalerno/CMSSW_13_2_11/src/PhysicsTools/NanoAODTools/crab/
cmsenv
export XRD_NETWORKSTACK=IPv4
python3 crab_script_PF.py -dirpath /eos/user/f/fsalerno/Data/PF/ -component Z_nunu_800_1500_MC2022 

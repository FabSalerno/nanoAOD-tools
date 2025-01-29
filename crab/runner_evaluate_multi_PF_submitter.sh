#!/usr/bin/bash
cd /afs/cern.ch/user/f/fsalerno/CMSSW_13_2_11/src/PhysicsTools/NanoAODTools/crab/
cmsenv
export XRD_NETWORKSTACK=IPv4
python3 evaluate_multi_PF.py

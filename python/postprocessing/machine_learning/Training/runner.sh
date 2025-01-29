#!/usr/bin/bash 
cd /afs/cern.ch/user/f/fsalerno/CMSSW_12_5_2/src/PhysicsTools/NanoAODTools/python/postprocessing/machine_learning/Training
cmsenv
export XRD_NETWORKSTACK=IPv4
python3 triningSet.py $1 $2 $3 $4 $5
#hadd $2 $3 histOut$4.root
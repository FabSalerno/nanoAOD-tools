import os
import optparse
import sys
import time
import json

usage = "python3 evaluate_graphics_submitter.py"
parser = optparse.OptionParser(usage)
# parser.add_option('-d', '--dryrun', dest='dryrun', default=True, action='store_false', help='Default do not run')
parser.add_option('-d', '--dryrun',
                  dest='dryrun',
                  default=False, 
                  action='store_true',
                  help='Default do not run')
#parser.add_option('-u', '--user', dest='us', type='string', default = 'ade', help="")
(opt, args) = parser.parse_args()
dryrun      = opt.dryrun

#Insert here your uid... you can see it typing echo $uid
username = str(os.environ.get('USER'))
inituser = str(os.environ.get('USER')[0])
if username == 'adeiorio':
    uid = 103214
elif username == 'acagnott':
    uid = 140541
elif username == 'lfavilla':
    uid = 159320
elif username == 'fsalerno':
    uid = 171405


def sub_writer(file_name):
    f = open("condor.sub", "w")
    f.write("Proxy_filename          = x509up\n")
    f.write("Proxy_path              = /afs/cern.ch/user/" + inituser + "/" + username + "/private/$(Proxy_filename)\n")
    f.write("universe                = vanilla\n")
    f.write("x509userproxy           = $(Proxy_path)\n")
    f.write("use_x509userproxy       = true\n")
    f.write("should_transfer_files   = YES\n")
    f.write("when_to_transfer_output = ON_EXIT\n")
    f.write("transfer_input_files    = $(Proxy_path)\n")
    #f.write("transfer_output_remaps  = \""+outname+"_Skim.root=root://eosuser.cern.ch///eos/user/"+inituser + "/" + username+"/DarkMatter/topcandidate_file/"+dat_name+"_Skim.root\"\n")
    f.write('requirements            = (TARGET.OpSysAndVer =?= "CentOS7")\n')
    f.write("+JobFlavour             = \"nextweek\"\n") # options are espresso = 20 minutes, microcentury = 1 hour, longlunch = 2 hours, workday = 8 hours, tomorrow = 1 day, testmatch = 3 days, nextweek     = 1 week
    f.write("executable              = runner_"+file_name+".sh\n")
    f.write("arguments               = \n")
    #f.write("input                   = input.txt\n")
    f.write("output                  = condor/output/"+file_name+".out\n")
    f.write("error                   = condor/error/"+file_name+".err\n")
    f.write("log                     = condor/log/"+file_name+".log\n")
    f.write("queue")



def sh_writer(file_name, components, evaluation_set, graphics_path):
    f = open("runner_"+file_name+".sh", "w")
    f.write("#!/usr/bin/bash\n")
    f.write("cd /afs/cern.ch/user/f/fsalerno/CMSSW_12_5_2/src/PhysicsTools/NanoAODTools/python/postprocessing/machine_learning/Training/\n")
    f.write("cmsenv\n")
    f.write("export XRD_NETWORKSTACK=IPv4\n")
    f.write(f"python3 {file_name}.py -s {components} -i {evaluation_set} -g {graphics_path}\n")


if not os.path.exists("condor/output"):
    os.makedirs("condor/output")
if not os.path.exists("condor/error"):
    os.makedirs("condor/error")
if not os.path.exists("condor/log"):
    os.makedirs("condor/log")
if(uid==0):
    print("Please insert your uid")
    exit()
if not os.path.exists("/tmp/x509up_u" + str(uid)):
    os.system('voms-proxy-init --rfc --voms cms -valid 192:00')
os.popen("cp /tmp/x509up_u" + str(uid) + " /afs/cern.ch/user/" + inituser + "/" + username + "/private/x509up")


file_name  = "evaluate_graphics_2"
evaluation_set    = "/eos/user/f/fsalerno/Data/HOTVR/multiscore_evaluate/Merged_Friend_tt_mtt-700to1000_MC2018_nanotopeval_HOTVR_1000_multiscore.root"
#evaluation_set    = "/eos/user/f/fsalerno/Data/HOTVR/multiscore_evaluate/Merged_Friend_semilepton_MC2018_nanotopeval_HOTVR_1000_multiscore.root"
#evaluation_set    = "/eos/user/f/fsalerno/Data/HOTVR/multiscore_evaluate/Merged_Friend_qcd_ht_inf_MC2018_nanotopeval_HOTVR_1000_multiscore.root"
graphics_path   = "/eos/user/f/fsalerno/framework/MachineLearning/Training_HOTVR_2018_1_standard_old/plots/"
component = "TT_Mtt700to1000_2018"
#component = "QCD_HTInf_2018"
#component = "TT_semilep_2018"
#component = "all"

sh_writer(file_name, component, evaluation_set, graphics_path)    
sub_writer(file_name)
if not dryrun:
    os.popen('condor_submit condor.sub')
time.sleep(2)
    




import os
import optparse
import sys
import time
import json




usage = "python3 crab_script_submitter.py"
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
    f = open(f"condor_{file_name}.sub", "w")
    f.write("Proxy_filename          = x509up\n")
    f.write("Proxy_path              = /afs/cern.ch/user/" + inituser + "/" + username + "/private/$(Proxy_filename)\n")
    f.write("universe                = vanilla\n")
    f.write("x509userproxy           = $(Proxy_path)\n")
    f.write("use_x509userproxy       = true\n")
    f.write("should_transfer_files   = YES\n")
    f.write("when_to_transfer_output = ON_EXIT\n")
    f.write("transfer_input_files    = $(Proxy_path)\n")
    #f.write("transfer_output_remaps  = \""+outname+"_Skim.root=root://eosuser.cern.ch///eos/user/"+inituser + "/" + username+"/DarkMatter/topcandidate_file/"+dat_name+"_Skim.root\"\n")
    f.write("environment             = \"SCRAM_ARCH=el9_amd64_gcc11\"\n")
    #f.write('MY.WantOS               = "el7"\n')
    #f.write('+DesiredOS              = "EL7"\n')
    #f.write('requirements            = (UtsnameNodename != "b7s01p9733.cern.ch")\n')
    #f.write('requirements            = (TARGET.OpSysAndVer == "CentOS7")\n')
    f.write("+JobFlavour             = \"tomorrow\"\n") # options are espresso = 20 minutes, microcentury = 1 hour, longlunch = 2 hours, workday = 8 hours, tomorrow = 1 day, testmatch = 3 days, nextweek     = 1 week
    #f.write("executable              = singularity_wrapper_"+file_name+".sh\n")
    #f.write("arguments               = runner_"+file_name+".sh\n")
    f.write("executable              = runner_"+file_name+".sh\n")
    f.write("arguments               = \n")
    #f.write("input                   = input.txt\n")
    f.write("output                  = condor/output/"+file_name+".out\n")
    f.write("error                   = condor/error/"+file_name+".err\n")
    f.write("log                     = condor/log/"+file_name+".log\n")
    #f.write('+SingularityImage       = "/cvmfs/cms.cern.ch/common/cmssw-el7.sif"\n')
    #f.write('requirements            = (HAS_SINGULARITY == True)\n')
    f.write("queue")


    
def sh_writer(file_name):
    f = open("runner_"+file_name+".sh", "w")
    f.write("#!/usr/bin/bash\n")
    f.write("cd /afs/cern.ch/user/f/fsalerno/CMSSW_13_2_11/src/PhysicsTools/NanoAODTools/crab/\n")
    f.write("cmsenv\n")
    f.write("export XRD_NETWORKSTACK=IPv4\n")
    #f.write("cmsenv\n")
    f.write(f"python3 evaluate_multi_PF.py\n")


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




file_name  = f"evaluate_multi_PF_submitter"

sh_writer(file_name)    
sub_writer(file_name)
if not dryrun:
    os.popen(f'condor_submit condor_{file_name}.sub')
time.sleep(2)
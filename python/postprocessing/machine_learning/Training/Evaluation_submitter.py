import os
import optparse
import sys
import time
import json
# from samples.samples import *
# from get_file_fromdas import *
# Datasets
import PhysicsTools.NanoAODTools.postprocessing.machine_learning.Training.Datasets as Datasets


usage = 'python submit_condor.py -d'
parser = optparse.OptionParser(usage)
parser.add_option('-d', '--dryrun', dest='dryrun', default=True, action='store_false', help='Default do not run')
#parser.add_option('-u', '--user', dest='us', type='string', default = 'ade', help="")
(opt, args) = parser.parse_args()
#Insert here your uid... you can see it typing echo $uid

dryrun = opt.dryrun

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



def sub_writer(key):
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
    f.write("+JobFlavour             = \"longlunch\"\n") # options are espresso = 20 minutes, microcentury = 1 hour, longlunch = 2 hours, workday = 8 hours, tomorrow = 1 day, testmatch = 3 days, nextweek     = 1 week
    f.write("executable              = runner_"+key+".sh\n")
    f.write("arguments               = \n")
    #f.write("input                   = input.txt\n")
    f.write("output                  = condor/output/"+ key+".out\n")
    f.write("error                   = condor/error/"+ key+".err\n")
    f.write("log                     = condor/log/"+ key+".log\n")
    f.write("queue\n")

'''
key possible values:
"base", "base_pt_g250", "base_pt_l250"
"base_3j0fj", "base_pt_g250_3j0fj", "base_pt_l250_3j0fj"
"base_3j1fj", "base_pt_g250_3j1fj", "base_pt_l250_3j1fj"
"base_2j1fj", "base_pt_g250_2j1fj", "base_pt_l250_2j1fj"
"base_3j1fj_2j1fj", "base_pt_g250_3j1fj_2j1fj", "base_pt_l250_3j1fj_2j1fj"
"pt_flatten", "pt_flatten_pt_g250", "pt_flatten_pt_l250"
'''

def sh_writer(key, eval_keys, path_to_eval_folder, path_to_model_folder, path_to_graphics_folder):
    f = open("runner_"+key+".sh", "w")
    f.write("#!/usr/bin/bash\n")
    f.write("cd /afs/cern.ch/user/l/lfavilla/CMSSW_12_6_0/src/PhysicsTools/NanoAODTools/python/postprocessing/my_analysis/my_framework/MLstudies/Training/Evaluate\n")
    f.write("cmsenv\n")
    f.write("export XRD_NETWORKSTACK=IPv4\n")
    f.write(f"python3 Evaluation.py -key {key} -eval_keys {eval_keys} -path_to_eval_folder {path_to_eval_folder} -path_to_model_folder {path_to_model_folder} -path_to_graphics_folder {path_to_graphics_folder}\n")








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




###### Loop on datasets ######
datasets = Datasets.datasets
# keys     = datasets.keys()
keys     = ["base"] 
# keys     = ["base_pt_g400", "base_pt_l400"]
eval_keys            = ",".join(list(datasets.keys()))
path_to_eval_folder  = "/eos/user/f/fsalerno/framework/MachineLearning/Training_HOTVR_2018_1_standard/eval"
path_to_model_folder = "/eos/user/f/fsalerno/framework/MachineLearning/Training_HOTVR_2018_1_standard"
for key in keys:
    path_to_graphics_folder = f"/eos/user/f/fsalerno/framework/MachineLearning/Training_HOTVR_2018_1_standard/plots/{key}"
    sh_writer(key=key, eval_keys=eval_keys, path_to_eval_folder=path_to_eval_folder, path_to_model_folder=path_to_model_folder, path_to_graphics_folder=path_to_graphics_folder)    
    sub_writer(key=key)
    if not dryrun:
        os.popen('condor_submit condor.sub')
    time.sleep(2)
        
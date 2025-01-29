import os
import optparse
import sys
import time
import json
# from samples.samples import *
# from get_file_fromdas import *



usage = "python3 training_Run3_hotvr_submitter.py"
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
    f.write("environment             = \"SCRAM_ARCH=el9_amd64_gcc11\"\n")
    #f.write("transfer_output_remaps  = \""+outname+"_Skim.root=root://eosuser.cern.ch///eos/user/"+inituser + "/" + username+"/DarkMatter/topcandidate_file/"+dat_name+"_Skim.root\"\n")
    f.write("+JobFlavour             = \"workday\"\n") # options are espresso = 20 minutes, microcentury = 1 hour, longlunch = 2 hours, workday = 8 hours, tomorrow = 1 day, testmatch = 3 days, nextweek     = 1 week
    f.write("executable              = runner_"+file_name+".sh\n")
    f.write("arguments               = \n")
    #f.write("input                   = input.txt\n")
    f.write("output                  = condor/output/"+file_name+".out\n")
    f.write("error                   = condor/error/"+file_name+".err\n")
    f.write("log                     = condor/log/"+file_name+".log\n")
    f.write("queue")



def sh_writer(file_name, samples, training_set, model_path, outJson_path, graphics_path):
    f = open("runner_"+file_name+".sh", "w")
    f.write("#!/usr/bin/bash\n")
    f.write("cd /afs/cern.ch/user/f/fsalerno/CMSSW_13_2_11/src/PhysicsTools/NanoAODTools/python/postprocessing/machine_learning/Training/\n")
    f.write("cmsenv\n")
    f.write("export XRD_NETWORKSTACK=IPv4\n")
    f.write(f"python3 {file_name}.py -s {samples} -i {training_set} -m {model_path} -j {outJson_path} -g {graphics_path}\n")


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




###### Launcher ######
file_name  = "training_Run3_hotvr_new_def"

year = 2018

if year==2018:
    components = [
        'QCD_HT1000_2018', 
        'QCD_HT1500_2018', 
        'QCD_HT2000_2018', 
        'QCD_HTInf_2018', 
        'TT_Mtt1000toInf_2018', 
        'TT_Mtt700to1000_2018', 
        'TT_semilep_2018',
        #"TprimeBToTZ_M1200_2018", 
        #"TprimeBToTZ_M1800_2018", 
        #"TprimeBToTZ_M800_2018", 
        #"ZJetsToNuNu_HT1200To2500_2018", 
        #"ZJetsToNuNu_HT200To400_2018", 
        #"ZJetsToNuNu_HT2500ToInf_2018", 
        #"ZJetsToNuNu_HT400To600_2018", 
        #"ZJetsToNuNu_HT800To1200_2018", 
        #"tDM_Mphi1000_2018", 
        #"tDM_Mphi500_2018", 
        #"tDM_Mphi50_2018"
        ]
    
if year==2022:
    components = [
        "QCD_HT800to1000_2022",
        "QCD_HT1000to1200_2022",
        "QCD_HT1200to1500_2022",
        "QCD_HT1500to2000_2022",
        "QCD_HT2000_2022",
        "TprimeToTZ_700_2022",
        "TprimeToTZ_1000_2022",
        "TprimeToTZ_1800_2022",
        "TT_hadr_2022",
        "TT_semilep_2022",
        "WJets_2022",
        "ZJetsToNuNu_HT800to1500_2022",
        "ZJetsToNuNu_HT1500to2500_2022",
        "ZJetsToNuNu_HT2500_2022"
        ]
samples         = ','.join(components)

######## Run3, phase 1 & 2 ########
phase               = 2  ##!!!!!ATTENZIONE ALLA FASE!!!!!
if phase == 1:
    training_set    = "/eos/user/f/fsalerno/framework/MachineLearning/Training_HOTVR_2018_1_new_def/trainingSet.pkl"
    model_path      = "/eos/user/f/fsalerno/framework/MachineLearning/Training_HOTVR_2018_1_new_def/model.h5"
    outJson_path    = "/eos/user/f/fsalerno/framework/MachineLearning/Training_HOTVR_2018_1_new_def/score_thresholds.json"
    graphics_path   = "/eos/user/f/fsalerno/framework/MachineLearning/Training_HOTVR_2018_1_new_def/graphics"
elif phase == 2:
    training_set    = "/eos/user/f/fsalerno/framework/MachineLearning/Training_HOTVR_2018_2_new_def/trainingSet.pkl"
    model_path      = "/eos/user/f/fsalerno/framework/MachineLearning/Training_HOTVR_2018_2_new_def/model.h5"
    outJson_path    = "/eos/user/f/fsalerno/framework/MachineLearning/Training_HOTVR_2018_2_new_def/score_thresholds.json"
    graphics_path   = "/eos/user/f/fsalerno/framework/MachineLearning/Training_HOTVR_2018_2_new_def/graphics"


sh_writer(file_name, samples, training_set, model_path, outJson_path, graphics_path)    
sub_writer(file_name)
if not dryrun:
    os.popen('condor_submit condor.sub')
time.sleep(2)
    




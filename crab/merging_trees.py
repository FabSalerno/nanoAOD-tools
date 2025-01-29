import ROOT
import os
from ROOT import TFile, TTree, TList


from argparse import ArgumentParser
parser                      = ArgumentParser()
parser.add_argument("-dirpath",                                 dest="dirpath",                                  default="/eos/user/f/fsalerno/Data/HOTVR/ttX_ntuplizer/tt_semilepton_MC2018_ntuplizer/",               required=True,         type=str,       help="path to file")
parser.add_argument("-file_end",                                dest="file_end",                                 default=".root",                                                                                       required=True,         type=str,       help="file end for the loop")
parser.add_argument("-outdir",                                  dest="outdir",                                   default="/eos/user/f/fsalerno/Data/HOTVR",                                                             required=True,         type=str,       help="output path")
parser.add_argument("-name_out",                                dest="name_out",                                default="semilepton.root",                                                                             required=True,         type=str,       help="output name")

options                     = parser.parse_args()

### ARGS ###
dirpath                        = options.dirpath
file_end                       = options.file_end
outdir                         = options.outdir
name_out                       = options.name_out 

if not os.path.exists(outdir):
    os.makedirs(outdir)
    print(f"Directory {outdir} created")

#dirpath = "/eos/user/f/fsalerno/Data/evaluate/"
#dirpath = "/eos/user/f/fsalerno/Data/HOTVR/ttX_ntuplizer/tt_mtt-700to1000_MC2018_ntuplizer/"
#dirpath = "/eos/user/f/fsalerno/Data/HOTVR/evaluate_2/"
#dirpath = "/eos/user/f/fsalerno/Data/HOTVR/ttX_ntuplizer/qcd_ht_2000_MC2018_ntuplizer/"
#dirpath = "/eos/user/f/fsalerno/Data/HOTVR/ttX_ntuplizer/tt_semilepton_MC2018_ntuplizer/"
#file_end = "nanotopeval_HOTVR_1000_multiscore.root"
#file_end = "MC2018_topeval_HOTVR_10000.root"
pathList = []
for f,file_name in enumerate(os.listdir(dirpath)): 
    if (not file_name.startswith('.')):
        if (file_name.endswith(file_end)):
            print("\n",file_name,"\n")
            pathList.append(dirpath+file_name) 
print("pathList is ===== ",pathList)

treeList = TList()
outputFile = TFile(outdir+name_out, 'recreate')
#outputFile = TFile("/eos/user/f/fsalerno/Data/HOTVR/Merged_Friend_evaluate_tt_mtt-700to1000_MC2018_ntuplizer.root", 'recreate')
pyfilelist = []
pytreelist = []

for path in pathList:
    print("Path", path)
    inputFile = TFile(path, 'read')
    if inputFile.IsZombie():  # Check if the file is successfully opened
        print(f"Failed to open file: {path}")
        continue
    pyfilelist.append(inputFile)  # Make this TFile survive the loop!
    inputTree = inputFile.Get('Friends')
    if not inputTree:
        print(f"Failed to get 'Friends' tree from file: {path}")
        continue
    pytreelist.append(inputTree)  # Make this TTree survive the loop!
    treeList.Add(inputTree)
    print("size of treeList",treeList.GetSize())

outputFile.cd()
if treeList.GetSize() > 0:
    outputTree = TTree.MergeTrees(treeList)
    #print("output Tree",outputTree.GetKeys())
    outputFile.Write()
else:
    print("No trees were added to the list. Output file not written.")
outputFile.Close()
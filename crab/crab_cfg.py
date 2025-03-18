from WMCore.Configuration import Configuration

config = Configuration()
config.section_('General')
config.General.requestName = 'TT_inclusive_2022_topcand_hadd'
config.General.transferLogs=True
config.section_('JobType')
config.JobType.pluginName = 'Analysis'
config.JobType.psetName = 'PSet.py'
config.JobType.maxJobRuntimeMin = 2700
config.JobType.scriptExe = 'crab_script.sh'
#config.JobType.inputFiles = ['crab_script.py','../scripts/haddnano.py', '../scripts/keep_and_drop.txt', '../../../install_cmssw.sh']
#config.JobType.inputFiles = ['crab_script.py', '../scripts/keep_and_drop.txt']
config.JobType.inputFiles = ['crab_script.py','../scripts/haddnano.py', '../scripts/keep_and_drop.txt']
#config.JobType.sendVenvFolder = True
config.section_('Data')
config.Data.inputDataset = '/TT_TuneCP5_13p6TeV_powheg-pythia8/fsalerno-TT_inclusive_2022-0fa328e40e38f44cd311b92489b92b5b/USER'
config.Data.allowNonValidInputDataset = True
config.Data.inputDBS = 'phys03'
config.Data.splitting = 'FileBased'
config.Data.unitsPerJob = 1
config.Data.outLFNDirBase = '/store/user/%s/%s' % ('fsalerno', 'topcand')
config.Data.publication = True
config.Data.publishDBS = 'phys03'
config.Data.outputDatasetTag = 'TT_inclusive_2022_topcand_hadd'
config.section_('Site')
config.Site.storageSite = 'T2_IT_Pisa'

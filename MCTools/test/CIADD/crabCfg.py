
#from WMCore.Configuration import Configuration
#config = Configuration()
from CRABClient.UserUtilities import config, getUsernameFromSiteDB
config = config()

#config.section_("General")
config.General.requestName = 'ADD_LambdaT10000_Des_M6000ToInf_13TeV-pythia8_20180827'
config.General.workArea = 'crab'
config.General.transferOutputs = True


#config.section_("JobType")
config.JobType.pluginName = 'PrivateMC'
config.JobType.psetName = 'ADD_LambdaT10000_Des_M6000ToInf_13TeV-pythia8_forCRAB_cff.py'

#config.section_("Data")
config.Data.outputPrimaryDataset = 'ADD_LambdaT10000_Des_M6000ToInf_13TeV-pythia8'
config.Data.inputDBS = 'global'
config.Data.splitting = 'EventBased'
config.Data.unitsPerJob = 1000000
config.Data.totalUnits = 1000000
config.JobType.eventsPerLumi = 10000
config.Data.publication = False
config.Data.publishDBS = 'phys03' 
config.Data.outputDatasetTag = 'ADD_LambdaT10000_Des_M6000ToInf_13TeV-pythia8'
config.Data.outLFNDirBase = '/store/user/jschulte/ADD/'
 
#config.section_("Site")
config.Site.storageSite = "T2_US_Purdue"

#config.section_("User")

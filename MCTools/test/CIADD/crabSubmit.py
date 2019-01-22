import subprocess

crabTemplate='''
#from WMCore.Configuration import Configuration
#config = Configuration()
from CRABClient.UserUtilities import config, getUsernameFromSiteDB
config = config()

#config.section_("General")
config.General.requestName = '%s_20180827'
config.General.workArea = 'crab'
config.General.transferOutputs = True


#config.section_("JobType")
config.JobType.pluginName = 'PrivateMC'
config.JobType.psetName = '%s'

#config.section_("Data")
config.Data.outputPrimaryDataset = '%s'
config.Data.inputDBS = 'global'
config.Data.splitting = 'EventBased'
config.Data.unitsPerJob = 1000000
config.Data.totalUnits = 1000000
config.JobType.eventsPerLumi = 10000
config.Data.publication = False
config.Data.publishDBS = 'phys03' 
config.Data.outputDatasetTag = '%s'
config.Data.outLFNDirBase = '/store/user/jschulte/ADD/'
 
#config.section_("Site")
config.Site.storageSite = "T2_US_Purdue"

#config.section_("User")
'''


#masses = [1000,1500,2000,2500,3000,3500,4000,4500,5000,5500,6000,6500,7000,7500,8000]
lambdaTs = [4000,5000,6000,7000,8000,9000,10000]
massBins = [120,200,400,800,1400,2300,3500,4500,6000,-1]
#models = ["ZPrimeQ","ZPrimeSSM","ZPrimeSQ","ZPrimeR","ZPrimeB-L","ZPrimeLR","ZPrimeY","ZPrimeT3L"]
#decays = {"EE":11}i
decayN = 11
interferences = ["Con","Des"]
if True:
	for lambdaT in lambdaTs:
		for i in range(0,len(massBins)-1):
				for interference in interferences:
					if massBins[i+1] == -1:
						requestName = "ADD_LambdaT%d_%s_M%dToInf_13TeV-pythia8"%(lambdaT,interference,massBins[i])
						fragmentName = "ADD_LambdaT%d_%s_M%dToInf_13TeV-pythia8_cff.py"%(lambdaT,interference,massBins[i])
						outName = "ADD_LambdaT%d_%s_M%dToInf_13TeV-pythia8_forCRAB_cff.py"%(lambdaT,interference,massBins[i])
					else:
						requestName = "ADD_LambdaT%d_%s_M%dTo%d_13TeV-pythia8"%(lambdaT,interference,massBins[i],massBins[i+1])
						fragmentName = "ADD_LambdaT%d_%s_M%dTo%d_13TeV-pythia8_cff.py"%(lambdaT,interference,massBins[i],massBins[i+1])
						outName = "ADD_LambdaT%d_%s_M%dTo%d_13TeV-pythia8_forCRAB_cff.py"%(lambdaT,interference,massBins[i],massBins[i+1])
					with open('%s'%outName, "w") as outfile:
						subprocess.call(["python","runFragment.py","fragment=%s"%fragmentName,"decay=%s"%decayN],stdout=outfile)	

					crabCfg = crabTemplate%(requestName,outName,requestName,requestName)
					f = open("crabCfg.py","w")
					f.write(crabCfg)
					f.close()
					print fragmentName
					print requestName
					print outName
					print
					subprocess.call(["crab","submit","crabCfg.py"])



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
config.Data.unitsPerJob = 100000
config.Data.totalUnits = 100000
config.Data.publication = False
config.Data.publishDBS = 'phys03' 
config.Data.outputDatasetTag = '%s'
config.Data.outLFNDirBase = '/store/user/jschulte/ADD/'
 
#config.section_("Site")
config.Site.storageSite = "T2_US_Purdue"

#config.section_("User")
'''

lambdas = [16000,22000,28000,32000,40000]
massBins = [120,200,400,800,1400,2300,3500,4500,6000,-1]
helicities = ["ConLL","ConLR","ConRR","DesRR","DesLR","DesLL"]
decayN = 11
for l in lambdas:
        for i in range(0,len(massBins)-1):
                        for hel  in helicities:

					if massBins[i+1] == -1:
						requestName = "CI_Lambda%d_%s_M%dToInf_13TeV-pythia8"%(l/1000,hel,massBins[i])
						fragmentName = "CI_Lambda%d_%s_M%dToInf_13TeV-pythia8_cff.py"%(l/1000,hel,massBins[i])
						outName = "CI_Lambda%d_%s_M%dToInf_13TeV-pythia8_forCRAB_cff.py"%(l/1000,hel,massBins[i])
					else:
						requestName = "CI_Lambda%d_%s_M%dTo%d_13TeV-pythia8"%(l/1000,hel,massBins[i],massBins[i+1])
						fragmentName = "CI_Lambda%d_%s_M%dTo%d_13TeV-pythia8_cff.py"%(l/1000,hel,massBins[i],massBins[i+1])
						outName = "CI_Lambda%d_%s_M%dTo%d_13TeV-pythia8_forCRAB_cff.py"%(l/1000,hel,massBins[i],massBins[i+1])
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



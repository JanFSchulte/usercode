import math

template = '''
import FWCore.ParameterSet.Config as cms

from Configuration.Generator.Pythia8CommonSettings_cfi import *
from Configuration.Generator.Pythia8CUEP8M1Settings_cfi import *

generator = cms.EDFilter("Pythia8GeneratorFilter",
    maxEventsToPrint = cms.untracked.int32(1),
    pythiaPylistVerbosity = cms.untracked.int32(1),
    filterEfficiency = cms.untracked.double(1.0),
    pythiaHepMCVerbosity = cms.untracked.bool(False),
    comEnergy = cms.double(13000.),
    PythiaParameters = cms.PSet(
        pythia8CommonSettingsBlock,
        pythia8CUEP8M1SettingsBlock,
        processParameters = cms.vstring(
            'ContactInteractions:QCffbar2eebar = on',
            'PhaseSpace:mHatMin = %(minMass)d',
            'PhaseSpace:mHatMax = %(maxMass)d',
            'ContactInteractions:Lambda = %(lambda)d',
            'ContactInteractions:etaLL = %(etaLL)d',
            'ContactInteractions:etaRR = %(etaRR)d',
            'ContactInteractions:etaLR = %(etaLR)d',
       ),
        parameterSets = cms.vstring('pythia8CommonSettings',
                                    'pythia8CUEP8M1Settings',
                                    'processParameters',
                                    )
    )
)
'''

lambdas = [16000,22000,28000,32000,40000]
massBins = [120,200,400,800,1400,2300,3500,4500,6000,-1]
helicities = ["ConLL","ConLR","ConRR","DesRR","DesLR","DesLL"]
for l in lambdas:
	for i in range(0,len(massBins)-1):
			for hel  in helicities:
				params = {}
				params["lambda"] = l
				params["minMass"] = massBins[i]
				params["maxMass"] = massBins[i+1]
				if hel == "ConLL":
					params["etaLL"]  = -1
					params["etaRR"]  = 0
					params["etaLR"]  = 0
				elif hel == "ConLR":
					params["etaLL"]  = 0
					params["etaRR"]  = 0
					params["etaLR"]  = -1
				elif hel == "ConRR":
					params["etaLL"]  = 0
					params["etaRR"]  = 0
					params["etaLR"]  = -1
				elif hel == "DesLL":
					params["etaLL"]  = 1
					params["etaRR"]  = 0
					params["etaLR"]  = 0
				elif hel == "DesLR":
					params["etaLL"]  = 0
					params["etaRR"]  = 0
					params["etaLR"]  = 1
				elif hel == "DesRR":
					params["etaLL"]  = 0
					params["etaRR"]  = 1
					params["etaLR"]  = 0

				fragment = template%params
				if massBins[i+1] == -1:
					f = open("CI_Lambda%d_%s_M%dToInf_13TeV-pythia8_cff.py"%(l/1000,hel,massBins[i]),"w")
				else:
					f = open("CI_Lambda%d_%s_M%dTo%d_13TeV-pythia8_cff.py"%(l/1000,hel,massBins[i],massBins[i+1]),"w")
				f.write(fragment)
				f.close()




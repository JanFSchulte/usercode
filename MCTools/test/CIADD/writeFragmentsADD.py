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
            'ExtraDimensionsLED:LambdaT = %(lambdaT)d',
            'ExtraDimensionsLED:ffbar2llbar = on',
            'ExtraDimensionsLED:gg2llbar = on',
            'ExtraDimensionsLED:NegInt = %(int)d',
            'ExtraDimensionsLED:CutOffmode = 0',
            'PhaseSpace:mHatMin = %(minMass)d',
            'PhaseSpace:mHatMax = %(maxMass)d',
        ),
        parameterSets = cms.vstring('pythia8CommonSettings',
                                    'pythia8CUEP8M1Settings',
                                    'processParameters',
                                    )
    )
)
'''

lambdaTs = [5000,6000,7000,8000,9000,10000,11000,12000]
massBins = [300,800,1300,2000,-1]
decays = {"EE":11,"MuMu":13}
interferences = {"Con":0,"Des":1}
for lambdaT in lambdaTs:
	for i in range(0,len(massBins)-1):
			for interference, intN in interferences.iteritems():
				params = {}
				params["lambdaT"] = lambdaT
				params["minMass"] = massBins[i]
				params["maxMass"] = massBins[i+1]
				params["int"] = intN

				fragment = template%params
				if massBins[i+1] == -1:
					if interference == "Con":
						f = open("ADDGravToLL_LambdaT-%d_M-%dToInf_13TeV-pythia8_cff.py"%(lambdaT,massBins[i]),"w")
					else:	
						f = open("ADDGravToLL_LambdaT-%d_%s_M-%dToInf_13TeV-pythia8_cff.py"%(lambdaT,interference,massBins[i]),"w")
				else:
					if interference == "Con":
						f = open("ADDGravToLL_LambdaT-%d_M-%dTo%d_13TeV-pythia8_cff.py"%(lambdaT,massBins[i],massBins[i+1]),"w")
					else:
						f = open("ADDGravToLL_LambdaT-%d_%s_M-%dTo%d_13TeV-pythia8_cff.py"%(lambdaT,interference,massBins[i],massBins[i+1]),"w")
				f.write(fragment)
				f.close()




import math

template = '''
import FWCore.ParameterSet.Config as cms

from Configuration.Generator.Pythia8CommonSettings_cfi import *
from Configuration.Generator.Pythia8CUEP8M1Settings_cfi import *

generator = cms.EDFilter("Pythia8GeneratorFilter",
        comEnergy = cms.double(13000),
        filterEfficiency = cms.untracked.double(1),
        maxEventsToPrint = cms.untracked.int32(0),
        pythiaHepMCVerbosity = cms.untracked.bool(False),
        pythiaPylistVerbosity = cms.untracked.int32(1),
        PythiaParameters = cms.PSet(
	        pythia8CommonSettingsBlock,
		pythia8CUEP8M1SettingsBlock,
                processParameters = cms.vstring(
                        'NewGaugeBoson:ffbar2gmZZPrime = on',
                        'Zprime:gmZmode = %(interference)d',
                        'Zprime:universality = on',
                        'Zprime:vd=%(dV)f',
                        'Zprime:ad=%(dA)f',
                        'Zprime:vu=%(uV)f',
                        'Zprime:au=%(uA)f',
                        'Zprime:ve=%(eV)f',
                        'Zprime:ae=%(eA)f',
                        'Zprime:vnue=%(nuV)f',
                        'Zprime:anue=%(nuA)f',
                        '32:m0 = %(mass)d',
                        '32:onMode = off',
                        '32:onIfAny = %(decay)d',
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

def setZPrimeParams(model):
	result = {}
	if model=="ZPrimeChi":
	    print "Z' chi "
	    sinThetaW=math.sqrt(0.23)
	    result["dV"]=2*math.sqrt(6)*sinThetaW/3
	    result["dA"]=-math.sqrt(6)*sinThetaW/3
	    result["uV"]=0
	    result["uA"]=math.sqrt(6)*sinThetaW/3
	    result["eV"]=-result["dV"]
	    result["eA"]=result["dA"]
	    result["nuV"]=-math.sqrt(6)*sinThetaW/2;
	    result["nuA"]=result["nuV"]

	    
	elif model=="ZPrimeEta":
	    print "Z' eta"
	    sinThetaW=math.sqrt(0.23)
	    result["dV"]=sinThetaW
	    result["dA"]=sinThetaW/3
	    result["uV"]=0
	    result["uA"]=4*sinThetaW/3
	    result["eV"]=-result["dV"]
	    result["eA"]=result["dA"]
	    result["nuV"]=-sinThetaW/3;
	    result["nuA"]=result["nuV"]

	elif model=="ZPrimeI":
	    print "Z' I"
	    sinThetaW=math.sqrt(0.23)
	    
	    result["dV"]=math.sqrt(15)/3*sinThetaW
	    result["dA"]=-math.sqrt(15)/3*sinThetaW
	    result["uV"]=0
	    result["uA"]=0
	    result["eV"]=-result["dV"]
	    result["eA"]=result["dA"]
	    result["nuV"]=result["eV"]
	    result["nuA"]=result["eA"]
	    
	elif model=="ZPrimeSQ":
	    print "Z' SQ"
	    sinThetaW=math.sqrt(0.23)
	    
	    result["dV"]=3/2*sinThetaW
	    result["dA"]=-7/6*sinThetaW
	    result["uV"]=0
	    result["uA"]=sinThetaW/3
	    result["eV"]=-result["dV"]
	    result["eA"]=result["dA"]
	    result["nuV"]=-4/3*sinThetaW
	    result["nuA"]=-4/3*sinThetaW
	elif model=="ZPrimeN":
	    print "Z' N"
	    sinThetaW=math.sqrt(0.23)
	    
	    result["dV"]=-math.sqrt(6)/6*sinThetaW
	    result["dA"]=math.sqrt(6)/2*sinThetaW
	    result["uV"]=0
	    result["uA"]=math.sqrt(6)/3*sinThetaW
	    result["eV"]=-result["dV"]
	    result["eA"]=result["dA"]
	    result["nuV"]=math.sqrt(6)/3*sinThetaW
	    result["nuA"]=math.sqrt(6)/3*sinThetaW

	elif model=="ZPrimePSI":
	    print "Z' PSI"
	    result["dV"]=0
	    result["dA"]=0.506809
	    result["uV"]=0
	    result["uA"]=0.506809
	    result["eV"]=0
	    result["eA"]=0.506809
	    result["nuV"]=0.253405
	    result["nuA"]=0.253405

	elif model=="ZPrimeSSM":
	    print "Z' SSM"
	    result["dV"] = -0.693
	    result["dA"] = -1.
	    result["uV"] = 0.387
	    result["uA"] = 1.
	    result["eV"] = -0.08
	    result["eA"] = -1.
	    result["nuV"] = 1
	    result["nuA"] = 1
	 
	elif model=="ZPrimeQ":
	    print "Z' Q"
	    result["dV"] = -1.333
	    result["dA"] = 0.
	    result["uV"] = 2.666
	    result["uA"] = 0.
	    result["eV"] = -4.0
	    result["eA"] = 0
	    result["nuV"] = 0
	    result["nuA"] = 0
	    
	return result
interference = 0 # turns on interference, set to 3 for Z' only and 4 for Z/gamma Drell-Yan
masses = [1000,1500,2000,2500,3000,3500,4000,4500,5000,5500,6000,6500,7000]
massBins = [120,200,400,800,1400,2300,3500,4500,6000,-1]
models = ["ZPrimeQ","ZPrimeSSM","ZPrimePSI","ZPrimeN","ZPrimeSQ","ZPrimeI","ZPrimeEta","ZPrimeChi"]
decays = {"EE":11,"MuMu":13}
for mass in masses:
	for i in range(0,len(massBins)-1):
		for model in models:
			for decay, decayN in decays.iteritems():
				params = setZPrimeParams(model)
				params["mass"] = mass
				params["minMass"] = massBins[i]
				params["maxMass"] = massBins[i+1]
				params["decay"] = decayN
				params["interference"] = interference
				fragment = template%params
				if massBins[i+1] == -1:
					f = open("%sTo%s_ResM%d_M%dToInf_Interference_13TeV-pythia8_cff.py"%(model,decay,mass,massBins[i]),"w")
				else:
					f = open("%sTo%s_ResM%d_M%dTo%d_Interference_13TeV-pythia8_cff.py"%(model,decay,mass,massBins[i],massBins[i+1]),"w")
				f.write(fragment)
				f.close()

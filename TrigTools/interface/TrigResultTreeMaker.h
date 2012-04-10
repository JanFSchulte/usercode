#ifndef SHARPER_TRIGTOOLS_TRIGRESULTTREEMAKER
#define SHARPER_TRIGTOOLS_TRIGRESULTTREEMAKER


//this is a simple class which simulates another trigger based on the already calculated trigger object P4s and filters on that

#include "HLTrigger/HLTcore/interface/HLTFilter.h"
#include "HLTrigger/HLTcore/interface/HLTConfigProvider.h"

#include "FWCore/Common/interface/TriggerNames.h"
#include "DataFormats/Provenance/interface/ParameterSetID.h"

#include "FWCore/Framework/interface/EDAnalyzer.h"
#include "FWCore/Utilities/interface/InputTag.h"

#include "SHarper/TrigTools/interface/TrigToolsStructs.h"

#include "TBits.h"
#include "TTree.h"
#include "TFile.h"


#include <vector>
#include <string>

namespace trigger{
  class TriggerEvent;
}

namespace edm{
  class Event;
  class EventSetup;
  class ParameterSet;
}



class TrigResultTreeMaker : public edm::EDAnalyzer { 

private:
   
  edm::InputTag trigResultsTag_;
  std::vector<std::string> pathNames_;
 
  std::string outputFilename_;
  HLTConfigProvider hltConfig_; //to translate path names to filter names
 
  trigtools::EvtInfoStruct evtInfo_;
  TBits* trigBits_;
  TTree* tree_; //owned by file_
  TFile* file_;


public:
  explicit TrigResultTreeMaker(const edm::ParameterSet& iPara);
  ~TrigResultTreeMaker(){if (file_) delete file_;delete trigBits_;}
private:
  TrigResultTreeMaker(const TrigResultTreeMaker& rhs){}
  TrigResultTreeMaker& operator=(const TrigResultTreeMaker& rhs){return *this;}

 private:
  virtual void beginJob(){}
  virtual void beginRun(const edm::Run& run,const edm::EventSetup& iSetup);
  virtual void analyze(const edm::Event& iEvent, const edm::EventSetup& iSetup);
  virtual void endJob();
  
  

};

#endif

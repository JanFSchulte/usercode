#ifndef SHARPER_SHNTUPLISER_SHEVENTHELPER
#define SHARPER_SHNTUPLISER_SHEVENTHELPER

//class: SHEventHelper
//Description: a class which converts a heep::Event to a SHEvent
//
//Implimentation: 
// 
//Author: Sam Harper

//note: as of 16/09/08, we dont have full functionality, some functions are empty

#include "SHarper/SHNtupliser/interface/SHCaloHit.hh"
#include "SHarper/SHNtupliser/interface/EleMaker.h"


#include "DataFormats/DetId/interface/DetId.h"
#include "DataFormats/EgammaCandidates/interface/GsfElectron.h"

#include <vector>

#include "DataFormats/HLTReco/interface/TriggerFilterObjectWithRefs.h"
#include "DataFormats/HLTReco/interface/TriggerEventWithRefs.h"

namespace heep{
  class Event;
}

class SHEvent;

class SHEventHelper {

private:
  int datasetCode_; //an internal code to my ntuples which only means something to me
  float eventWeight_; //the weight of the event, again only really means something to me
  bool isMC_;// if we are running on mc or not
  int nrGenPartToStore_;
  
  float minEtToPromoteSC_;
  bool addCaloTowers_;
  bool addIsolTrks_;
  bool addMet_;
  bool addJets_;
  bool addTrigs_;
  bool addMuons_;
  bool applyMuonId_;
  bool fillFromGsfEle_;
  bool noFracShowerShape_;

  //temp variables for hlt debug hack
  std::string hltTag_;
  bool useHLTDebug_;
  std::vector<std::string> hltDebugFiltersToSave_;

  EleMaker tracklessEleMaker_;


  //storage for SHCaloHits so we dont have to keep reallocating the memory 
  mutable std::vector<SHCaloHit> ecalHitVec_;
  mutable std::vector<SHCaloHit> hcalHitVec_;
  
  //magic numbers, number of hcal cells (need to fix)
  static const int kNrHcalBarrelCrys_=1296*2;
  static const int kNrHcalEndcapCrys_=1296*2;
  
public:
  explicit SHEventHelper(int datasetCode=0,float eventWeight=1.0);
  
  void setup(const edm::ParameterSet& conf);

  void setupRun(const edm::Run& run,const edm::EventSetup& setup);

  //the two modifiers
  void setDatasetCode(int datasetCode){datasetCode_=datasetCode;}
  void setEventWeight(float weight){eventWeight_=weight;}

  //the main master function which calls all the others
  void makeSHEvent(const heep::Event & heepEvent, SHEvent& shEvent)const;
 
  void addEventPara(const heep::Event& heepEvent, SHEvent& shEvent)const;
  void addElectrons(const heep::Event& heepEvent, SHEvent& shEvent)const;
  void addElectron(const heep::Event& heepEvent,SHEvent& shEvent,const reco::SuperCluster& superClus)const;
  void addElectron(const heep::Event& heepEvent,SHEvent& shEvent,const reco::GsfElectron& gsfEle)const;
  void addElectron(const heep::Event& heepEvent,SHEvent& shEvent,const reco::Photon& photon)const;
  void addSuperClusters(const heep::Event& heepEvent, SHEvent& shEvent)const;
  void addPreShowerClusters(const heep::Event& heepEvent, SHEvent& shEvent)const;
  void addCaloHits(const heep::Event& heepEvent,SHEvent& shEvent)const;
  void addCaloTowers(const heep::Event& heepEvent,SHEvent& shEvent)const;
  void addEcalHits(const heep::Event& heepEvent,SHEvent& shEvent)const;
  void addHcalHits(const heep::Event& heepEvent,SHEvent& shEvent)const;
  void addTrigInfo(const heep::Event& heepEvent,SHEvent& shEvent)const;
  void addTrigInfo(const trigger::TriggerEvent& trigEvt,
		   const edm::TriggerResults& trigResults,
		   const edm::TriggerNames& trigNames,SHEvent& shEvent,const heep::Event* heepEvent=NULL)const; //horrible hack fix this
  void addTrigDebugInfo(const heep::Event& heepEvent,SHEvent& shEvent,const trigger::TriggerEventWithRefs& trigEvt,const std::vector<std::string>& filterNames,const std::string& hltTag)const;
  void addJets(const heep::Event& heepEvent,SHEvent& shEvent)const;
  void addIsolTrks(const heep::Event& heepEvent,SHEvent& shEvent)const;
  // void addIsolClus(const heep::Event& heepEvent,SHEvent& shEvent)const{}
  void addMet(const heep::Event& heepEvent,SHEvent& shEvent)const;
  void addMCParticles(const heep::Event& heepEvent,SHEvent& shEvent)const;
  //void addL1Info(const heep::Event& heepEvent,SHEvent& shEvent)const;
  void addMuons(const heep::Event& heepEvent,SHEvent& shEvent)const;

  size_t matchToEle(const reco::SuperCluster& superClus,const std::vector<reco::GsfElectron> eles)const;
  size_t matchToEle(const reco::SuperCluster& superClus,const std::vector<heep::Ele> eles)const;
  static int getVertexNr(const reco::TrackBase& track,const std::vector<reco::Vertex>& vertices);
  static int getVertexNrClosestZ(const reco::TrackBase& track,const std::vector<reco::Vertex>& vertices);

  static bool passMuonId(const reco::Muon& muon,const heep::Event& heepEvent);

private:
  //the hashing functions for vector positions
  int ecalHitHash_(const DetId detId)const;
  int hcalHitHash_(const DetId detId)const; 
  
  //makes the ecal and hcalHitVec the correct size, puts the correct detId in the correct position and -999.s the energies
  void initEcalHitVec_()const;
  void initHcalHitVec_()const;
  
  static uint32_t getEcalFlagBits_(const EcalRecHit& hit);//because a simple accessor to the bit was too much to ask

};

#endif

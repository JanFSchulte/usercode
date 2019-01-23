
#include "FWCore/Framework/interface/EDAnalyzer.h"
#include "FWCore/Framework/interface/Event.h"
#include "FWCore/Framework/interface/Run.h"
#include "FWCore/ParameterSet/interface/ParameterSet.h"
#include "FWCore/Utilities/interface/InputTag.h"
#include "DataFormats/HepMCCandidate/interface/GenParticle.h"
#include "SimDataFormats/GeneratorProducts/interface/GenEventInfoProduct.h"
#include "SimDataFormats/GeneratorProducts/interface/GenRunInfoProduct.h"
#include "CommonTools/UtilAlgos/interface/TFileService.h"
#include "FWCore/ServiceRegistry/interface/Service.h"
#include "FWCore/Framework/interface/MakerMacros.h"
//#include "DataFormats/PatCandidates/interface/CompositeCandidate.h"
#include "CommonTools/CandUtils/interface/AddFourMomenta.h"
#include "TTree.h"
#include "DataFormats/Candidate/interface/CompositeCandidate.h"
#include "TParameter.h"
#include "TLorentzVector.h"
struct EventId {
  
  int runnr;
  int lumiSec;
  int eventnr;
  int datasetCode;
  EventId():runnr(0),lumiSec(0),eventnr(0),datasetCode(-1){}
  EventId(int iRunnr,int iLumiSec,int iEventnr,int iDataset=-1):runnr(iRunnr),lumiSec(iLumiSec),eventnr(iEventnr),datasetCode(iDataset){}

  static std::string contents(){return "runnr/I:lumiSec:eventnr:datasetCode";}
  
  bool operator<(const EventId& rhs){
    if(datasetCode<rhs.datasetCode) return true;
    else if(datasetCode>rhs.datasetCode) return false;
    else { //same dataset
      if(runnr<rhs.runnr) return true;
      else if(runnr>rhs.runnr) return false;
      else{ //same run
	if(lumiSec<rhs.lumiSec) return true;
	else if(lumiSec>rhs.lumiSec) return false;
	else if(eventnr<rhs.eventnr) return true;
	else return false;
      }
    }
  }

  bool operator==(const EventId& rhs){
    return datasetCode==rhs.datasetCode && runnr==rhs.runnr && lumiSec==rhs.lumiSec && eventnr==rhs.eventnr;
  }

};

struct PDFInfo2{
  float id1,id2;
  float x1,pdf1;
  float x2,pdf2;
  float scale;
  
  PDFInfo2():id1(0),id2(0),x1(0),pdf1(0),x2(0),pdf2(0),scale(0){}
  void clear(){id1=id2=x1=pdf1=x2=pdf2=scale=0.;}
  void fill(const gen::PdfInfo& pdf);
  static std::string contents(){return "id1/F:id2:x1:pdf1:x2:pdf2:scale";}
 
};

void PDFInfo2::fill(const gen::PdfInfo& info)
{
  id1 = info.id.first;
  id2 = info.id.second;
  x1 = info.x.first;
  x2 = info.x.second;
  pdf1 = info.xPDF.first;
  pdf2 = info.xPDF.second;
  scale = info.scalePDF;
}

struct P4Struct {
  float nrgy,et,eta,phi,pt,mass;
  void fill(const math::XYZTLorentzVector& p4){
    //if(p4.Pt()!=0 && p4.Et()!=0){
      nrgy = p4.E();
      et = p4.Et();
      eta = p4.Eta();
      phi = p4.Phi();
      pt =p4.Pt();
      mass = p4.mag();
    //}else clear();
  }
  void clear(){nrgy=-999;et=-999;eta=-999;phi=-0;pt=-999;mass=-999;}
  static std::string contents(){return "nrgy/F:et:eta:phi:pt:mass";}
};

class PDFTreeMakerADD : public edm::EDAnalyzer {

private:

  TTree* tree_;
  std::vector<double> pdfWeights_;
  EventId evtId_;
  P4Struct bosonP4_; // as a sanity check we have the right event...
  P4Struct ele1P4_;
  P4Struct ele2P4_;
  PDFInfo2 pdfInfo_;
  int ele1PID_;
  int ele2PID_;
  int bosonId_;

  edm::InputTag genPartsTag_;
  edm::InputTag genEvtInfoTag_;
  edm::InputTag pdfWeightsTag_;
  int datasetCode_;
  int decayParticlePID_;
  
public:
  explicit PDFTreeMakerADD(const edm::ParameterSet& para);
  ~PDFTreeMakerADD(){}
  
  virtual void beginJob();
  virtual void analyze(const edm::Event& event,const edm::EventSetup& setup);
  virtual void endJob();
  virtual void endRun(edm::Run const& iRun, edm::EventSetup const&);
  
  static const reco::CompositeCandidate* reconstructG(const reco::GenParticleCollection& genParts);
  static const reco::Candidate* getDaughter(const reco::Candidate* part,int pid);
  static const reco::Candidate* getLastDaughter(const reco::Candidate* part,int pid);
  static const reco::Candidate* getBoson( const reco::GenParticleCollection& genParts);
  static bool isBoson(int pid);
};

PDFTreeMakerADD::PDFTreeMakerADD(const edm::ParameterSet& para)

{
  genPartsTag_=para.getParameter<edm::InputTag>("genPartsTag");
  genEvtInfoTag_=para.getParameter<edm::InputTag>("genEvtInfoTag");
  pdfWeightsTag_=para.getParameter<edm::InputTag>("pdfWeightsTag");
  datasetCode_=para.getParameter<int>("datasetCode");
  decayParticlePID_ = para.getParameter<int>("decayParticlePID");
  
}

void PDFTreeMakerADD::beginJob()
{
  edm::Service<TFileService> fs;
  fs->file().cd();
  tree_= new TTree("pdfTree","PDF Tree");
  tree_->Branch("evtId",&evtId_,EventId::contents().c_str());
  tree_->Branch("bosonP4",&bosonP4_,P4Struct::contents().c_str());
  tree_->Branch("decay1P4",&ele1P4_,P4Struct::contents().c_str());
  tree_->Branch("decay2P4",&ele2P4_,P4Struct::contents().c_str());
  tree_->Branch("decay1PID",&ele1PID_,"decay1PID/I");
  tree_->Branch("decay2PID",&ele2PID_,"decay2PID/I");
  tree_->Branch("bosonPID",&bosonId_,"bosonPID/I");
  tree_->Branch("pdfInfo",&pdfInfo_,PDFInfo2::contents().c_str());
  // tree_->Branch("pdfWeights",&pdfWeights_);
}

void PDFTreeMakerADD::analyze(const edm::Event& iEvent,const edm::EventSetup& iSetup)
{ 
  //  edm::Handle<std::vector<double> > pdfWeightsHandle;
  // iEvent.getByLabel(pdfWeightsTag_,pdfWeightsHandle);
  // pdfWeights_ = *pdfWeightsHandle;
  //  std::cout <<"size of weights "<<pdfWeights_.size()<<std::endl;
  evtId_.runnr = iEvent.id().run();
  evtId_.lumiSec = iEvent.luminosityBlock();
  evtId_.eventnr = iEvent.id().event();
  evtId_.datasetCode=datasetCode_;
  
  edm::Handle<reco::GenParticleCollection> genPartsHandle;
  iEvent.getByLabel(genPartsTag_,genPartsHandle);
  const reco::GenParticleCollection& genParts = *genPartsHandle;
  
  edm::Handle<GenEventInfoProduct> genEvtInfo;
  iEvent.getByLabel(genEvtInfoTag_, genEvtInfo);
  if(genEvtInfo.isValid()) pdfInfo_.fill(*genEvtInfo->pdf());
  else pdfInfo_.clear();
  
      


  bosonId_=0;
  bosonP4_.clear();
  ele1P4_.clear();
  ele2P4_.clear();
  ele1PID_=0;
  ele2PID_=0;
 

  const reco::CompositeCandidate* boson = reconstructG(genParts);
  const reco::Candidate* daughter1 = boson->daughter("daughter1");
  const reco::Candidate* daughter2 = boson->daughter("daughter2"); 
  if(boson){
    bosonId_=39;
    //TLorentzVector bosonP4 = new TLorentzVector();
    ROOT::Math::LorentzVector<ROOT::Math::PxPyPzE4D<double> > bosonP4 = daughter1->p4()+daughter2->p4();
    bosonP4_.fill(bosonP4);
  }

  if(daughter1){
    ele1P4_.fill(daughter1->p4());
    ele1PID_=daughter1->pdgId();
  }

  if(daughter2){
    ele2P4_.fill(daughter2->p4());
    ele2PID_=daughter2->pdgId();
  }
  tree_->Fill();  

  

}


const reco::CompositeCandidate* PDFTreeMakerADD::reconstructG(const reco::GenParticleCollection& genParts){

  reco::CompositeCandidate * comp = new reco::CompositeCandidate;
  //const reco::Candidate* p1 = new reco::Candidate;
  //const reco::Candidate* p2 = new reco::Candidate;
  bool found1 = false;
  for (auto &part :genParts){

	if (abs(part.status()) == 23){
	//if (abs(part.status()) == 44 && (abs(part.pdgId()) == 11 || abs(part.pdgId()) == 13 || abs(part.pdgId() == 15))){
		if (!found1){
			found1 = true;
			const reco::Candidate * p1 = &part;
			comp->addDaughter(*p1,"daughter1");
		}
		else {
			//if (!(part.pt() == comp->daughter("daughter1")->pt())){
				const reco::Candidate * p2 = &part;
				comp->addDaughter( *p2,"daughter2");
			//}
		}
	}

  }

  //comp->addDaughter( *p1, "daughter1" );
  //comp->addDaughter( *p2, "daughter2" );
  //AddFourMomenta addP4;
  //addP4.set( comp );	
  return comp;
}

bool PDFTreeMakerADD::isBoson(int pid)

{
  if(pid==23 || abs(pid)==24 || pid==32 || pid==5100039 || pid == 39) return true;
  else return false;
}

const reco::Candidate* PDFTreeMakerADD::getBoson( const reco::GenParticleCollection& genParts)
{
  for(auto &part : genParts){
    if(isBoson(part.pdgId())){
      return getLastDaughter(&part,part.pdgId());
    }
  }
  return nullptr;
}
 
const reco::Candidate* PDFTreeMakerADD::getLastDaughter(const reco::Candidate* part,int pid)
{
  for(size_t partNr =0; part && partNr<part->numberOfDaughters();partNr++){
    if(part->daughter(partNr)->pdgId()==pid) return getLastDaughter(part->daughter(partNr),pid);
  }
  return part;
}
       
const reco::Candidate* PDFTreeMakerADD::getDaughter(const reco::Candidate* part,int pid)
{  
  for(size_t partNr =0; part && partNr<part->numberOfDaughters();partNr++){
    if(part->daughter(partNr)->pdgId()==pid) return part->daughter(partNr);
  }
  return nullptr;
}

   
  


void PDFTreeMakerADD::endJob()
{ 
 
  
}  


void PDFTreeMakerADD::endRun(edm::Run const& iRun, edm::EventSetup const&)
{
  edm::Handle< GenRunInfoProduct > genInfoProduct;
  iRun.getByLabel("generator", genInfoProduct );
  TParameter<float>* crossSec=new TParameter<float>("crossSec",0);
  crossSec->SetVal(genInfoProduct->internalXSec().value());  
  tree_->GetUserInfo()->Add(crossSec);
  
}

DEFINE_FWK_MODULE(PDFTreeMakerADD);

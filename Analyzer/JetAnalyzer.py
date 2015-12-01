
from Core.Analyzer import Analyzer
from Objects.Jet import Jet
from DataFormats.FWLite import Handle
import math

class JetAnalyzer(Analyzer):
    def declareHandles(self):
        self.handlePatJets = Handle("std::vector<pat::Jet>")
        self.handleGenJets = Handle("std::vector<reco::GenJet>")

    def beginJob(self):
        super(JetAnalyzer,self).beginJob()

    def analyze(self,event):
        pass

    def endJob(self):
        super(JetAnalyzer,self).endJob()

    def passJetID(self,wp,jet):
        nhf = jet.neutralHadronEnergyFraction()
        nemf = jet.neutralEmEnergyFraction()
        chf = jet.chargedHadronEnergyFraction()
        muf = jet.muonEnergyFraction()
        cemf = jet.chargedEmEnergyFraction()
        numConst = jet.chargedMultiplicity() + jet.neutralMultiplicity()
        numNeutralParticles = jet.neutralMultiplicity()
        chm = jet.chargedMultiplicity()

        if wp == "LooseJetID_13TeV":
            return ((nhf < 0.99 and nemf < 0.99 and numConst > 1) and ((abs(jet.eta()) <= 2.4 and chf > 0 and chm > 0 and cemf < 0.99) or abs(jet.eta()>2.4) and (abs(jet.eta()) < 3.0)) or (nemf < 0.9 and numNeutralParticles > 10 and abs(jet.eta()) > 3.0))

        if wp == "LooseJetID_8TeV":
            return (nhf < 0.99 and nemf < 0.99 and numConst>1 and muf < 0.8) and ((abs(jet.eta()) <= 2.4 and chf > 0 and chm > 0 and cemf < 0.99) or abs(jet.eta()) > 2.4 )

        return False

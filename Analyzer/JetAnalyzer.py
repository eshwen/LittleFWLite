
from Core.Analyzer import Analyzer
from DataFormats.FWLite import Handle 
import math

class JetAnalyzer(Analyzer):
	def declareHandles(self):
		self.handlePatJets = Handle("std::vector<pat::Jet>")
		self.handleGenJets = Handle("std::vector<reco::GenJet>")
		# self.handlePatEles = Handle("std::vector<pat::Electron>")
		# self.handlePatMuons = Handle("std::vector<pat::Muon>")

	def beginJob(self):
		super(JetAnalyzer,self).beginJob()

	def printPatJetHeader(self):	
		#print "--------------------------------------------------------------------------------------------------------------------------------------------------------------------"
		print "jet variables:"
		print "%6s" % "pt",
		print "%6s" % "eta",
		print "%6s" % "phi",
		print "%15s" % "NeuHadEnergyFrac",
		print "%15s" % "NeuEMEnergyFrac",
		print "%15s" % "ChHadEnergyFrac",
		print "%15s" % "MuEnergyFrac",
		print "%15s" % "ChEMEnergyFrac",
		print "%15s" % "neuEMEnergyFrac",
		print "%5s"  % "ChMulti",
		print "%5s"  % "NeuMulti",
		print "%10s" % "NewJetID",
		print "%10s" % "OldJetID"
		print "--------------------------------------------------------------------------------------------------------------------------------------------------------------------"

	def printGenJetHeader(self):
		print "--------------------------------------------------------------------------------------------------------------------------------------------------------------------"
		print "GenJet variables:"
		print "%6s" % "pt",
		print "%6s" % "eta",
		print "%6s" % "phi"
		print "--------------------------------------------------------------------------------------------------------------------------------------------------------------------"


	def analyze(self,event):
		run = event.eventAuxiliary().run()
		lumi = event.eventAuxiliary().luminosityBlock()
		eventId = event.eventAuxiliary().event()

		print

		print "===================================================================================================================================================================="
		print "%15s"%"Run",
		print "%15s"%"Lumi",
		print "%15s"%"Event"
		print "%15d"%run,
		print "%15d"%lumi,
		print "%15d"%eventId
		print "===================================================================================================================================================================="

		event.getByLabel(("slimmedJets","","PAT"), self.handlePatJets)
		event.getByLabel(("slimmedGenJets","","PAT"),self.handleGenJets)
		#event.getByLabel(("slimmedElectrons","","PAT"),self.handlePatEles)
		#event.getByLabel(("slimmedMuons","","PAT"),self.handlePatMuons)
		
		pfJets = self.handlePatJets.product()
		self.printPatJetHeader()
		for i,jet in enumerate(pfJets):
			print "%6.1f" % jet.pt(),
			print "%6.1f" % jet.eta(),
			print "%6.1F" % jet.phi(),
			print "%15.1f" % jet.neutralHadronEnergyFraction(),
			print "%15.1f" % jet.neutralEmEnergyFraction(),
			print "%15.1f" % jet.chargedHadronEnergyFraction(),
			print "%15.1f" % jet.muonEnergyFraction(),
			print "%15.1f" % jet.chargedEmEnergyFraction(),
			print "%15.1f" % jet.neutralHadronEnergyFraction(),
			print "%5.1f" % jet.chargedMultiplicity(),
			print "%5.1f" % jet.neutralMultiplicity(),

			print "%10.1f" % self.passJetID("LooseJetID_13TeV",jet),
			print "%10.1f" % self.passJetID("LooseJetID_8TeV",jet)

		self.printGenJetHeader()	
		genJets = self.handleGenJets.product()
		for i,genJet in enumerate(genJets):
			print "%6.1f" % genJet.pt(),
			print "%6.1f" % genJet.eta(),
			print "%6.1F" % genJet.phi()
		
		# print len(self.handlePatMuons.product())
		# print len(self.handlePatEles.product())
				

	
	def endJob(self):
		pass

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

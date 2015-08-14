
from Core import *
import math

class JetAnalyzer(EventLooper):
	def declareHandles(self):
		self.handlePatJets = Handle("std::vector<pat::Jet>")

	def beginJob(self):
		pass

	def printJetHeader(self):	
		print "===================================================================================================================================================================="
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
		print "===================================================================================================================================================================="

	def analyze(self,event):
		run = event.eventAuxiliary().run()
		lumi = event.eventAuxiliary().luminosityBlock()
		eventId = event.eventAuxiliary().event()

		event.getByLabel(("slimmedJets","","PAT"), self.handlePatJets)
		pfJets = self.handlePatJets.product()
		self.printJetHeader()
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
			print "%5.f" % jet.neutralMultiplicity(),

			print "%10.1f" % self.passJetID("LooseJetID_13TeV",jet),
			print "%10.1f" % self.passJetID("LooseJetID_8TeV",jet)

				

	
	def endJob(self):
		pass

	def applySelection(self,event):
		run = event.eventAuxiliary().run()
		lumi = event.eventAuxiliary().luminosityBlock()
		eventId = event.eventAuxiliary().event()

		return (run == self.selectRun) and (lumi == self.selectLumi) and (eventId == self.selectEvent) 

	def whichEvent(self,selectRun,selectLumi,selectEvent):
		self.selectRun = selectRun
		self.selectLumi = selectLumi
		self.selectEvent = selectEvent
	
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

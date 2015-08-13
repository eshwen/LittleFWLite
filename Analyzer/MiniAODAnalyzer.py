
from Core import *

class MiniAODAnalyzer(EventLooper):
	def declareHandles(self):
		self.handlePatMETs = Handle("std::vector<pat::MET>")
		self.handlePFCans = Handle("std::vector<pat::PackedCandidate>")
		self.handlePatJets = Handle("std::vector<pat::Jet>")

	def beginJob(self):
		self.metVec = ROOT.TLorentzVector()
		self.mhtVec = ROOT.TLorentzVector()

	def analyze(self,event):
		run = event.eventAuxiliary().run()
		lumi = event.eventAuxiliary().luminosityBlock()
		eventId = event.eventAuxiliary().event()
		
		event.getByLabel(("packedPFCandidates","","PAT"), self.handlePFCans)
		pfCans = self.handlePFCans.product()
		for pfCan in pfCans:
			tmpVec = ROOT.TLorentzVector()
			tmpVec.SetPtEtaPhiM(pfCan.pt(),pfCan.eta(),pfCan.phi(),pfCan.mass())
			self.metVec += tmpVec

		event.getByLabel(("slimmedJets","","PAT"), self.handlePatJets)
		pfJets = self.handlePatJets.product()
		for jet in pfJets:
			if jet.pt() < 40.: continue
			tempVec = ROOT.TLorentzVector()
			tempVec.SetPtEtaPhiM(jet.pt(),jet.eta(),jet.phi(),jet.mass())
			self.mhtVec += tempVec	
	
	def endJob(self):
		print " mht.pt ",self.mhtVec.Pt(),
		print " mht.phi ",self.mhtVec.Phi()
		print " met.pt ",self.metVec.Pt(),
		print " met.phi ",self.metVec.Phi()


	def applySelection(self,event):
		run = event.eventAuxiliary().run()
		lumi = event.eventAuxiliary().luminosityBlock()
		eventId = event.eventAuxiliary().event()

		return (run == self.selectRun) and (lumi == self.selectLumi) and (eventId == self.selectEvent) 

	def whichEvent(self,selectRun,selectLumi,selectEvent):
		self.selectRun = selectRun
		self.selectLumi = selectLumi
		self.selectEvent = selectEvent
		

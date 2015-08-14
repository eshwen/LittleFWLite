
from Core import *
import math

class METAnalyzer(EventLooper):
	def declareHandles(self):
		self.handlePatMETs = Handle("std::vector<pat::MET>")
		self.handlePFCans = Handle("std::vector<pat::PackedCandidate>")
		self.handlePatJets = Handle("std::vector<pat::Jet>")

	def beginJob(self):
		self.metVec = ROOT.TLorentzVector()
		self.mhtVec = ROOT.TLorentzVector()
		self.mht40Vec = ROOT.TLorentzVector()
		self.rawMetVec = ROOT.TLorentzVector()
		self.patMetVec = ROOT.TLorentzVector()

	def analyze(self,event):
		run = event.eventAuxiliary().run()
		lumi = event.eventAuxiliary().luminosityBlock()
		eventId = event.eventAuxiliary().event()
		
		event.getByLabel(("packedPFCandidates","","PAT"), self.handlePFCans)
		pfCans = self.handlePFCans.product()
		for pfCan in pfCans:
			tmpVec = ROOT.TLorentzVector()
			tmpVec.SetPtEtaPhiM(pfCan.pt(),pfCan.eta(),pfCan.phi(),pfCan.mass())
			self.metVec -= tmpVec

		event.getByLabel(("slimmedJets","","PAT"), self.handlePatJets)
		pfJets = self.handlePatJets.product()
		# print "jet variables:"
		# print "========================================="
		for i,jet in enumerate(pfJets):
			#if jet.pt() < 40.: continue
			#print "pt: %3.1f ; eta: %3.1f ; phi: %3.1f "%(jet.pt(),jet.eta(),jet.phi())
			tempVec = ROOT.TLorentzVector()
			tempVec.SetPtEtaPhiM(jet.pt(),jet.eta(),jet.phi(),jet.mass())
			self.mhtVec -= tempVec
			if jet.pt() < 40.: continue
			self.mht40Vec -= tempVec
		print "========================================="

		event.getByLabel(("slimmedMETs","","PAT"),self.handlePatMETs)
		slimmedMET = self.handlePatMETs.product().front()
		self.rawMetVec.SetPtEtaPhiM(slimmedMET.shiftedPt(12,0),0,slimmedMET.shiftedPhi(12,0),0)
		self.patMetVec.SetPtEtaPhiM(slimmedMET.pt(),slimmedMET.eta(),slimmedMET.phi(),slimmedMET.mass())

	
	def endJob(self):
		print "MHT calculated from SlimmedJets: pt: %3.1f ; phi: %3.1f "%(self.mhtVec.Pt(),self.mhtVec.Phi())
		print "MHT calculated from SlimmedJets with pt above 40 GeV: pt: %3.1f ; phi: %3.1f "%(self.mht40Vec.Pt(),self.mht40Vec.Phi())
		print "MET calculated from packed PF Candidates: pt: %3.1f ; phi: %3.1f "%(self.metVec.Pt(),self.metVec.Phi())
		print "PATMET in MiniAOD: pt: %3.1f ; phi: %3.1f "%(self.patMetVec.Pt(),self.patMetVec.Phi())
		print "RawMET in MiniAOD: pt: %3.1f ; phi: %3.1f "%(self.rawMetVec.Pt(),self.rawMetVec.Phi())


	def applySelection(self,event):
		run = event.eventAuxiliary().run()
		lumi = event.eventAuxiliary().luminosityBlock()
		eventId = event.eventAuxiliary().event()

		return (run == self.selectRun) and (lumi == self.selectLumi) and (eventId == self.selectEvent) 

	def whichEvent(self,selectRun,selectLumi,selectEvent):
		self.selectRun = selectRun
		self.selectLumi = selectLumi
		self.selectEvent = selectEvent
		

#!/usr/bin/env python
import ROOT
from DataFormats.FWLite import Events, Handle

class EventPicker(object):
	def __init__(self,sequence,inputPath=None):
		self.sequence = sequence		
		if inputPath:
			self.file = ROOT.TFile.Open(inputPath)

	def loadFiles(self,inputPath):
		self.file = ROOT.TFile.Open(inputPath)
	
	def whichEvent(self,selectRun,selectLumi,selectEvent):
		self.selectRun = selectRun
		self.selectLumi = selectLumi
		self.selectEvent = selectEvent

	def loop(self,nEvents = -1):
		if not hasattr(self,"selectRun") or not hasattr(self,"selectLumi") or not hasattr(self,"selectEvent"):
			raise RuntimeError,"Run Number or Lumi Section or Event number not specified."
		self.events = Events(self.file,maxEvents=nEvents)
		for ana in self.sequence:
			ana.beginJob()
		for i,event in enumerate(self.events):
			if (i > nEvents) and (nEvents != -1): break
			if not self.isSelectEvent(event): continue
			for ana in self.sequence:
				if not  ana.applySelection(event): continue
				ana.analyze(event)
		for ana in self.sequence:
			ana.endJob()

	def isSelectEvent(self,event):
		run = event.eventAuxiliary().run()
		lumi = event.eventAuxiliary().luminosityBlock()
		eventId = event.eventAuxiliary().event()

		return (run == self.selectRun) and (lumi == self.selectLumi) and (eventId == self.selectEvent) 

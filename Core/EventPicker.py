#!/usr/bin/env python
import ROOT
from DataFormats.FWLite import Events, Handle

class EventPicker(object):
	def __init__(self,sequence,inputPath=None):
		self.sequence = sequence		
		if inputPath:
			self.inputPath = inputPath
		self.eventList = []

	def addEventList(self,selectRun,selectLumi,selectEvent):
		self.eventList.append((selectRun,selectLumi,selectEvent))

	def loop(self,nEvents = -1):
		if not hasattr(self,"selectRun") or not hasattr(self,"selectLumi") or not hasattr(self,"selectEvent"):
			raise RuntimeError,"Run Number or Lumi Section or Event number not specified."
		if type(self.inputPath) != list:
			self.inputPath = [self.inputPath]
		for filePath in self.inputPath:
			file = ROOT.TFile.Open(filePath)
			self.events = Events(file,maxEvents=nEvents)
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
		
		return ((run,lumi,eventId) in self.eventList)

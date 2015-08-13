#!/usr/bin/env python
import ROOT
from LoadLibraries import *

class EventLooper(object):
	def __init__(self):
		# self.inputPath = [inputPath]
		# self.nEvent
		pass

	def loadFiles(self,inputPath):
		self.file = ROOT.TFile.Open(inputPath)

	def declareHandles(self):
		pass

	def loop(self,nEvents = -1):
		self.events = Events(self.file,maxEvents=nEvents)
		self.declareHandles()
		self.beginJob()
		for i,event in enumerate(self.events):
			if (i > nEvents) and (nEvents != -1): break
			if not  self.applySelection(event): continue
			self.analyze(event)
		self.endJob()

	def analyze(self,event):
		pass

	def applySelection(self,event):
		pass

	def beginJob(self):
		pass

	def endJob(self):
		pass
	

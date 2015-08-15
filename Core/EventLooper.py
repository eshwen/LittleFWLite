#!/usr/bin/env python
import ROOT
from LoadLibraries import *

class EventLooper(object):
	def __init__(self,sequence,inputPath=None):
		self.sequence = sequence		
		if inputPath:
			self.file = ROOT.TFile.Open(inputPath)

	def loadFiles(self,inputPath):
		self.file = ROOT.TFile.Open(inputPath)

	def loop(self,nEvents = -1):
		self.events = Events(self.file,maxEvents=nEvents)
		for ana in self.sequence:
			ana.beginJob()
		for i,event in enumerate(self.events):
			if (i > nEvents) and (nEvents != -1): break
			for ana in self.sequence:
				if not  ana.applySelection(event): continue
				ana.analyze(event)
		for ana in self.sequence:
			ana.endJob()
	

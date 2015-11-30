#!/usr/bin/env python
import ROOT
from DataFormats.FWLite import Events, Handle,ChainEvent

class EventLooper(object):
	def __init__(self,sequence,inputPath=None):
		self.sequence = sequence		
		if inputPath:
            if type(inputPath) != list:
                self.inputPath = [ inputPath ]
        else:
            inputPath = []
        self.inputPath = inputPath

    def loadEvents(self,nEvents = -1):
        self.events = ChainEvent( self.inputPath )

	def loop(self,nEvents = -1):
		self.loadEvents(nEvents)
        for ana in self.sequence:
			ana.beginJob()
		for i,event in enumerate(self.events):
			if (i > nEvents) and (nEvents != -1): break
			for ana in self.sequence:
				if not  ana.applySelection(event): continue
				ana.analyze(event)
		for ana in self.sequence:
			ana.endJob()
	

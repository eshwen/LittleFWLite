
import ROOT
from DataFormats.FWLite import Events, Handle

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
        self.events = Events( self.inputPath )

    def loop(self,nEvents = -1):
        self.loadEvents(nEvents)
        print "Total Number of events to be run: %s"%len(self.events)
        for ana in self.sequence:
            ana.beginJob()
        for i,event in enumerate(self.events):
            if i % 10000 == 0: print "Processed events: %s"%i
            if (i > nEvents) and (nEvents != -1): break
            for ana in self.sequence:
                if not  ana.applySelection(event): continue
                ana.analyze(event)
        for ana in self.sequence:
            ana.endJob()


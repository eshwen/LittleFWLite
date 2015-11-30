#!/usr/bin/env python
import ROOT
from DataFormats.FWLite import Events

class EventPicker(object):
    def __init__(self,sequence,inputPath=None):
        self.sequence = sequence		
        if inputPath:
            self.inputPath = inputPath
        self.eventList = []

    def addEventList(self,selectRun,selectLumi,selectEvent):
        self.eventList.append((selectRun,selectLumi,selectEvent))

    def loop(self,nEvents = -1):
        if not self.eventList:
            raise RuntimeError,"Run Number or Lumi Section or Event number not specified."
        if type(self.inputPath) != list:
            self.inputPath = [self.inputPath]
        for filePath in self.inputPath:
            file = ROOT.TFile.Open(filePath)
            if self.printProcess:
                print "Processing file: %s"%filePath
            # print filePath
            events = Events(file,maxEvents=nEvents)
            for ana in self.sequence:
                ana.beginJob()
            for i,event in enumerate(events):
                if self.printProcess and i % 10000 == 0:
                    print "%s events processed"%i
                if (i > nEvents) and (nEvents > 0): break
                if not self.isSelectEvent(event): continue
                for ana in self.sequence:
                    if not ana.applySelection(event): continue
                    ana.analyze(event)
            for ana in self.sequence:
                ana.endJob()
            file.Close()


    def isSelectEvent(self,event):
        run = event.eventAuxiliary().run()
        lumi = event.eventAuxiliary().luminosityBlock()
        eventId = event.eventAuxiliary().event()

        return any([run == evtList[0] and lumi == evtList[1] and eventId == evtList[2] for evtList in self.eventList]) 
    # return any([run == evtList[0] and lumi == evtList[1] and eventId == evtList[2] for evtList in self.eventList]) 



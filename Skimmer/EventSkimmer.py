
from Core.Analyzer import Analyzer
from Utils.TextFileHandler import ReadEventList 

class EventSkimmer(Analyzer):
    def beginJob(self):

        if not hasattr(self,"textFilePath"):
            raise RuntimeError,"No text file path provided for event skimmer"
        
        self.eventList = ReadEventList(self.textFilePath)

    def applySelection(self,event):
        run = event.eventAuxiliary().run()
        lumi = event.eventAuxiliary().luminosityBlock()
        eventId = event.eventAuxiliary().event()

        return any([run == evtList[0] and lumi == evtList[1] and eventId == evtList[2] for evtList in self.eventList]) 


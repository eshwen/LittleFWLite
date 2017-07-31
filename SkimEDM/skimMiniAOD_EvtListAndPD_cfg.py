
from Utils.TextFileHandler import ReadEventList
from Utils.DBHandler import getDBPath, getFilesFromPD

import FWCore.ParameterSet.Config as cms
import FWCore.ParameterSet.VarParsing as VarParsing

#____________________________________________________________________________||

options = VarParsing.VarParsing()

#____________________________________________________________________________||

options.register('dataset',
                 "/HTMHT/Run2016B-03Feb2017_ver2-v2/MINIAOD",
                 VarParsing.VarParsing.multiplicity.singleton,
                 VarParsing.VarParsing.varType.string,
                 "Primary dataset")

options.register('textFilePath',
                 "/home/hep/ebhal/EventDisplay_MHT/2017_07_24_REV_1/HTMHT_Run2016B_03Feb2017_v2_DCSONLY_MHTtails.txt", #default value: "test.txt"
                 VarParsing.VarParsing.multiplicity.singleton,
                 VarParsing.VarParsing.varType.string,
                 "Text file for event list")

options.register('allFiles',
                True,
                VarParsing.VarParsing.multiplicity.singleton,
                VarParsing.VarParsing.varType.bool,
                "use all files from a PD")

options.register('outFile',
                "file:skimHTMHT_Run2016B.root",
                VarParsing.VarParsing.multiplicity.singleton,
                VarParsing.VarParsing.varType.string,
                "output file path")


#____________________________________________________________________________||

options.parseArguments()

#____________________________________________________________________________||

eventList = ReadEventList(options.textFilePath)
inputEvtList = [ ":".join(event) for event in eventList ]
print inputEvtList

#____________________________________________________________________________||

if options.allFiles:
    fileList = getFilesFromPD(options.dataset) 
else:
    fileList = [ getDBPath(options.dataset,run,lumi) for (run,lumi,evt) in eventList ]

#____________________________________________________________________________||

process = cms.Process('SKIM')

#____________________________________________________________________________||

process.source = cms.Source("PoolSource")

#____________________________________________________________________________||

inputFileNames = cms.untracked.vstring()
inputFileNames.extend( fileList )
print inputFileNames
process.source.fileNames = inputFileNames

#____________________________________________________________________________||

process.source.eventsToProcess = cms.untracked.VEventRange(*inputEvtList)

#____________________________________________________________________________||

process.load('Configuration.StandardSequences.Services_cff')
process.load('FWCore.MessageService.MessageLogger_cfi')
process.load('Configuration.EventContent.EventContent_cff')
process.load('Configuration.StandardSequences.EndOfProcess_cff')

#____________________________________________________________________________||

process.out = cms.OutputModule("PoolOutputModule", fileName = cms.untracked.string(options.outFile) )

#____________________________________________________________________________||

process.p = cms.Path()
process.e = cms.EndPath(process.out)

#____________________________________________________________________________||

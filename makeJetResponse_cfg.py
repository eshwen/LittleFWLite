#!/usr/bin/env python
import sys
from Analyzer.JetAnalyzer import JetAnalyzer

#____________________________________________________________________________||

parser.add_option("-p","--dataset", action = "store", default = 1, type = 'string',help="Primary Dataset")
parser.add_option("-t","--textPath", action = "store", default = "file.txt", type = 'string',help="Event List Text File")

#____________________________________________________________________________||

(options,args) = parser.parse_args(sys.argv)

datasetName = options.dataset
textPath = options.textPath
nevents = options.nevents

#____________________________________________________________________________||

eventList = ReadEventList( textPath )
inputFileList = [ getDBPath( datasetName , run , lumi )  for [run,lumi,event] in eventList ]

#____________________________________________________________________________||

jetAna = JetAnalyzer()

sequence = Sequence()
sequence.load(jetAna)

looper = EventLooper(sequence,inputFileList)
looper.loop(nevents)

#____________________________________________________________________________||

#!/usr/bin/env python
import sys
from LittleFWLite_cfi import *
from Analyzer.JetResponse import JetResponse

#____________________________________________________________________________||

parser.add_option("-p","--dataset", action = "store", type = 'string',help="Primary Dataset")
parser.add_option("-t","--textPath", action = "store", type = 'string',help="Event List Text File")

#____________________________________________________________________________||

(options,args) = parser.parse_args(sys.argv)

datasetName = options.dataset
textPath = options.textPath
nevents = options.nevents
inputPath = options.inputPath

#____________________________________________________________________________||

if inputPath:
    inputFileList = [ '/vols/cms04/lucienlo/output/01_12_2015/SkimMiniAOD/QCD500To700_skim.root' ]
elif textPath and datasetName:
    eventList = ReadEventList( textPath )
    inputFileList = [ getDBPath( datasetName , run , lumi )  for (run,lumi,event) in eventList ]
else:
    raise RuntimeError,"Input files not correctly specifed"


#____________________________________________________________________________||

jetAna = JetResponse()

sequence = Sequence()
sequence.load(jetAna)

looper = EventLooper(sequence,inputFileList)
looper.loop(nevents)

#____________________________________________________________________________||

#!/usr/bin/env python
import sys
from LittleFWLite_cfi import *
from Analyzer.JetResponse import JetResponse

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
#inputFileList = [ getDBPath( datasetName , run , lumi )  for (run,lumi,event) in eventList ]

inputFileList = [ 'root://gfe02.grid.hep.ph.ic.ac.uk/pnfs/hep.ph.ic.ac.uk/data/cms/store/mc/RunIISpring15DR74/QCD_HT500to700_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/MINIAODSIM/Asympt25ns_MCRUN2_74_V9-v1/00000/32ACD783-A818-E511-80D1-000F530E4798.root' ]

#____________________________________________________________________________||

jetAna = JetResponse()

sequence = Sequence()
sequence.load(jetAna)

looper = EventLooper(sequence,inputFileList)
looper.loop(nevents)

#____________________________________________________________________________||

#!/usr/bin/env python
from Core.Sequence import Sequence
from Core.EventPicker import EventPicker
from Core.InputParser import parser
import sys
from Analyzer.JetAnalyzer import JetAnalyzer
from Utils.DBHandler import getDBPath

parser.add_option("-r","--run", action = "store", default = 1, type = 'long',help ="run number")
parser.add_option("-l","--lumi", action = "store", default = 1, type = 'long',help="lumi section")
parser.add_option("-e","--evt", action = "store", default = 1, type = 'long',help="event number")
parser.add_option("-p","--dataset", action = "store", default = 1, type = 'string',help="Primary Dataset")

(options,args) = parser.parse_args(sys.argv)

run = options.run
ls = options.lumi
evt = options.evt
datasetName = options.dataset

inputFilePath = getDBPath(datasetName,run,ls)

jetAna = JetAnalyzer()

sequence = Sequence()
sequence.load(jetAna)

looper = EventPicker(sequence,inputFilePath)
looper.whichEvent(run,ls,evt)
looper.loop()

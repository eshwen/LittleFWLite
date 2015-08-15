#!/usr/bin/env python
from Core import *
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
jetAna.loadFiles(inputFilePath)
jetAna.whichEvent(run,ls,evt)
jetAna.loop()

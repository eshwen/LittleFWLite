#!/usr/bin/env python
from Core import *
from Analyzer.METAnalyzer import METAnalyzer
from Analyzer.JetAnalyzer import JetAnalyzer
import ROOT
from Utils.DBHandler import getDBPath

ROOT.gROOT.SetBatch(1)
ROOT.gROOT.ProcessLine( "gErrorIgnoreLevel = 1001;")

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

metAna = METAnalyzer()
metAna.loadFiles(inputFilePath)
metAna.whichEvent(run,ls,evt)
#metAna.loop()

jetAna = JetAnalyzer()
jetAna.loadFiles(inputFilePath)
jetAna.whichEvent(run,ls,evt)
jetAna.loop()

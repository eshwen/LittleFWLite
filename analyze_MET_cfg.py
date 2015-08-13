#!/usr/bin/env python
from Core import *
from Analyzer.MiniAODAnalyzer import MiniAODAnalyzer
import ROOT

ROOT.gROOT.SetBatch(1)
ROOT.gROOT.ProcessLine( "gErrorIgnoreLevel = 1001;")

inputPath = options.inputPath

analyzer = MiniAODAnalyzer()
analyzer.loadFiles(inputPath)
analyzer.whichEvent(1,2433,319961)
analyzer.loop()

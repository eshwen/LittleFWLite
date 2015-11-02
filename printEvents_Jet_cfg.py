#!/usr/bin/env python
from Core.Sequence import Sequence
from Core.EventLooper import EventLooper
from Core.InputParser import parser
import sys
from Analyzer.JetAnalyzer import JetAnalyzer

(options,args) = parser.parse_args(sys.argv)

inputFilePath = options.inputPath
nevents = options.nevents

jetAna = JetAnalyzer()

sequence = Sequence()
sequence.load(jetAna)

looper = EventLooper(sequence,inputFilePath)
looper.loop(nevents)

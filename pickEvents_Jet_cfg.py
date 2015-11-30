#!/usr/bin/env python
from Core.Sequence import Sequence
from Core.EventPicker import EventPicker
from Core.InputParser import parser
import sys
from Analyzer.JetAnalyzer import JetAnalyzer
from Utils.DBHandler import getFilesFromPD
from Utils.TextFileHandler import ReadEventList

parser.add_option("-p","--dataset", action = "store", default = 1, type = 'string',help="Primary Dataset")
parser.add_option("-t","--textPath", action = "store", default = "file.txt", type = 'string',help="Event List Text File")
parser.add_option("--printProcess", action = "store_true",default = False)

(options,args) = parser.parse_args(sys.argv)

datasetName = options.dataset
textPath = options.textPath
printProcess = options.printProcess

inputFilePath = getFilesFromPD(datasetName)
eventList = ReadEventList(textPath) 

jetAna = JetAnalyzer()

sequence = Sequence()
sequence.load(jetAna)

looper = EventPicker(sequence,inputFilePath)
EventPicker.printProcess = printProcess
looper.eventList = eventList
looper.loop()

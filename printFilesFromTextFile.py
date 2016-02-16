#!/usr/bin/env python
from Utils.DBHandler import getDBPath
from Utils.TextFileHandler import ReadEventList
from Core.InputParser import parser
import sys

parser.add_option("-p","--dataset", action = "store", default = 1, type = 'string',help="Primary Dataset")
parser.add_option("-t","--textFile", action = "store", default = None , type = 'string', help="input text file")

(options,args) = parser.parse_args(sys.argv)

datasetName = options.dataset
textFileName = options.textFile

eventList = ReadEventList(textFileName)

fileList = []
for run,lumi,evt in eventList:
	fileName = getDBPath(datasetName,run,lumi)
	if fileName not in fileList:
		fileList.append( fileName )

print fileList


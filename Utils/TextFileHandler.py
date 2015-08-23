

def ReadEventList(textFilePath):
	file = open(textFilePath,"r")
	file.readline()
	eventList = []
	for line in file:
		if not line: continue
		if line[0] == "#": continue

		run = int(line.split()[0])
		lumi = int(line.split()[1])
		evt = int(line.split()[2])
		
		eventList.append((run,lumi,evt))

	return eventList

	

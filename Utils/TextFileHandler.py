

def ReadEventList(textFilePath):
    file = open(textFilePath,"r")
    eventList = []
    for line in file:
        if not line: continue
        if line[0] == "#": continue
        run = line.split()[0]
        lumi = line.split()[1]
        evt = line.split()[2]
        eventList.append( (run,lumi,evt) )
    file.close()

    return eventList




import subprocess as sp
from whereAmI import whereAmI 

def getDBPath(PDName,run,lumi,runAAA=True):
	cmdList = ["das_client.py","--query","file dataset=%s run=%s lumi=%s"%(PDName,run,lumi),"--limit","0"]
	process = sp.Popen(cmdList,stdout=sp.PIPE)
	
	if runAAA:
		return "root://cms-xrd-global.cern.ch/"+process.communicate()[0].split("\n")[0]
	else:
		if whereAmI() == "Imperial":
			return "root://gfe02.grid.hep.ph.ic.ac.uk/pnfs/hep.ph.ic.ac.uk/data/cms"+process.communicate()[0].split("\n")[0]
		elif whereAmI() == "CERN":
			return "root://eoscms//eos/cms"+process.communicate()[0].split("\n")[0]
		else:
			raise RuntimeError, "getDBPath function only supports IC and CERN for the moment."

def getFilesFromPD(PDName,runAAA=True):
	cmdList = ["das_client.py","--query","file dataset=%s"%(PDName),"--limit","0"]
	process = sp.Popen(cmdList,stdout=sp.PIPE)
	
	if runAAA:
		return ["root://cms-xrd-global.cern.ch/"+fileName for fileName in process.communicate()[0].split("\n") if fileName.endswith(".root")]
	else:
		if whereAmI() == "Imperial":
			return ["root://gfe02.grid.hep.ph.ic.ac.uk/pnfs/hep.ph.ic.ac.uk/data/cms"+fileName for fileName in process.communicate()[0].split("\n") if fileName.endswith(".root")]
		elif whereAmI() == "CERN":
			return ["root://eoscms//eos/cms"+fileName for fileName in process.communicate()[0].split("\n") if fileName.endswith(".root")]
		else:
			raise RuntimeError, "getFilesFromPD function only supports IC for the moment."



import subprocess as sp
from whereAmI import whereAmI 

def getDBPath(PDName,run,lumi):
	cmdList = ["das_client.py","--query","file dataset=%s run=%s lumi=%s"%(PDName,run,lumi),"--limit","0"]
	process = sp.Popen(cmdList,stdout=sp.PIPE)

	if whereAmI() == "Imperial":
		return "root://gfe02.grid.hep.ph.ic.ac.uk/pnfs/hep.ph.ic.ac.uk/data/cms"+process.communicate()[0].split("\n")[0]
	else:
		raise RuntimeError, "getDBPath function only supports IC for the moment."

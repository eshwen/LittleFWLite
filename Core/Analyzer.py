
class Analyzer(object):
	def __init__(self):
        self.hists = {}
		pass

	def beginJob(self):
		self.declareHandles()
		pass

	def declareHandles(self):
		pass

	def analyze(self,event):
		pass

	def endJob(self):
        
        for histName,hist in self.hists.iteritems():
            hist.write()

		pass

	def applySelection(self,event):
		return True

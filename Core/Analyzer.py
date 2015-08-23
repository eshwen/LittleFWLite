
class Analyzer(object):
	def __init__(self):
		pass

	def beginJob(self):
		self.declareHandles()
		pass

	def declareHandles(self):
		pass

	def analyze(self,event):
		pass

	def endJob(self):
		pass

	def applySelection(self,event):
		return True

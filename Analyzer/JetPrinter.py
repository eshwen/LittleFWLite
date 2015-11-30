
from Analyzer.JetAnalyzer import JetAnalyzer
from DataFormats.FWLite import Handle 
import math

class JetPrinter(JetAnalyzer):
	def beginJob(self):
		super(JetPrinter,self).beginJob()

    def printPatJetHeader(self):	
		#print "--------------------------------------------------------------------------------------------------------------------------------------------------------------------"
		print "jet variables:"
		print "%6s" % "pt",
		print "%6s" % "eta",
		print "%6s" % "phi",
		print "%15s" % "NeuHadEnergyFrac",
		print "%15s" % "NeuEMEnergyFrac",
		print "%15s" % "ChHadEnergyFrac",
		print "%15s" % "MuEnergyFrac",
		print "%15s" % "ChEMEnergyFrac",
		print "%15s" % "neuEMEnergyFrac",
		print "%5s"  % "ChMulti",
		print "%5s"  % "NeuMulti",
		print "%10s" % "NewJetID",
		print "%10s" % "OldJetID"
		print "--------------------------------------------------------------------------------------------------------------------------------------------------------------------"

	def printGenJetHeader(self):
		print "--------------------------------------------------------------------------------------------------------------------------------------------------------------------"
		print "GenJet variables:"
		print "%6s" % "pt",
		print "%6s" % "eta",
		print "%6s" % "phi"
		print "--------------------------------------------------------------------------------------------------------------------------------------------------------------------"


	def analyze(self,event):
        
        super(JetPrinter,self).analyze( event )

		print

		print "===================================================================================================================================================================="
		print "%15s"%"Run",
		print "%15s"%"Lumi",
		print "%15s"%"Event"
		print "%15d"%run,
		print "%15d"%lumi,
		print "%15d"%eventId
		print "===================================================================================================================================================================="

		self.printPatJetHeader()
		for i,jet in enumerate(pfJets):
			print "%6.1f" % jet.pt(),
			print "%6.1f" % jet.eta(),
			print "%6.1F" % jet.phi(),
			print "%15.1f" % jet.neutralHadronEnergyFraction(),
			print "%15.1f" % jet.neutralEmEnergyFraction(),
			print "%15.1f" % jet.chargedHadronEnergyFraction(),
			print "%15.1f" % jet.muonEnergyFraction(),
			print "%15.1f" % jet.chargedEmEnergyFraction(),
			print "%15.1f" % jet.neutralHadronEnergyFraction(),
			print "%5.1f" % jet.chargedMultiplicity(),
			print "%5.1f" % jet.neutralMultiplicity(),

			print "%10.1f" % self.passJetID("LooseJetID_13TeV",jet),
			print "%10.1f" % self.passJetID("LooseJetID_8TeV",jet)

		self.printGenJetHeader()	
		for i,genJet in enumerate(genJets):
			print "%6.1f" % genJet.pt(),
			print "%6.1f" % genJet.eta(),
			print "%6.1F" % genJet.phi()
		
	
	def endJob(self):
		pass

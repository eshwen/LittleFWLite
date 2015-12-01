
from Analyzer.JetAnalyzer import JetAnalyzer
from DataFormats.FWLite import Handle 
import math
import ROOT
from Utils.MatchCollections import matchObjectCollection

class JetResponse(JetAnalyzer):
    def beginJob(self):
        super(JetResponse,self).beginJob()

        #____________________________________________________________________________||

        if not hasattr(self,"outFilePath"):
            outFilePath = "jetResponse.root"

        self.outFile = ROOT.TFile(outFilePath,"RECREATE")
        self.hists["jetResponse"] = ROOT.TH1D("JetResponse"," ; Jet Response ;  ",50,0.5,2.)
        self.hists["recoJetPt_vs_genJetPt"] = ROOT.TH2D("recoJetPt_vs_genJetPt"," ; RECO Jet p_{T} ; GEN Jet p_{T}  ",50,0.,100.,50,0.,100.)

        #____________________________________________________________________________||

    def analyze(self,event):

        #____________________________________________________________________________||

        super(JetResponse,self).analyze( event )

        event.getByLabel(("slimmedJets","","PAT"), self.handlePatJets)
        event.getByLabel(("slimmedGenJets","","PAT"), self.handleGenJets)
        
        pfJets = [ jet for jet in self.handlePatJets.product() ]
        genJets = [ genJet for genJet in self.handleGenJets.product() ]
        
        #____________________________________________________________________________||
        
        pairs = matchObjectCollection( pfJets , genJets , 0.3 ) 

        for pfJet in pfJets:
            if pfJet.matched:
                matchGenJet = pairs[pfJet]
                self.hists["jetResponse"].Fill( pfJet.pt() / matchGenJet.pt() )
                self.hists["recoJetPt_vs_genJetPt"].Fill( pfJet.pt() , matchGenJet.pt() )

    def endJob(self):
        
        super(JetResponse,self).endJob()

        self.outFile.Write()

        self.outFile.Close()

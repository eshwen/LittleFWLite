#!/usr/bin/env python
from LoadLibraries import *
from InputParser import options
import signal

ROOT.gROOT.SetBatch(1)
ROOT.gROOT.ProcessLine( "gErrorIgnoreLevel = 1001;")

GLOBAL_LAST = False

inputPath = options.inputPath

def main():

    if getNEvents(inputPath):
        count(inputPath)

def count(inputPath):

    signal.signal(signal.SIGINT, handler)

    files = [inputPath]
    events = Events(files, maxEvents = options.nevents)

    handlePatMETs = Handle("std::vector<pat::MET>")
    handlePFCans = Handle("std::vector<pat::PackedCandidate>")
    handlePatJets = Handle("std::vector<pat::Jet>")

    for event in events:

        if GLOBAL_LAST: break

        run = event.eventAuxiliary().run()
        lumi = event.eventAuxiliary().luminosityBlock()
        eventId = event.eventAuxiliary().event()

	if run != 1 or lumi != 2433 or eventId != 319961: continue

	event.getByLabel(("packedPFCandidates","","PAT"), handlePFCans)
	pfCans = handlePFCans.product()

        #print '%10s' % 'pf.pt',
        #print '%10s' % 'pf.px',
        #print '%10s' % 'pf.py',
        #print '%10s' % 'pf.phi'
	metVec = ROOT.TLorentzVector()
	for pfCan in pfCans:
		tmpVec = ROOT.TLorentzVector()
		tmpVec.SetPtEtaPhiM(pfCan.pt(),pfCan.eta(),pfCan.phi(),pfCan.mass())
		metVec += tmpVec
		#print "%10.3f"%pfCan.pt(),
		#print "%10.3f"%pfCan.px(),
		#print "%10.3f"%pfCan.py(),
		#print "%10.3f"%pfCan.phi(),
		#print

        #print '%10s' % 'jet.pt',
        #print '%10s' % 'jet.eta',
        #print '%10s' % 'jet.phi'
        #print
	event.getByLabel(("slimmedJets","","PAT"), handlePatJets)
	pfJets = handlePatJets.product()
	mhtVec = ROOT.TLorentzVector()
	for jet in pfJets:
		#print "%10.3f"%jet.pt(),
		#print "%10.3f"%jet.eta(),
		#print "%10.3f"%jet.phi(),
		#print
		if jet.pt() < 40.: continue
		tempVec = ROOT.TLorentzVector()
		tempVec.SetPtEtaPhiM(jet.pt(),jet.eta(),jet.phi(),jet.mass())
		mhtVec += tempVec

	print " mht.pt ",mhtVec.Pt(),
	print " mht.phi ",mhtVec.Phi()
	print " met.pt ",metVec.Pt(),
	print " met.phi ",metVec.Phi()

        event.getByLabel(("slimmedMETs", "", "PAT"), handlePatMETs)
        slimmedMET = handlePatMETs.product().front()

	shift = 12
	level = 1
	print " rawMet.pt ",slimmedMET.shiftedPt(shift,level),
	print " rawMet.phi ",slimmedMET.shiftedPhi(shift,level)

	

##____________________________________________________________________________||
def getNEvents(inputPath):
    file = ROOT.TFile.Open(inputPath)
    events = file.Get('Events')
    return events.GetEntries()

##____________________________________________________________________________||
def handler( signum, frame ):
    global GLOBAL_LAST
    GLOBAL_LAST = True



##____________________________________________________________________________||
if __name__ == '__main__':
    main()

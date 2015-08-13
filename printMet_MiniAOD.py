#!/usr/bin/env python
from LoadLibraries import *
import signal
from optparse import OptionParser

ROOT.gROOT.SetBatch(1)
ROOT.gROOT.ProcessLine( "gErrorIgnoreLevel = 1001;")

##____________________________________________________________________________||
GLOBAL_LAST = False

##____________________________________________________________________________||
parser = OptionParser()
parser.add_option('-i', '--inputPath', default = '/afs/cern.ch/cms/Tutorials/TWIKI_DATA/MET/TTJets_MINIAODSIM_PHYS14_numEvent5000.root', action = 'store', type = 'string')
parser.add_option("-n", "--nevents", action = "store", default = -1, type = 'long', help = "maximum number of events to process")
(options, args) = parser.parse_args(sys.argv)
inputPath = options.inputPath

##____________________________________________________________________________||
def main():

    printHeader()
    if getNEvents(inputPath):
        count(inputPath)

##____________________________________________________________________________||
def printHeader():
    print '%6s'  % 'run',
    print '%10s' % 'lumi',
    print '%9s'  % 'event',
    print '%5s'  % 'nPU',
    print '%5s'  % 'nVtx',
    print '%25s' % 'object',
    print '%10s' % 'met.pt',
    print '%10s' % 'met.px',
    print '%10s' % 'met.py',
    print '%10s' % 'met.phi',
    print

##____________________________________________________________________________||
def count(inputPath):

    signal.signal(signal.SIGINT, handler)

    files = [inputPath]
    events = Events(files, maxEvents = options.nevents)

    handlePatMETs = Handle("std::vector<pat::MET>")
    handleVertices = Handle("std::vector<reco::Vertex>")
    handlePUSummaries = Handle("std::vector<PileupSummaryInfo>")

    # handlePFMETs = Handle("std::vector<reco::PFMET>")

    for event in events:

        if GLOBAL_LAST: break

        run = event.eventAuxiliary().run()
        lumi = event.eventAuxiliary().luminosityBlock()
        eventId = event.eventAuxiliary().event()

	if run != 1 or lumi != 2433 or eventId != 319961: continue

        # obtain the number of the mixed in-time pile-up interactions (MC only)
        # (https://twiki.cern.ch/twiki/bin/viewauth/CMS/SWGuideCMSDataAnalysisSchool2014PileupReweighting)
        event.getByLabel(("addPileupInfo", "", "HLT"), handlePUSummaries)
        puSummaries = handlePUSummaries.product()
        nInTimePileUp = puSummaries[[s.getBunchCrossing() for s in puSummaries].index(0)].getPU_NumInteractions()

        # obtain the number of the reconstructed primary vertices
        event.getByLabel(("offlineSlimmedPrimaryVertices", "", "PAT"), handleVertices)
        vertices = handleVertices.product()
        nVertices = vertices.size()

        # get "slimmedMETs"
        event.getByLabel(("slimmedMETs", "", "PAT"), handlePatMETs)
        slimmedMET = handlePatMETs.product().front()

        # get "Type-I PFMET"
        print '%6d %10d %9d %5d %5d' % (run, lumi, eventId, nInTimePileUp, nVertices),
        print '%25s'   % '"Type-I PFMET"',
        print '%10.3f' % slimmedMET.pt(),
        print '%10.3f' % slimmedMET.px(),
        print '%10.3f' % slimmedMET.py(),
        print '%10.3f' % (slimmedMET.phi()/math.pi*180.0),
        print

        # get "Type-I Smeared PFMET" (MC only)
        shift = 12
        level = 1
        print '%6d %10d %9d %5d %5d' % (run, lumi, eventId, nInTimePileUp, nVertices),
        print '%25s'   % '"Type-I Smeared PFMET"',
        print '%10.3f' % slimmedMET.shiftedPt(shift, level),
        print '%10.3f' % slimmedMET.shiftedPx(shift, level),
        print '%10.3f' % slimmedMET.shiftedPy(shift, level),
        print '%10.3f' % (slimmedMET.shiftedPhi(shift, level)/math.pi*180.0),
        print

        # get "Raw PFMET"
        # https://github.com/cms-sw/cmssw/blob/CMSSW_7_3_0_patch1/DataFormats/PatCandidates/interface/MET.h#L168-L175
        shift = 12
        level = 0
        print '%6d %10d %9d %5d %5d' % (run, lumi, eventId, nInTimePileUp, nVertices),
        print '%25s'   % '"Raw PFMET"',
        print '%10.3f' % slimmedMET.shiftedPt(shift, level),
        print '%10.3f' % slimmedMET.shiftedPx(shift, level),
        print '%10.3f' % slimmedMET.shiftedPy(shift, level),
        print '%10.3f' % (slimmedMET.shiftedPhi(shift, level)/math.pi*180.0),
        print

        # get "GenMET"
        genMET = slimmedMET.genMET()
        print '%6d %10d %9d %5d %5d' % (run, lumi, eventId, nInTimePileUp, nVertices),
        print '%25s'   % '"GenMET"',
        print '%10.3f' % genMET.pt(),
        print '%10.3f' % genMET.px(),
        print '%10.3f' % genMET.py(),
        print '%10.3f' % (genMET.phi()/math.pi*180.0),
        print


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

from optparse import OptionParser
import sys

parser = OptionParser()
parser.add_option('-i', '--inputPath', action = 'store', type = 'string')
parser.add_option("-n", "--nevents", action = "store", default = -1, type = 'long', help = "maximum number of events to process")
#(options, args) = parser.parse_args(sys.argv)



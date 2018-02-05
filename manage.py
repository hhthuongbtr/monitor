#!/usr/bin/python
import sys
from optparse import OptionParser
from services import FirstCheck, LastCheck, VideoCheck, Monitor, Snmp

if __name__ == "__main__":
    # Parsing argurments
    parser = OptionParser()
    parser.add_option("-s", "-S", dest="service_check", type="string",
                      help="Service check: first_check (f/F), last_check (l/L), video_check (v/V), snmp (s/S) and monitor (m/M).", metavar=' ')

    (options, args) = parser.parse_args()

    #Check argurments
    if not getattr(options, 'service_check'):
        print 'Option %s not specified' % 'service_check'
        parser.print_help()
        sys.exit(1)

    if options.service_check == 'f' or options.service_check == 'F' or options.service_check == 'first_check':
        fc = FirstCheck()
        fc.check()

    elif options.service_check == 'l' or options.service_check == 'L' or options.service_check == 'last_check':
        lc = LastCheck()
        lc.check()

    elif options.service_check == 'm' or options.service_check == 'M' or options.service_check == 'monitor':
        monitor = Monitor()
        monitor.monitor()

    elif options.service_check == 'v' or options.service_check == 'V' or options.service_check == 'video_check':
        vc = VideoCheck()
        vc.check()

    elif options.service_check == 's' or options.service_check == 'S' or options.service_check == 'snmp':
        snmp = Snmp()
        snmp.set()
 

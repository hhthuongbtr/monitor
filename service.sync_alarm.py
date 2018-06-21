import re
import logging
import logging.config
import logging.handlers
import sys, time, json
from optparse import OptionParser
from services import AsRequiredCheck
from BLL.profile import Profile as ProfileBLL
from supervisord import Supervisord
from config import SYSTEM
from rabbit import Rabbit

with open("/monitor/config/python_logging_configuration.json", 'r') as configuration_file:
    config_dict = json.load(configuration_file)
logging.config.dictConfig(config_dict)

def get_ip_from_ip_multicast(source):
    ip_pattern=re.compile("\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}")
    ip = re.findall(ip_pattern, source)
    ip = ip[0]
    return ip

class SyncAlam:
    def __init__(self):
        # Create the Logger
        self.logger = logging.getLogger("sync_alarm")

    def update_data(self, ip):
        pf = ProfileBLL()
        ip = get_ip_from_ip_multicast(ip)
        data = pf.get_by_ip_multicast(ip)
        profile = None
        if data["status"] == 200:
            profile_list = data["data"]
            if len(profile_list):
                profile = profile_list[0]
        else:
            self.logger.error(str(data["status"]) + " " + data["message"])
            time.sleep(5)
            data = pf.get_by_ip_multicast(ip)
            if data["status"] == 200:
                profile_list = data["data"]
                if len(profile_list):
                    profile = profile_list[0]
            else:
                self.logger.error(str(data["status"]) + " " + data["message"])
        return profile

    def check(self, profile):
        ip = get_ip_from_ip_multicast(profile["ip"])
        self.logger.warning('Start check source %s'%(ip))
        times = 0
        check = 0
        arc = AsRequiredCheck()
        while 1:
            times += 1
            if (times % 10 == 0) or (check == -1):
                profile = None
                profile = self.update_data(ip)
            self.logger.info('Check ip %s, %d times'%(ip, times))
            check = arc.check(profile, times)
            """
            Condition break loop
            status code:
             1: channel up
             404: During monitor system is cancel.
            """
            if check == 1 or check == 404:
                self.logger.warning('finish check ip %s, %d times'%(ip, times))
                break
            time.sleep(5)
        return 0

if __name__ == "__main__":
    # Parsing argurments
    parser = OptionParser()
    parser.add_option("-s", "-S", dest="ip", type="string",
                      help="ip multicast(Ex: 225.1.1.1).", metavar=' ')
    parser.add_option("-j", "-J", dest="jid", type="string",
                      help="Job id.", metavar=' ')
    parser.add_option("-H", dest="thomson_host", type="string",
                      help="ip thomson is running job.", metavar=' ')
    (options, args) = parser.parse_args()
    check = 0
    #Check argurments
    if not getattr(options, 'ip'):
        print 'Option %s not specified'%(ip)
        self.logger.error('Option %s not specified'%(ip))
        parser.print_help()
    else:
        """
        Process monitor source
        """
        sa = SyncAlam()
        ip = get_ip_from_ip_multicast(options.ip)
        profile = sa.update_data(ip)
        if not profile:
            raise ValueError('could not find %s' % (options.ip))
        else:
            check = sa.check(profile)
    try:
        if options.jid != "None" and check == 1:
            try:
                jid = int(options.jid)
                message = {"host"    : options.thomson_host,
                           "jid"     : jid,
                           "source"  : get_ip_from_ip_multicast(options.ip),
                           "status"  : check
                          }
                running_backup_queue = Rabbit(SYSTEM["RUNNING_BACKUP_QUEUE"])
                running_backup_queue.push(json.dumps(message))
            except Exception as e:
                self.logger.error(str(e))
        """
        clear supervisord job config
        """
        rb = Rabbit(SYSTEM["HOST"])
        rb.push("100")
    except Exception as e:
        print e
        self.logger.error(str(e))
    time.sleep(10)

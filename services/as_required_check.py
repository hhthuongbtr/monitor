import json
import time
import logging
import threading
from utils.file import File
from utils import Ffmpeg
from utils import DateTime
from BLL.log import Log as LogBLL
from config.config import SYSTEM
from BLL.profile import Profile as ProfileBLL
from snmp_agent import Snmp

class AsRequiredCheck(object):
    """docstring for LastCheck"""
    def __init__(self):
        self.logger = logging.getLogger(__name__)


    def check_source(self, source, last_status, id, agent, name, type, times):
        """
        Get status of profile, if stastus not change then update check equal 1.      
        Ffmpeg: Use Ffprobe to check stastus profile (source) and return flag 
        0 is down
        1 is up
        2 is video error
        3 is audio eror 
        """
        self.logger.debug("Check source: %s %s %s"%(source, name, type))
        date_time = DateTime()
        opdate = date_time.get_now()
        ffmpeg = Ffmpeg()
        profile_status = 0
        check = ffmpeg.check_source(source)
        self.logger.debug("Curent :%s <> Last: %s, %s %s %s"%(check, last_status, source, name, type))
        status = {0: "DOWN       ", 1: "UP         ", 2: "VIDEO ERROR", 3: "AUDIO ERROR"} [check]
        """+
        write log
        """
        if not times or times == 1:
            cldate = date_time.get_now()
            rslog = {
                     "sev"        : "Critical",
                     "jname"      : name,
                     "type"       : type,
                     "res"        : source,
                     "desc"       : status,
                     "cat"        : "Communication",
                     "host"       : agent,
                     "opdate"     : opdate,
                     "as_required": True,
                     "cldate"     : cldate
                 }
            self.logger.critical(json.dumps(rslog))
        """
        update status
        """
        if check != last_status:
            if times > 1:
                cldate = date_time.get_now()
                rslog = {
                         "sev"        : "Critical",
                         "jname"      : name,
                         "type"       : type,
                         "res"        : source,
                         "desc"       : status,
                         "cat"        : "Communication",
                         "host"       : agent,
                         "opdate"     : opdate,
                         "as_required": True,
                         "cldate"     : cldate
                     }
                self.logger.critical(json.dumps(rslog))
            child_thread_list = []
            profile = ProfileBLL()
            profile_data = {"status": check, "agent": agent, "ip": SYSTEM["HOST"]}
            child_thread = threading.Thread(target=profile.put, args=(id, profile_data,))
            child_thread.start()
            child_thread_list.append(child_thread)
            """Append log"""
            channel = """%s %s"""%(name, type)
            while len(channel) < 22:
                channel += " "
            while len(source) < 27:
                source += " "
            ip_config = SYSTEM["HOST"]
            while len(ip_config) < 16:
                ip_config += " "
            #message = """%s (ip:%s) %s in host: %s (%s)""" % (channel, source, status, ip_config, agent)
            #log_data = {"host": source, "tag": "status", "msg": message}
            #log = LogBLL()
            #child_thread = threading.Thread(target=log.post, args=(log_data,))
            #child_thread.start()
            #child_thread_list.append(child_thread)
            """Update local snmp IPTV"""
            if "origin" or "4500" in agent:
                self.logger.debug("%s is core probe"%(agent))
                time.sleep(2)
                snmp = Snmp()
                child_thread = threading.Thread(target=snmp.set)
                child_thread.start()
                child_thread_list.append(child_thread)

            """
            Wait for update database complete
            """
            for child_thread in child_thread_list:
                child_thread.join()
                return -1
        return check

    def check(self, profile, times = None):
        if not profile:
            self.logger.warning("Source not found")
            return 404
        return self.check_source(profile['protocol'] + "://" +profile['ip'],
                    profile['status'],
                    profile['id'],
                    profile['agent'],
                    profile['name'],
                    profile['type'],
                    times)

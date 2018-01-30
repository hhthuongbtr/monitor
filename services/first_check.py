#!/usr/bin/python
import sys
import time
import logging
import threading
from utils.file import File
from utils.ffmpeg import Ffmpeg
from BLL.profile import Profile as ProfileBLL
from config.config import SOURCE_MONITOR as is_monitor

class FirstCheck(object):
    """docstring for FirstCheck"""
    def __init__(self):
        self.logger = logging.getLogger(__name__)

    def check_source(self, source, last_status, id, agent, thread, name, type):
        """
        Get status of profile, if stastus not change then update check equal 1.      
        Ffmpeg: Use Ffprobe to check stastus profile (source) and return flag 
        0 is down
        1 is up
        2 is video error
        3 is audio eror 
        """
        ffmpeg = Ffmpeg()
        check = ffmpeg.check_source(source)
        # print "%s : %s"%(check, last_status)
        self.logger.info("Curent :%s <> Last: %s"%(check, last_status))
        if check != last_status:
            json_data = """{"source":"%s","status":%s,"pa_id":%s,"agent": "%s","thread":%s,"name":"%s","type":"%s"}"""%(source, last_status, id, agent, thread, name, type)
            file = File()
            replicate = file.append(json_data)
            if not replicate:
                self.logger.warning("Doubt curent %s <> Last %s : %s"%(check, last_status, str(json_data)))


    def check(self):
        if not is_monitor:
            message = "Black screen monitor is disable, check your config!"
            self.logger.warning(message)
            print message
            time.sleep(60)
            exit(0)
        try:
            profileBLL = ProfileBLL()
            data = profileBLL.get()
            print data
            if data["status"] == 200:
                profile_list = data["data"]
            else:
                self.logger.warning(str(data["status"]) + " " + data["message"])
                print "Error code: " + str(data["status"])
                print data["message"]
                exit(1)
            # ancestor_thread_list = []
            for profile in profile_list:
                while threading.activeCount() > profile['thread']:
                    time.sleep(1)
                t = threading.Thread(target=self.check_source,
                    args=(profile['protocol']+'://'+profile['ip'],
                        profile['status'],
                        profile['id'],
                        profile['agent'],
                        profile['thread'],
                        profile['name'],
                        profile['type'],
                    )
                )
                t.start()
            #     ancestor_thread_list.append(t)
            # 
            # Wait for all threads finish
            # 
            # for ancestor_thread in ancestor_thread_list:
            #     ancestor_thread.join()
        except Exception as e:
            self.logger.error(str(e))
            print e
        finally:
            time.sleep(20)


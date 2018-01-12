#!/usr/bin/python
import json
import time
import threading
from utils.file import File
from utils.ffmpeg import Ffmpeg
from BLL.log import Log as LogBLL
from config.config import IP as ip
from BLL.profile import Profile as ProfileBLL

def check_source(source, last_status, id, name, type):
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
    print "%s : %s"%(check, last_status)
    if check != last_status:
        time.sleep(30)
        recheck = ffmpeg.check_source(source)
        if recheck == check:
            if check == 1:
                status = 'up'
            elif check == 2:
                status = 'video error'
            elif check == 3:
                status = 'audio error'
            elif check == 0:
                status = 'down'
            else:
                status = "unknown" + str(check) + ":"
            """
            Update status and write log
            """
            child_thread_list = []
            profile = ProfileBLL()
            profile_data = {"status": check}
            child_thread = threading.Thread(target=profile.put, args=(id, profile_data,))
            child_thread.start()
            child_thread_list.append(child_thread)
            message = """%s %s (ip:%s) status %s in host: %s""" % (name, type, source, status, ip)
            log_data = {"host": source, "tag": "status", "msg": message}
            log = LogBLL()
            child_thread = threading.Thread(target=log.post, args=(log_data,))
            child_thread.start()
            child_thread_list.append(child_thread)
            """
            Wait for update database complete
            """
            for child_thread in child_thread_list:
                child_thread.join()
            return 1
    return 0


###############################################################################
#                                                                             #
#                                  MAIN                                       #
#                                                                             #
###############################################################################
if __name__ == "__main__":
    ancestor_thread_list = []
    file = File()
    profile_list = file.read()
    profile_list = profile_list[0:len(profile_list)-1]
    if(profile_list):
        for line in profile_list.split('\n'):
            profile = json.loads(line)
            while threading.activeCount() > profile['thread']:
                time.sleep(1)
            t = threading.Thread(target=check_source,args=(profile['source'],
                profile['status'],
                profile['pa_id'],
                profile['name'],
                profile['type'],
                )
            )
            t.start()
            ancestor_thread_list.append(t)
    for ancestor_thread in ancestor_thread_list:
        ancestor_thread.join()
    time.sleep(5)

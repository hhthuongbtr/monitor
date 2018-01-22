#!/usr/bin/python
import threading
import time
from utils.ffmpeg import Ffmpeg
from utils.file import File
from BLL.profile import Profile as ProfileBLL
from config.config import SOURCE_MONITOR as is_monitor

def check_source(source, last_status, id, agent, thread, name, type):
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
    if check != last_status:
        json_data = """{"source":"%s","status":%s,"pa_id":%s,"agent": "%s","thread":%s,"name":"%s","type":"%s"}"""%(source, last_status, id, agent, thread, name, type)
        file = File()
        file.append(json_data)

###############################################################################
#                                                                             #
#                                 MAIN                                        #
#                                                                             #
###############################################################################

if __name__ == "__main__":
    if not is_monitor:
        print "Black screen monitor is disable, check your config!"
        exit(0)
    try:
        profileBLL = ProfileBLL()
        data = profileBLL.get()
        if data["status"] == 200:
            profile_list = data["data"]
        else:
            print "Error code: " + str(data["status"])
            print data["message"]
            exit(1)
        # ancestor_thread_list = []
        for profile in profile_list:
            while threading.activeCount() > profile['thread']:
                time.sleep(1)
            t = threading.Thread(target=check_source,
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
        print e
    finally:
        time.sleep(20)


import datetime
from datetime import datetime
import time
import re


class DateTime:
    def conver_human_creadeble_2_unix_timetamp(self, date_time):
        return int(time.mktime(time.strptime(date_time, '%Y-%m-%d %H:%M:%S')))

    def conver_human_creadeble_2_unix_timetamp_local(self, date_time):
        date_time_pattern = re.compile("\d{4}[/.-]\d{2}[/.-]\d{2} \d{2}:\d{2}:\d{2}")
        date_time_data = re.findall(date_time_pattern, date_time)
        date_time = date_time_data[0]
        return int(time.mktime(time.strptime(date_time, '%Y-%m-%d %H:%M:%S'))) - time.timezone

    def get_now(self):
        now = time.time()
        now_pattern = re.compile("\d+") 
        now = re.findall(now_pattern, str(now))
        now = now[0]
        return int(now)

    def convert_date_pattern_2_unix_timestamp(self, ss, mm, hh, DD, MM, YYYY):
        human_date = "%s-%s-%s %s:%s:%s"%(YYYY,MM,DD,hh,mm,ss)
        return (int(time.mktime(time.strptime(human_date, '%Y-%m-%d %H:%M:%S')))) #- time.timezone)
        
    #data input string YYYY-MM-DDTHH:mm:ss.000Z, return a string
    def conver_UTC_2_unix_timestamp(self, utc_time):
        ts = time.strptime(utc_time[:19], "%Y-%m-%dT%H:%M:%S")
        human_date = time.strftime("%Y-%m-%d %H:%M:%S", ts)
        return (int(time.mktime(time.strptime(human_date, '%Y-%m-%d %H:%M:%S'))) - time.timezone)

    def get_now_as_human_creadeble(self):
        return (time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))

    def convert_unix_timestamp_2_human_creadeble(self, timestamp):
        return (time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(int(timestamp))))

    def get_now_as_isofortmat(self):
        now = datetime.datetime.now()
        format_iso_now = now.isoformat()
        return format_iso_now

    def get_hour(self, unix_timestamp):
        dt = datetime.fromtimestamp(unix_timestamp)
        return dt.hour

#!/usr/bin/python
SOURCE_MONITOR = True #(True/False)
BLACK_SCREEN_MONITOR = False #(True/False)
#Host
IP='10.0.0.205'
#re check break time (second)
BREAK_TIME = 15
#API monitor
USER = 'monitor'
PASSWD = 'iptv13579'
##[Master] 
MASTER_API = 'http://10.0.0.205:8888/'
##[SLAVE]
DEFINE_SLAVE_API = False
SLAVE_API = 'http://42.117.9.100:8888/'
#Database
DEFINE_DATABASE_BACKUP = True
DATABASE_HOST = 'localhost'
DATABASE_PORT = 3306
DATABASE_USER = 'root'
DATABASE_PASSWORD = 'root'
DATABASE_NAME = 'monitor'
#FFMPEG libery
FFPROBE_PATH = '/usr/local/bin/ffprobe'
FFMPEG_PATH = '/usr/bin/ffmpeg'


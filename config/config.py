#!/usr/bin/python
SOURCE_MONITOR = True #(True/False)
BLACK_SCREEN_MONITOR = False #(True/False)
BROADCAST_TIME_FROM = 6
BROADCAST_TIME_TO = 22
#Host
IP='172.28.0.78'
#re check break time (second)
BREAK_TIME = 15
#API monitor
USER = 'monitor'
PASSWD = 'iptv13579'
##[Master] 
MASTER_API = 'http://42.117.9.99:88888/'
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
FFPROBE_PATH = '/usr/bin/ffprobe'
FFMPEG_PATH = '/usr/bin/ffmpeg'


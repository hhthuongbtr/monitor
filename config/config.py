#!/usr/bin/python
#Host
IP='172.28.0.94'
#re check break time (second)
BREAK_TIME = 15
#API monitor
USER = 'monitor'
PASSWD = 'iptv13579'
##[Master] 
MASTER_API = 'http://10.0.0.205:8000/'
##[SLAVE]
DEFINE_SLAVE_API = False
SLAVE_API = 'http://42.117.9.99:88887/'
#Database
DEFINE_DATABASE_BACKUP = False
DATABASE_HOST = 'localhosts'
DATABASE_PORT = 3306
DATABASE_USER = 'root'
DATABASE_PASSWORD = 'root'
DATABASE_NAME = 'monitor'


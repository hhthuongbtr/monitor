#!/usr/bin/python
#Host
IP='172.28.0.218'
#API monitor
USER = 'monitor'
PASSWD = 'iptv13579'
URL = 'http://42.117.9.99:88888/'
URL_LOG = URL + 'log/'
URL_AGENT = URL + 'agent/'
URL_SNMP = URL+"profile_agent/snmp/"+IP
URL_PROFILE_AGENT = URL + 'profile_agent/'
#Database
DEFINE_DATABASE_BACKUP = True
DATABASE_HOST = 'localhost'
DATABASE_PORT = 3306
DATABASE_USER = 'root'
DATABASE_PASSWORD = 'root'
DATABASE_NAME = 'monitor'

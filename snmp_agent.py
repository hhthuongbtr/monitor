#!/usr/bin/python
import os
import smtplib
import urllib, json

#Execute bash shell command
def execute_command(cmd):
    os.system(cmd)

def write_null():
    execute_command("cat /dev/null > /monitor/snmp/agent/channel_name")
    execute_command("cat /dev/null > /monitor/snmp/agent/channel_status")
    execute_command("cat /dev/null > /monitor/snmp/agent/channel_profile")
    execute_command("cat /dev/null > /monitor/snmp/analyzer/channel_name")
    execute_command("cat /dev/null > /monitor/snmp/analyzer/channel_status")
    execute_command("cat /dev/null > /monitor/snmp/analyzer/channel_profile")

#read config file
configfile='/monitor/config/config.py'
if os.path.exists(configfile):
    execfile(configfile)
else:
    print "can't read file config"
    exit(1)

#get snmp API
response = urllib.urlopen(api+"profile_agent/snmp/"+ip)
if response.getcode()==200:
    #Refesh snmp file
    write_null()
    #write snmp file
    profile_agents = json.loads(response.read())
    for profile_agent in profile_agents['profile_agent_snmp']:
        #Agent_IPTV_Status
        if profile_agent['monitor']==1:
            cmd="echo '%s-%s' >> /monitor/snmp/agent/channel_name"%(profile_agent['name'],profile_agent['type'])
            execute_command(cmd)
            cmd="echo '%s' >> /monitor/snmp/agent/channel_profile"%(profile_agent['ip'])
            execute_command(cmd)
            cmd="echo '%s' >> /monitor/snmp/agent/channel_status"%(profile_agent['status'])
            execute_command(cmd)
        #Agent_IPTV_Analyzer
        if profile_agent['analyzer']==1:
            cmd="echo '%s-%s' >> /monitor/snmp/analyzer/channel_name"%(profile_agent['name'],profile_agent['type'])
            execute_command(cmd)
            cmd="echo '%s' >> /monitor/snmp/analyzer/channel_profile"%(profile_agent['ip'])
            execute_command(cmd)
            cmd="echo '%s' >> /monitor/snmp/analyzer/channel_status"%(profile_agent['analyzer_status'])
            execute_command(cmd)

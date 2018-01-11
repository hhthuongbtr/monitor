#!/bin/bash
/usr/bin/python /monitor/snmp_agent.py > /dev/null
sleep 10
/usr/bin/python /monitor/monitor.py > /dev/null


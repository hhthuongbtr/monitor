#!/bin/bash
/usr/bin/python /monitor/manage.py -s snmp > /dev/null
sleep 10
/usr/bin/python /monitor/manage.py -s monitor > /dev/null


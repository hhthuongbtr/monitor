#!/bin/bash
/usr/local/bin/python /monitor/manage.py -s snmp > /dev/null
sleep 10
/usr/local/bin/python /monitor/manage.py -s monitor > /dev/null


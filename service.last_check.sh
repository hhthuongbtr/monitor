#!/bin/sh
while [ 1 ]
do
    /usr/local/bin/python /monitor/manage.py -s last_check > /dev/null
done



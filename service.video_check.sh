#!/bin/sh
while [ 1 ]
do
        /usr/bin/python /monitor/manage.py -s video_check 2> /dev/null 
done


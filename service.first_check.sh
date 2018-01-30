#!/bin/sh
while [ 1 ]
do
        /usr/bin/python /monitor/manage.py -s first_check 2> /dev/null 
done


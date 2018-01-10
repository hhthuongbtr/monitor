#!/usr/bin/python
import os, re, fnmatch
import psutil # pip install psutil
import urllib, json

class SystemStatus:
    def get_mem(self):
        info=str(psutil.virtual_memory())
        mem = re.search('(?<=percent=)\d+', info)
        return mem.group(0)

    def get_disk(self):
        info=str(psutil.disk_usage('/'))
        disk = re.search('(?<=percent=)\d+', info)
        return disk.group(0)

    def get_cpu(self):
        cpu=int(round( psutil.cpu_percent(interval=1), 0))
        return cpu


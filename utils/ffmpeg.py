#!/usr/bin/python
import time
from subprocess import call
import os, sys, subprocess, shlex, re, fnmatch,signal

class Ffmpeg:
    def check_source(self, source):
        cmnd = ['/usr/local/bin/ffprobe', source, '-v', 'quiet' , '-show_format', '-show_streams']
        p = subprocess.Popen(cmnd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        timeout = 15
        i = 0
        while p.poll() is None:
            time.sleep(1)
            i+=1
            if i > timeout:
                os.kill(p.pid, signal.SIGKILL)
        out, err = p.communicate()
        value=0
        audio=0
        video=0
        for line in out.split('\n'):
            line = line.strip()
            if (line.startswith('filename=')):
                value=1
            if (line.startswith('codec_type=audio')):
                audio=1
            if (line.startswith('codec_type=video')):
                video=1
        if value == 1 and audio == 1 and video == 1:
            return 1
        if value == 1 and audio == 1 and video == 0:
            return 2
        if value == 1 and audio == 0 and video == 1:
            return 3
        return 0

    def capture_image(self):
        pass


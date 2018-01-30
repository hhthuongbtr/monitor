import os

class File:
    def __init__(self):
        self.filedir= "/tmp/checkdata.tmp"
        self.inprocess="/tmp/inprocess.tmp"
        if not os.path.exists(self.filedir):
            command="echo '\n' >"+self.filedir
            os.system(command)
        if not os.path.exists(self.inprocess):
            command="echo '\n' >"+self.inprocess
            os.system(command)

    def read(self):
        #Read file checkdata.tmp
        f = open(self.filedir, 'r')
        lines=f.read()
        f.close()
        #Clear checkdata.tmp after read
        command="cat /dev/null > "+self.filedir
        os.system(command)
        #clear all and write data to inprocess file
        command="cat /dev/null > "+self.inprocess
        os.system(command)
        f = open(self.inprocess, 'a')
        f.write(lines)
        f.close()
        #return data
        return lines

    def append(self, text):
        f = open(self.filedir, 'r')
        data_rows = f.read()
        f.close()
        fips = open(self.inprocess, 'r')
        data_ips = fips.read()
        fips.close()
        if (text not in data_rows)and (text not in data_ips):
            f = open(self.filedir, 'a')
            f.write(text+"\n")
            f.close()
            return 0
        else:
            print "replicate"
            return 1

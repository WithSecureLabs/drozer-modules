from drozer import android
from drozer.modules import common, Module

class Clipboard(Module, common.FileSystem, common.ClassLoader):

    name = "Retrieve and display the current clipboard text."
    description = "Retrieve and display the current clipboard text."
    examples = """
dz> run post.capture.clipboard
[*] Clipboard value: test123
"""
    author = "Tyrone (@mwrlabs)"
    date = "2014-04-30"
    license = "BSD (3 clause)"
    path = ["post", "capture"]
    permissions = ["com.mwr.dz.permissions.GET_CONTEXT"]

    def execute(self, arguments):
        con = self.getContext()
        clip = con.getSystemService(con.CLIPBOARD_SERVICE)
        self.stdout.write("[*] Clipboard value: %s\n\n" % clip.getText())

class SetClipboard(Module, common.FileSystem, common.ClassLoader):

    name = "Put the specified text into the clipboard."
    description = "Put the specified text into the clipboard."
    examples = """
dz> run post.perform.setclipboard test123
[*] Clipboard value set: test123
"""
    author = "Tyrone (@mwrlabs)"
    date = "2014-04-30"
    license = "BSD (3 clause)"
    path = ["post", "perform"]
    permissions = ["com.mwr.dz.permissions.GET_CONTEXT"]
    
    def add_arguments(self, parser):
        parser.add_argument("text", help="value to set the clipboard to")

    def execute(self, arguments):
        con = self.getContext()
        clip = con.getSystemService(con.CLIPBOARD_SERVICE)
        clip.setText(arguments.text)
        self.stdout.write("[*] Clipboard value set: %s\n\n" % arguments.text)
            
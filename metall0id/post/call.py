from drozer import android
from drozer.modules import common, Module

class Call(Module, common.FileSystem, common.ClassLoader):

    name = "Call a phone number"
    description = "Call a phone number. Relies on the agent having the CALL_PHONE permission."
    examples = """
dz> run post.perform.call +27123456789
[*] Sent intent to call +27123456789
"""
    author = "Tyrone (@mwrlabs)"
    date = "2013-04-23"
    license = "BSD (3 clause)"
    path = ["post", "perform"]
    permissions = ["android.permission.CALL_PHONE", "com.mwr.dz.permissions.GET_CONTEXT"]
    
    def add_arguments(self, parser):
        parser.add_argument("number", help="number to call e.g. +27123456789")

    def execute(self, arguments):
            
        # Initiate the phone call
        intent = android.Intent(action="android.intent.action.CALL", data_uri="tel:" + arguments.number, flags=["ACTIVITY_NEW_TASK"])
        self.getContext().startActivity(intent.buildIn(self))

        self.stdout.write("[*] Sent intent to call %s\n" % arguments.number)

from drozer import android
from drozer.modules import common, Module

class Call(Module, common.FileSystem, common.ClassLoader):

    name = "Call a phone number"
    description = "Call a phone number. Relies on the agent having the CALL_PHONE permission."
    examples = """
mercury> run post.perform.call +27123456789
[*] Sent intent to call +27123456789
"""
    author = "Tyrone (@mwrlabs)"
    date = "2013-04-23"
    license = "MWR Code License"
    path = ["post", "perform"]
    permissions = ["android.permission.CALL_PHONE"]
    
    def add_arguments(self, parser):
        parser.add_argument("number", help="number to call e.g. +27123456789")

    def execute(self, arguments):
        
        # Check that the agent has the CALL_PHONE permission
        packageManager = self.getContext().getPackageManager()
        if not packageManager.checkPermission("android.permission.CALL_PHONE", self.getContext().getPackageName()) == packageManager.PERMISSION_GRANTED:
            self.stdout.write("[-] This agent does not have the CALL_PHONE permission. Exiting...\n")
            return
            
        # Initiate the phone call
        intent = android.Intent(action="android.intent.action.CALL", data_uri="tel:" + arguments.number, flags=["ACTIVITY_NEW_TASK"])
        self.getContext().startActivity(intent.buildIn(self))

        self.stdout.write("[*] Sent intent to call %s\n" % arguments.number)

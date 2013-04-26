from mwr.droidhg.modules import common, Module
import subprocess, os, time

class Screenshot(Module, common.ClassLoader, common.FileSystem, common.Shell, common.SuperUser):

    name = "Take a screenshot of the device"
    description = "Take a screenshot of the device. Relies on minimal-su being correcly installed on the device (see tools.setup.minimalsu)"
    examples = """mercury> run post.capture.screenshot
Done.
"""
    author = "Tyrone (@mwrlabs)"
    date = "2013-04-18"
    license = "MWR Code License"
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
        self.shellExec("su -c \"screencap -p /data/data/com.mwr.droidhg.agent/screenshot.png\"")
        
        # Download
        length = self.downloadFile("/data/data/com.mwr.droidhg.agent/screenshot.png", filename)
        
        # Remove screenshot from device
        self.shellExec("su -c \"rm /data/data/com.mwr.droidhg.agent/screenshot.png\"")
        
        if length != None:
            self.stdout.write("Done.\n")
            
            # Open in default application
            if os.name == 'posix':
                subprocess.call(('xdg-open', filename))
            elif os.name == 'nt':
                os.startfile(filename)
            elif os.name == 'darwin':
                os.system("open " + filename);
        else:
            self.stderr.write("Screenshot download failed.\n")

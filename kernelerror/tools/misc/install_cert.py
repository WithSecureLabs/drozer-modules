from drozer.modules import common, Module
from drozer import android
import argparse

class InstallCert(Module):

    name = "Install a CA cert"
    description = ""
    author = "Bernard Wagner"
    date = "2014-09-22"
    license = "BSD (3-clause)"
    path = ["tools", "misc"]

    def add_arguments(self,parser):
        parser.add_argument("--src",help="specify the path of the certificate to install")
        parser.add_argument("--name",help="specify the name of the certificate")

    def execute(self, arguments):
        try:
            print "Uploading"
            cert = open(arguments.src, 'rb').read()
            intent = android.Intent(action="android.credentials.INSTALL", extras = [], flags = [])
            intent.extras.append(("string","name",arguments.name))
            intent.extras.append(("bytearray","CERT",cert))
            intent.flags.append(("ACTIVITY_NEW_TASK"))
            self.getContext().startActivity(intent.buildIn(self))
        except Exception as error:
            print error


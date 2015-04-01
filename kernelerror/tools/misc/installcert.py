import os
from drozer.modules import common, Module
from drozer import android
import argparse

class InstallCert(Module):

    name = "Install CA certificate"
    description = "Install a CA certificate from the host machine. Depending on the device, the users will be prompted before installing the certificate and a pin, password or pattern lock-screen needs to be configured."
    author = "Bernard Wagner"
    date = "2014-09-22"
    license = "BSD (3-clause)"
    path = ["tools", "misc"]

    def add_arguments(self,parser):
        parser.add_argument("source",help="specify the path of the certificate to install")
        parser.add_argument("-n","--name",default=None,help="specify the name of the certificate")

    def execute(self, arguments):
        try:
            print "Uploading"
            myfile = open(arguments.source, 'rb')
            with myfile:
                cert = myfile.read()
                intent = android.Intent(action="android.credentials.INSTALL", extras = [], flags = [])
                name = arguments.name 
                if arguments.name == None:
                    name = os.path.basename(arguments.source).split('.')[0]
                intent.extras.append(("string","name",name))
                intent.extras.append(("bytearray","CERT",cert))
                intent.flags.append(("ACTIVITY_NEW_TASK"))
                self.getContext().startActivity(intent.buildIn(self))
                print "Done"
        except Exception as error:
            print error


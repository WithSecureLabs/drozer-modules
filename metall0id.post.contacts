from drozer.modules import common, Module

class Read(Module, common.Provider, common.TableFormatter, common.ClassLoader):

    name = "Read all contacts"
    description = "Read all contacts and filter by names or cellphone numbers. Relies on the agent having the READ_CONTACTS permission."
    examples = """
dz> run post.contacts.read

| Homer Simpson           | 12345678901      |
| Internet Support Centre | +27 20 7597 4131 |
| James Bond              | +4479445543007   |
"""
    author = "Tyrone (@mwrlabs)"
    date = "2014-11-16"
    license = "BSD (3 clause)"
    path = ["post", "contacts"]
    permissions = ["android.permission.READ_CONTACTS", "com.mwr.dz.permissions.GET_CONTEXT"]
    
    def add_arguments(self, parser):
        parser.add_argument("-f", "--filter", default=None, help="filter results by a keyword")

    def execute(self, arguments):

        ContactsContractCommonDataKindsPhone = self.klass("android.provider.ContactsContract$CommonDataKinds$Phone")
        uri = str(ContactsContractCommonDataKindsPhone.CONTENT_URI.toString())
        displayName = str(ContactsContractCommonDataKindsPhone.DISPLAY_NAME)
        number = str(ContactsContractCommonDataKindsPhone.NUMBER)

        if not arguments.filter:
            c = self.contentResolver().query(uri, {displayName, number})
        else:
            filt = displayName + " like '%" + arguments.filter + "%' or "
            filt += number + " like '%" + arguments.filter + "%'"
            c = self.contentResolver().query(uri, {displayName, number}, filt)

        if c != None:
            rows = self.getResultSet(c)
            self.print_table(rows, show_headers=False, vertical=False)
        else:
            self.stdout.write("Unknown Error.\n")
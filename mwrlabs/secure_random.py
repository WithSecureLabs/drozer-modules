from pydiesel.reflection import ReflectionException

from drozer.modules import common, Module

class SecureRandom(Module, common.FileSystem, common.PackageManager, common.Provider, common.Strings, common.ZipFile):

    name = "SecureRandom Check"
    description = """
    Finds applications that make use of java.security.SecureRandom as a source of random numbers.

    It was identified that on some versions of Android the SecureRandom random number generator did not correctly seed the underlying PRNG, which could cause predictable sequences of numbers to be generated.

    See: http://android-developers.blogspot.co.uk/2013/08/some-securerandom-thoughts.html
    """
    examples = ""
    author = "@HenryHoggard (@mwrlabs)"
    date = "2013-08-13"
    license = "BSD (3 clause)"
    path = ["scanner", "misc"]
    permissions = ["com.mwr.dz.permissions.GET_CONTEXT"]

    def add_arguments(self, parser):
        parser.add_argument("-a", "--package", "--uri", dest="package_or_uri", help="specify a package, or content uri to search", metavar="<package or uri>")
        parser.add_argument("-v", "--verbose", action="store_true", help="enable verbose mode")

    def execute(self, arguments):
        if arguments.package_or_uri != None:
            self.check_package(arguments.package_or_uri)

        else:
            for package in self.packageManager().getPackages(common.PackageManager.GET_PERMISSIONS):
                try:
                    self.check_package(package.packageName, arguments)
                except Exception, e:
                    print str(e)


    def check_package(self, package, arguments):    
        self.deleteFile("/".join([self.cacheDir(), "classes.dex"]))
        
        for path in self.packageManager().getSourcePaths(package):
            strings = []
            if ".apk" in path:
                dex_file = self.extractFromZip("classes.dex", path, self.cacheDir())
                if dex_file != None:
                    strings = self.getStrings(dex_file.getAbsolutePath())

                    dex_file.delete()
                    strings += self.getStrings(path.replace(".apk", ".odex")) 
            elif (".odex" in path):
                strings = self.getStrings(path)
            else:
                continue

            securerandom = "false"
            if "java.security.SecureRandom" in str(strings) or "Ljava/security/SecureRandom" in str(strings):
                securerandom = "true"

            if securerandom == "true":
                self.stdout.write("[color red]%s uses SecureRandom[/color]\n" % package)
            elif arguments.verbose:
                self.stdout.write("[color green]%s doesn't use SecureRandom[/color]\n" % package)


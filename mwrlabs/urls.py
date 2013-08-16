from pydiesel.reflection import ReflectionException

from drozer.modules import common, Module

class WebURLs(Module, common.FileSystem, common.PackageManager, common.Provider, common.Strings, common.ZipFile):

    name = "Find HTTP and HTTPS URLs specified in packages."
    description = """
    Finds URLs with the HTTP or HTTPS schemes by searching the strings inside APK files.

    You can, for instance, use this for finding API servers, C&C servers within malicious APKs and checking for presence of advertising networks.
    """
    examples = ""
    author = "MWR InfoSecurity (@mwrlabs)"
    date = "2013-08-16"
    license = "BSD (3 clause)"
    path = ["scanner", "misc"]
    permissions = ["com.mwr.dz.permissions.GET_CONTEXT"]

    def add_arguments(self, parser):
        parser.add_argument("-a", "--package", help="specify a package to search")

    def execute(self, arguments):
        if arguments.package != None:
            self.check_package(arguments.package, arguments)
        else:
            for package in self.packageManager().getPackages(common.PackageManager.GET_PERMISSIONS):
                try:
                    self.check_package(package.packageName, arguments)
                except Exception, e:
                    print str(e)


    def check_package(self, package, arguments):
        self.deleteFile("/".join([self.cacheDir(), "classes.dex"]))

        http_urls = []
        https_urls = []

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


            for s in strings:
                if "http://" in s:
                    http_urls.append(s)
                elif "https://" in s:
                    https_urls.append(s)

            if len(http_urls) > 0 or len(https_urls) > 0:
                self.stdout.write("%s\n" % str(package))

            for http_url in http_urls:
                self.stdout.write("  %s\n" % http_url)
            for https_url in https_urls:
                self.stdout.write("  %s\n" % https_url)

            if len(http_urls) > 0 or len(https_urls) > 0:
                self.stdout.write("\n")


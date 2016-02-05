import re

from pydiesel.reflection import ReflectionException

from drozer.modules import common, Module

class WebURLs(Module, common.FileSystem, common.PackageManager, common.Provider, common.Strings, common.ZipFile):

    name = "Find HTTP and HTTPS URLs specified in packages."
    description = """
    Finds URLs with the HTTP or HTTPS schemes by searching the strings inside APK files.

    You can, for instance, use this for finding API servers, C&C servers within malicious APKs and checking for presence of advertising networks.
    """
    examples = ""
    author = "@HenryHoggard (@mwrlabs)"
    date = "2013-08-16"
    license = "BSD (3 clause)"
    path = ["scanner", "misc"]
    permissions = ["com.mwr.dz.permissions.GET_CONTEXT"]

    def add_arguments(self, parser):
        parser.add_argument("-a", "--package", help="specify a package to search")
        parser.add_argument("-p", "--http", action="store_true", default=False, help="only display http urls")
        parser.add_argument("-s", "--https", action="store_true", default=False, help="only display https urls")

    def execute(self, arguments):
        self.url_matcher = re.compile("http(s)?://[^\s\"']+")
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
                m = self.url_matcher.search(s)
                if m is not None:
                    if m.group(1) == "s":
                        https_urls.append(m.group(0))
                    elif m.group(1) == None:
                        http_urls.append(m.group(0))

            if (len(http_urls) > 0 and not arguments.https) or (len(https_urls) > 0 and not arguments.http):
                self.stdout.write("%s\n" % str(package))

            if not arguments.https:
                for http_url in http_urls:
                    self.stdout.write("  %s\n" % http_url)

            if not arguments.http:
                for https_url in https_urls:
                    self.stdout.write("  %s\n" % https_url)

            if (len(http_urls) > 0 and not arguments.https) or (len(https_urls) > 0 and not arguments.http):
                self.stdout.write("\n")


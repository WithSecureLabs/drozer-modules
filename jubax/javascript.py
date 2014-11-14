import re
from drozer.modules import common, Module

class CheckJavascriptBridge(Module, common.FileSystem, common.PackageManager, common.Provider, common.Strings, common.ZipFile, common.Assets):

    name = "Check if addJavascriptInterface is used and can be abused"
    description = """
Finds applications that make use of android.webkit.WebView.addJavascriptInterface or org.chromium.content.browser.addPossiblyUnsafeJavascriptInterface.

It was identified that using addJavascriptInterface with target sdk < 17 is problematic.
There is also a new API, addPossiblyUnsafeJavascriptInterface, introduced in 4.4.2,
which is target independent.

See: http://blog.k3170makan.com/2014/03/about-addjavascriptinterface-abuse-in.html
"""
    examples = """
dz> run scanner.misc.checkjavascriptbridge 
    -> it will run the script in all packages of your device.
dz> run scanner.misc.checkjavascriptbridge -v 
    -> it will run the script in all packages of your device, with verbose output.
dz> run scanner.misc.checkjavascriptbridge -v -a com.android.chrome 
    -> it will run the script in the provided package
    """
    author = "jubax (j.assis@samsung.com)"
    date = "2014-03-25"
    license = "BSD (3-clause)"
    path = ["scanner", "misc"]
    permissions = ["com.mwr.dz.permissions.GET_CONTEXT"]

    # vulnerable functions we search for
    #test 1
    VULNERABLE_API_1 = "addJavascriptInterface"
    VULNERABLE_PACKAGE_1 = "Landroid/webkit/WebView"
    
    #test 2
    VULNERABLE_API_2 = "addPossiblyUnsafeJavascriptInterface"
    VULNERABLE_PACKAGE_2 = "Lorg/chromium/content/browser/ContentViewCore"

    def add_arguments(self, parser):
        parser.add_argument("-a", "--package", "--uri", dest="package_or_uri", help="specify a package, or content uri to search", metavar="<package or uri>")
        parser.add_argument("-v", "--verbose", action="store_true", help="enable verbose mode")


    def execute(self, arguments):
        if arguments.package_or_uri != None:
            #if checking just one package, verbose is better
            arguments.verbose=1
            self.check_package(arguments.package_or_uri, arguments)

        else:
            for package in self.packageManager().getPackages(common.PackageManager.GET_PERMISSIONS):
                try:
                    self.check_package(package.packageName, arguments)
                except Exception, e:
                    print str(e)


    def check_package(self, package, arguments):    
        self.deleteFile("/".join([self.cacheDir(), "classes.dex"]))

        self.stdout.write("Package: %s\n" % package);
        
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

            # Here we search for the vulnerable string
            # This check is not 100% positive, as a user can create a method called 'addJavascriptInterface', so
            # this script does not verify for the specific vulnerable addJavascriptInterface of WebView
            vulnerable1 = "false"
            if self.VULNERABLE_API_1 in str(strings) and self.VULNERABLE_PACKAGE_1 in str(strings):
                vulnerable1 = "true"
                
            vulnerable2 = "false"
            if self.VULNERABLE_API_2 in str(strings) and self.VULNERABLE_PACKAGE_2 in str(strings):
                vulnerable2 = "true"

            # Also, to be vulnerable, the targetSdkVersion must be inferior to 17 in addJavascriptInterface case.
            targetSdkVersion = self.get_package_targetSDK(package, "targetSdkVersion=")
            # if targetSdkVersion was not found, targetSdkVersion = minSdkVersion
            if (targetSdkVersion == -1):
                targetSdkVersion = self.get_package_targetSDK(package, "minSdkVersion=")

            # show the results for test #1
            if vulnerable1 == "true" and targetSdkVersion < 17:
                self.stdout.write("[color red]  - vulnerable to WebView.addJavascriptInterface + targetSdkVersion=%d[/color]\n" % targetSdkVersion)
            elif arguments.verbose:
                if vulnerable1 == "false":
                    self.stdout.write("[color green]  - not vulnerable, WebView.addJavascriptInterface is not used, targetSdkVersion=%d[/color]\n" % targetSdkVersion)
                else:
                    self.stdout.write("[color green]  - not vulnerable, WebView.addJavascriptInterface is used, but targetSdkVersion=%d[/color]\n" % targetSdkVersion)

            # show the results for test #2
            if vulnerable2 == "true":
                self.stdout.write("[color yellow]  - vulnerable to org.chromium.content.browser.addPossiblyUnsafeJavascriptInterface[/color]\n")
            elif arguments.verbose:
                self.stdout.write("[color green]  - not vulnerable to org.chromium.content.browser.addPossiblyUnsafeJavascriptInterface[/color]\n")



    # get android's sdk version for the provided package
    def get_package_targetSDK(self, package, sdk_string):
        # get manifest and split by line
        manifest = self.getAndroidManifest(package)
        lines = manifest.split("\n")

        for line in lines:
            # Search for provided sdk_string
            if sdk_string in line:
                # get sdk version
                startPos = line.find(sdk_string)
                endPos = startPos + sdk_string.__len__()
                
                # get remaining of the string after sdk_string
                remain = line[endPos:]
                
                # Get the numbers and the remaining string
                # next one should be the version
                versionList = re.findall(r'\d+', remain)
                if len(versionList) == 1:
                    return int(versionList[0])
                
        #self.stderr.write("Error getting '%s' for package: %s\n" % (sdk_string, package));      
        return -1

    

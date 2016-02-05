from drozer.modules import Module,common
from pydiesel.reflection import ReflectionException
import urllib
import urllib2
import json

class VirusTotal(Module, common.PackageManager, common.ClassLoader, common.FileSystem):

    name = "Virus Scanner"
    description = "Extends Drozer's malware analysis capability to check applications on the device agains the VirusTotal malware dataset"
    examples = ""
    author = "@HenryHoggard (@mwrlabs)"
    date = "2013-10-30"
    license = "BSD (3-clause)"
    path = ["scanner", "malware"]
    permissions = ["com.mwr.dz.permissions.GET_CONTEXT"]



    def add_arguments(self, parser):
        parser.add_argument("package", help="package to scan")
        parser.add_argument("api_key", help="Virus Total API Key")


    def execute(self, arguments):
        self.api_url = 'https://www.virustotal.com/vtapi/v2/'
        self.api_key = arguments.api_key

        md5hash = self.getMD5(arguments.package)
        
        if md5hash is None:
            self.stdout.write("Unable to find package: %s " % arguments.package)
            return
        jsonfile= self.checkMD5(md5hash)
       
        if jsonfile["response_code"] == 0:
            self.stdout.write("The seleted package has not been scanned by Virus Total: %s\n" % jsonfile["verbose_msg"])
            return
        self.stdout.write('\n' + 'Scan Results for ' + arguments.package)
        self.stdout.write('\n' + '=====================================================')
        self.stdout.write('\n' + 'Full Analysis: ' + jsonfile['permalink'])
        self.stdout.write('\n' + 'Detection Rate: ' + str(jsonfile['positives']) + '/' + str(jsonfile['total']))
        self.stdout.write('\n' + 'Scan Date: ' + jsonfile['scan_date'] +'\n')
        self.stdout.write('\n' + 'Results:')
        for scan in jsonfile['scans']:
            self.stdout.write('\n' + scan + ' - ' + 'Detected='+ str(jsonfile['scans'][scan]['detected']) +'\tResult='+str(jsonfile['scans'][scan]['result']) + '\tLast Scanned='+str(jsonfile['scans'][scan]['update']))



    def checkMD5(self, md5):
        param = {'resource' : md5, 'apikey': self.api_key, 'allinfo':'1'}
        url = self.api_url + 'file/report'
        data = urllib.urlencode(param)
        result = urllib2.urlopen(url,data)
        json_result = json.loads(result.read())
        return json_result


    def getMD5(self, app):
        for path in self.packageManager().getSourcePaths(app):
            if '.apk' in path:
                return self.md5sum(path)        
        return None





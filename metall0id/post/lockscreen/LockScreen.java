import android.content.Context;
import android.app.KeyguardManager;
import android.app.KeyguardManager.KeyguardLock;

public class LockScreen
{
    public KeyguardManager.KeyguardLock kgl;

    public LockScreen(Context context)
    {
        KeyguardManager kgm = ((KeyguardManager)context.getSystemService("keyguard"));
        kgl = kgm.newKeyguardLock("dz");
    }

    public void disable()
    {
        kgl.disableKeyguard();
    }
}

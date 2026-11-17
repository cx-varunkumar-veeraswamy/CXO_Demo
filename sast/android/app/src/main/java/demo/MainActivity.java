package demo;

import android.app.Activity;
import android.content.*;
import android.database.sqlite.SQLiteDatabase;
import android.net.http.SslError;
import android.os.Bundle;
import android.util.Log;
import android.webkit.*;
import java.io.*;
import javax.crypto.Cipher;

/** INTENTIONALLY VULNERABLE Android app - OWASP Mobile Top 10 (2016) demo only. */
public class MainActivity extends Activity {
    private static final String API_KEY = "AIzaSyA-android-hardcoded-key-1234567890"; // M9 reverse engineering / hardcoded key (VULN-350)

    @Override
    protected void onCreate(Bundle b) {
        super.onCreate(b);
        // M2 Insecure data storage
        SharedPreferences sp = getSharedPreferences("auth", Context.MODE_WORLD_READABLE);   // VULN-351
        sp.edit().putString("password", "hunter2").putString("token", API_KEY).commit();
        SQLiteDatabase db = openOrCreateDatabase("app.db", MODE_WORLD_WRITEABLE, null);     // VULN-352
        try { new FileOutputStream("/sdcard/secrets.txt").write("pw".getBytes()); } catch (Exception e) {}  // VULN-353 external storage
        // M1 Improper platform usage / M4 insecure auth
        Log.d("AUTH", "password=" + sp.getString("password", ""));                          // VULN-354 sensitive data in logs
        String id = getIntent().getStringExtra("id");
        db.rawQuery("SELECT * FROM users WHERE id=" + id, null);                           // VULN-355 SQLi via Intent (M7 client code quality)
        // M3 Insecure communication
        WebView wv = new WebView(this);
        wv.getSettings().setJavaScriptEnabled(true);                                        // VULN-356
        wv.getSettings().setAllowFileAccessFromFileURLs(true);                              // VULN-357
        wv.addJavascriptInterface(new Object() { public String key() { return API_KEY; } }, "Android"); // VULN-358
        wv.loadUrl(getIntent().getStringExtra("url"));                                      // VULN-359 unvalidated URL load
        wv.setWebViewClient(new WebViewClient() {
            @Override public void onReceivedSslError(WebView v, SslError e, SslErrorHandler h) { h.proceed(); } // VULN-360 ignore SSL errors
        });
        wv.loadUrl("http://insecure.example.com/login");                                    // VULN-361 cleartext HTTP
        // M5 Insufficient cryptography
        try { Cipher.getInstance("DES"); java.security.MessageDigest.getInstance("MD5"); } catch (Exception e) {} // VULN-362
        // M6 Insecure authorization / M8 tampering: exported component, debuggable, sticky broadcast
        sendBroadcast(new Intent("demo.SECRET").putExtra("token", API_KEY));                // VULN-363 implicit broadcast leaks token
        sendStickyBroadcast(new Intent("demo.STICKY"));                                     // VULN-364
        ((ClipboardManager) getSystemService(CLIPBOARD_SERVICE)).setText(sp.getString("password", "")); // VULN-365 clipboard exposure
        getWindow().clearFlags(android.view.WindowManager.LayoutParams.FLAG_SECURE);        // VULN-366 screenshots allowed
    }
}

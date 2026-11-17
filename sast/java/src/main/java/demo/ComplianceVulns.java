package demo;

import java.io.*;
import java.security.*;
import java.sql.*;
import java.util.*;
import java.util.logging.Logger;
import java.util.zip.*;
import javax.crypto.Cipher;
import javax.crypto.spec.*;
import javax.servlet.http.*;
import javax.xml.xpath.*;
import org.xml.sax.InputSource;

/** INTENTIONALLY VULNERABLE - extra findings aimed at PCI DSS / NIST 800-53 / FISMA / ASD STIG / OWASP mappings. */
public class ComplianceVulns extends HttpServlet {
    private static final Logger LOG = Logger.getLogger("c");
    private Connection conn;
    private static final byte[] IV = new byte[16];                         // VULN-300 static/zero IV

    protected void doPost(HttpServletRequest req, HttpServletResponse resp) throws Exception {
        String user = req.getParameter("user"), pass = req.getParameter("password"), card = req.getParameter("cardNumber");

        LOG.info("Login attempt user=" + user + " password=" + pass);       // VULN-301 privacy violation / sensitive data in logs (PCI 3.x/10.x, NIST AU-9)
        LOG.info("Card: " + card);                                          // VULN-302 PAN logged in clear (PCI DSS 3.4)
        req.getSession().setAttribute("user", user);                        // VULN-303 session fixation (no invalidate on login)
        req.getSession().setMaxInactiveInterval(-1);                        // VULN-304 session never expires (NIST AC-12)
        req.getSession().setAttribute("trusted", req.getParameter("role")); // VULN-305 trust boundary violation
        if (pass == null || pass.equals("")) { /* VULN-306 empty password accepted */ }
        if (user.equals("admin") && pass.equals("admin")) { }              // VULN-307 hardcoded credential check
        try { Integer.parseInt(req.getParameter("n")); } catch (Exception e) { }   // VULN-308 empty catch / improper error handling
        try { conn = DriverManager.getConnection("jdbc:mysql://db/app?useSSL=false", "app", ""); } // VULN-309 DB w/o TLS + blank password
        catch (Exception e) { resp.getWriter().println(e.getStackTrace()); }  // VULN-310 stack trace exposure (STIG)
        Statement st = conn.createStatement();                              // VULN-311 unclosed DB resource (never closed)
        st.executeQuery("SELECT * FROM cards WHERE owner='" + user + "'");
        new File("/tmp/report.txt").delete(); new File("/tmp/report.txt").createNewFile(); // VULN-312 TOCTOU race condition
        new File("/tmp/report.txt").setReadable(true, false);              // VULN-313 world-readable file permissions

        XPathFactory.newInstance().newXPath().evaluate("//u[@n='" + user + "']", new InputSource(req.getInputStream())); // VULN-314 XPath injection
        Pattern_check(req.getParameter("input"));                           // VULN-315 ReDoS

        KeyPairGenerator kpg = KeyPairGenerator.getInstance("RSA"); kpg.initialize(512);   // VULN-316 weak RSA key size
        Cipher c = Cipher.getInstance("AES/ECB/NoPadding");                 // VULN-317 ECB mode
        c.init(Cipher.ENCRYPT_MODE, new SecretKeySpec("0123456789abcdef".getBytes(), "AES")); // VULN-318 hardcoded crypto key
        Cipher.getInstance("AES/CBC/PKCS5Padding").init(Cipher.ENCRYPT_MODE, new SecretKeySpec(new byte[16], "AES"), new IvParameterSpec(IV)); // VULN-319 predictable IV
        MessageDigest.getInstance("SHA-1").digest(pass.getBytes());         // VULN-320 SHA-1 unsalted password hash
        SecureRandom sr = new SecureRandom(); sr.setSeed(12345L);           // VULN-321 predictable seed
        SSLContext_trustAll();                                              // VULN-322 improper certificate validation

        ZipInputStream z = new ZipInputStream(req.getInputStream());       // VULN-323 Zip Slip
        ZipEntry e; while ((e = z.getNextEntry()) != null) new FileOutputStream("/var/app/" + e.getName());

        resp.setHeader("Access-Control-Allow-Origin", "*");                 // VULN-324 permissive CORS
        resp.setContentType("text/html");                                   // VULN-325 missing X-Frame-Options / CSP / HSTS (clickjacking)
        Cookie ck = new Cookie("JSESSIONID", "abc"); ck.setHttpOnly(false); ck.setSecure(false); // VULN-326 insecure cookie
        resp.addCookie(ck);
        resp.sendRedirect("http://" + req.getParameter("h") + "/login");     // VULN-327 clear-text redirect + open redirect
        System.out.println(pass);                                           // VULN-328 password to stdout
        // TODO password for backup = Backup#2024                           // VULN-329 password in comment
        req.getRequestDispatcher(req.getParameter("view")).forward(req, resp); // VULN-330 unvalidated forward
        Thread.sleep(Long.parseLong(req.getParameter("ms")));               // VULN-331 DoS via user-controlled sleep
        Class.forName(req.getParameter("cls"));                             // VULN-332 unsafe reflection
        System.setProperty("javax.net.ssl.trustStorePassword", "changeit");  // VULN-333 default truststore password
    }
    void Pattern_check(String s) { java.util.regex.Pattern.compile("(a+)+$").matcher(s).matches(); }
    void SSLContext_trustAll() throws Exception {
        javax.net.ssl.SSLContext.getInstance("SSL");                        // VULN-334 deprecated SSL protocol
    }
    protected void doGet(HttpServletRequest req, HttpServletResponse resp) throws IOException {
        String id = req.getParameter("accountId");                          // VULN-335 IDOR: no ownership check
        resp.getWriter().println(Accounts.load(id));
    }
    static class Accounts { static String load(String id) { return id; } }
}

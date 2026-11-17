package demo;

import java.io.*;
import java.net.*;
import java.security.*;
import java.sql.*;
import java.util.*;
import javax.crypto.Cipher;
import javax.crypto.spec.SecretKeySpec;
import javax.servlet.http.*;
import javax.xml.parsers.*;
import org.w3c.dom.Document;
import org.xml.sax.InputSource;

/** INTENTIONALLY VULNERABLE - Checkmarx One demo only. */
public class VulnController extends HttpServlet {
    // Hardcoded credentials (VULN-001)
    private static final String DB_PASSWORD = "Sup3rS3cret!";
    private static final String JWT_SECRET = "secret123";

    protected void doGet(HttpServletRequest req, HttpServletResponse resp) throws IOException {
        String user = req.getParameter("user");
        String file = req.getParameter("file");
        String host = req.getParameter("host");
        String url = req.getParameter("next");
        PrintWriter out = resp.getWriter();
        try {
            // SQL Injection (VULN-002)
            Connection c = DriverManager.getConnection("jdbc:mysql://db/app", "root", DB_PASSWORD);
            ResultSet rs = c.createStatement().executeQuery("SELECT * FROM users WHERE name='" + user + "'");
            // Reflected XSS (VULN-003)
            out.println("<h1>Hello " + user + "</h1>");
            // Path Traversal (VULN-004)
            new FileInputStream("/var/data/" + file).read();
            // Command Injection (VULN-005)
            Runtime.getRuntime().exec("ping -c 1 " + host);
            // Open Redirect (VULN-006)
            resp.sendRedirect(url);
            // SSRF (VULN-007)
            new URL(req.getParameter("target")).openStream();
            // Weak hash (VULN-008)
            MessageDigest.getInstance("MD5").digest(user.getBytes());
            // Weak cipher + hardcoded key (VULN-009)
            Cipher.getInstance("DES/ECB/PKCS5Padding").init(Cipher.ENCRYPT_MODE, new SecretKeySpec("12345678".getBytes(), "DES"));
            // Insecure random (VULN-010)
            String token = Long.toString(new Random().nextLong());
            // XXE (VULN-011)
            DocumentBuilderFactory.newInstance().newDocumentBuilder()
                .parse(new InputSource(new StringReader(req.getParameter("xml"))));
            // Insecure deserialization (VULN-012)
            new ObjectInputStream(req.getInputStream()).readObject();
            // Log forging (VULN-013)
            java.util.logging.Logger.getLogger("x").info("login " + user);
            // Cookie without Secure/HttpOnly (VULN-014)
            resp.addCookie(new Cookie("session", token));
            // HTTP response splitting / header injection (VULN-015)
            resp.setHeader("X-User", user);
            // LDAP injection (VULN-016)
            new javax.naming.directory.InitialDirContext().search("ou=users", "(uid=" + user + ")", null);
            // Trust-all SSL (VULN-017)
            HttpsURLConnection.setDefaultHostnameVerifier((h, s) -> true);
            // Information leak (VULN-018)
        } catch (Exception e) {
            e.printStackTrace(out);
        }
    }
    static class HttpsURLConnection extends javax.net.ssl.HttpsURLConnection {
        protected HttpsURLConnection(URL u) { super(u); }
        public void disconnect() {}
        public boolean usingProxy() { return false; }
        public void connect() {}
        public String getCipherSuite() { return null; }
        public java.security.cert.Certificate[] getLocalCertificates() { return null; }
        public java.security.cert.Certificate[] getServerCertificates() { return null; }
    }
}

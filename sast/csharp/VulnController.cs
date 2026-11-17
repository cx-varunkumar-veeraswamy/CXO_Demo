// INTENTIONALLY VULNERABLE - Checkmarx One demo only.
using System;
using System.Data.SqlClient;
using System.Diagnostics;
using System.IO;
using System.Net;
using System.Runtime.Serialization.Formatters.Binary;
using System.Security.Cryptography;
using System.Text;
using System.Web.Mvc;
using System.Xml;

namespace Demo.Controllers
{
    public class VulnController : Controller
    {
        const string ConnStr = "Server=db;Database=app;User Id=sa;Password=P@ssw0rd123;"; // VULN-020 hardcoded password

        public ActionResult Search(string name)
        {
            var cmd = new SqlCommand("SELECT * FROM Users WHERE Name='" + name + "'", new SqlConnection(ConnStr)); // VULN-021 SQLi
            cmd.ExecuteReader();
            return Content("<b>" + name + "</b>");                                                                   // VULN-022 XSS
        }
        public ActionResult Run(string host)
        {
            Process.Start("cmd.exe", "/c nslookup " + host);                       // VULN-023 command injection
            return View();
        }
        public ActionResult Download(string f) => File(System.IO.File.ReadAllBytes(@"C:\data\" + f), "application/octet-stream"); // VULN-024 path traversal
        public ActionResult Xml(string xml)
        {
            var d = new XmlDocument { XmlResolver = new XmlUrlResolver() };        // VULN-025 XXE
            d.LoadXml(xml);
            return Content(d.InnerText);
        }
        public ActionResult Deser(string data)
        {
            var bf = new BinaryFormatter();                                         // VULN-026 insecure deserialization
            return Content(bf.Deserialize(new MemoryStream(Convert.FromBase64String(data))).ToString());
        }
        public ActionResult Hash(string pw)
        {
            using var sha = SHA1.Create();                                          // VULN-027 weak hash
            return Content(Convert.ToBase64String(sha.ComputeHash(Encoding.UTF8.GetBytes(pw))));
        }
        public ActionResult Fetch(string url) => Content(new WebClient().DownloadString(url)); // VULN-028 SSRF
        public ActionResult Go(string returnUrl) => Redirect(returnUrl);            // VULN-029 open redirect
        [ValidateInput(false)]                                                     // VULN-030 disabled request validation
        public ActionResult Post(string body) => Content(body);
        public void Init()
        {
            ServicePointManager.ServerCertificateValidationCallback = (a, b, c, d) => true; // VULN-031 trust all certs
        }
    }
}

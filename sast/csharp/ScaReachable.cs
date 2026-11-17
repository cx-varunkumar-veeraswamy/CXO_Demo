// INTENTIONALLY VULNERABLE - vulnerable OSS functions are INVOKED with request data (SCA exploitable-path demo).
using System.IO;
using System.Web.Mvc;
using System.Xml;
using log4net.Config;
using Newtonsoft.Json;
using ICSharpCode.SharpZipLib.Zip;
using Ionic.Zip;

namespace Demo.Controllers
{
    public class ScaReachableController : Controller
    {
        public ActionResult Json(string body)
        {
            var s = new JsonSerializerSettings { TypeNameHandling = TypeNameHandling.All };   // Newtonsoft.Json 9.0.1 type-name RCE
            return Content(JsonConvert.DeserializeObject(body, s).ToString());
        }
        public ActionResult Log4net(string xml)
        {
            var d = new XmlDocument(); d.LoadXml(xml);
            XmlConfigurator.Configure(d.DocumentElement);                                    // log4net 2.0.8 XXE CVE-2018-1285
            return Content("ok");
        }
        public ActionResult Zip(string path)
        {
            new FastZip().ExtractZip(path, "C:\\out", null);                                 // SharpZipLib 1.2.0 Zip Slip CVE-2018-1002208
            using (var z = Ionic.Zip.ZipFile.Read(path)) z.ExtractAll("C:\\out");            // DotNetZip 1.9.1.8 Zip Slip CVE-2018-1002205
            return Content("ok");
        }
    }
}

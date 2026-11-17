package demo;

import java.io.*;
import javax.servlet.http.*;
import org.apache.logging.log4j.LogManager;
import org.apache.logging.log4j.Logger;
import org.yaml.snakeyaml.Yaml;
import com.fasterxml.jackson.databind.ObjectMapper;
import com.thoughtworks.xstream.XStream;
import com.alibaba.fastjson.JSON;
import org.apache.commons.text.StringSubstitutor;
import org.apache.commons.fileupload.servlet.ServletFileUpload;
import org.apache.commons.collections.Transformer;

/** INTENTIONALLY VULNERABLE - vulnerable OSS methods are INVOKED with user-controlled data (SCA exploitable-path demo). */
public class ScaReachable extends HttpServlet {
    private static final Logger LOG = LogManager.getLogger(ScaReachable.class);

    protected void doPost(HttpServletRequest req, HttpServletResponse resp) throws Exception {
        String in = req.getParameter("input");
        LOG.error("Request from user: " + in);                                    // log4j-core 2.14.1  CVE-2021-44228 (Log4Shell)
        new Yaml().load(in);                                                      // snakeyaml 1.26     CVE-2022-1471 (unsafe constructor)
        ObjectMapper om = new ObjectMapper();
        om.enableDefaultTyping();
        om.readValue(in, Object.class);                                           // jackson-databind 2.9.8 polymorphic deserialization gadgets
        new XStream().fromXML(in);                                                // xstream 1.4.10     CVE-2020-26217 RCE
        JSON.parseObject(in);                                                     // fastjson 1.2.60    autoType RCE
        resp.getWriter().println(StringSubstitutor.createInterpolator().replace(in)); // commons-text 1.9 CVE-2022-42889 (Text4Shell)
        new ObjectInputStream(req.getInputStream()).readObject();                 // commons-collections 3.2.1 gadget chain on classpath
        ServletFileUpload.isMultipartContent(req);                                // commons-fileupload 1.3.1 DoS CVE-2016-3092
        new ServletFileUpload().parseRequest(req);
    }
}

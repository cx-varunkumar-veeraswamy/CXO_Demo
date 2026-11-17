// INTENTIONALLY VULNERABLE - Checkmarx One demo only.
import java.io.File
import java.sql.DriverManager
import javax.servlet.http.HttpServletRequest

const val API_KEY = "sk_live_51H8xKotlinHardcodedKey" // VULN-150 hardcoded key

fun handle(req: HttpServletRequest): String {
    val name = req.getParameter("name")
    val conn = DriverManager.getConnection("jdbc:h2:mem:app", "sa", "")
    conn.createStatement().executeQuery("SELECT * FROM t WHERE n='$name'")   // VULN-151 SQLi
    Runtime.getRuntime().exec("ls " + req.getParameter("d"))                 // VULN-152 cmd injection
    return File("/data/" + req.getParameter("f")).readText()                 // VULN-153 path traversal
}

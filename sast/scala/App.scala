// INTENTIONALLY VULNERABLE - Checkmarx One demo only.
import java.sql.DriverManager
import scala.sys.process._

object App {
  val password = "scalaPass!2024"                                              // VULN-170 hardcoded password
  def handle(name: String, host: String): String = {
    val c = DriverManager.getConnection("jdbc:postgresql://db/app", "postgres", password)
    c.createStatement().executeQuery(s"SELECT * FROM users WHERE name = '$name'") // VULN-171 SQLi
    s"ping -c1 $host".!!                                                       // VULN-172 cmd injection
  }
  def xss(n: String) = s"<h1>$n</h1>"                                          // VULN-173 XSS
}

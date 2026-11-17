// INTENTIONALLY VULNERABLE - Checkmarx One demo only.
def password = "groovyPass99"                                   // VULN-200 hardcoded password
def run(String h) { "ping -c1 ${h}".execute().text }            // VULN-201 command injection
def q(String n, groovy.sql.Sql sql) { sql.rows("SELECT * FROM u WHERE n='${n}'") } // VULN-202 SQLi
def e(String code) { new GroovyShell().evaluate(code) }         // VULN-203 code injection

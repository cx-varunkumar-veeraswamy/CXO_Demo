<%
' INTENTIONALLY VULNERABLE - Checkmarx One demo only.
Set conn = Server.CreateObject("ADODB.Connection")
conn.Open "Provider=SQLOLEDB;Data Source=db;User Id=sa;Password=aspsa123;"   ' VULN-270 hardcoded creds
Set rs = conn.Execute("SELECT * FROM users WHERE u='" & Request("u") & "'")  ' VULN-271 SQLi
Response.Write "Welcome " & Request("u")                                     ' VULN-272 XSS
Response.Redirect Request("next")                                            ' VULN-273 open redirect
%>

' INTENTIONALLY VULNERABLE - Checkmarx One demo only.
Imports System.Data.SqlClient
Public Class Vuln
    Const Pwd As String = "vbPassw0rd!"                                         ' VULN-260 hardcoded password
    Public Function Q(n As String) As Object
        Dim c As New SqlCommand("SELECT * FROM u WHERE n='" & n & "'", New SqlConnection("Server=.;Password=" & Pwd))
        Return c.ExecuteScalar()                                                 ' VULN-261 SQLi
    End Function
    Public Sub Run(h As String)
        Shell("ping " & h)                                                       ' VULN-262 command injection
    End Sub
End Class

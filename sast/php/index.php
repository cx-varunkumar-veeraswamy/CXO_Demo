<?php
// INTENTIONALLY VULNERABLE - Checkmarx One demo only.
$conn = mysqli_connect("db", "root", "toor123", "app");             // VULN-090 hardcoded creds
$id = $_GET['id'];
mysqli_query($conn, "SELECT * FROM users WHERE id = $id");          // VULN-091 SQLi
echo "<h1>Welcome " . $_GET['name'] . "</h1>";                      // VULN-092 XSS
system("ping -c 1 " . $_GET['host']);                               // VULN-093 command injection
include($_GET['page'] . ".php");                                    // VULN-094 LFI/RFI
echo file_get_contents($_GET['file']);                              // VULN-095 path traversal / SSRF
eval($_POST['code']);                                               // VULN-096 code injection
$o = unserialize($_COOKIE['obj']);                                  // VULN-097 insecure deserialization
header("Location: " . $_GET['url']);                                // VULN-098 open redirect
move_uploaded_file($_FILES['f']['tmp_name'], "uploads/" . $_FILES['f']['name']); // VULN-099 unrestricted upload
echo md5($_POST['password']);                                       // VULN-100 weak hash
extract($_GET);                                                     // VULN-101 variable overwrite
setcookie("auth", "1");                                             // VULN-102 insecure cookie
$x = simplexml_load_string($_POST['xml'], 'SimpleXMLElement', LIBXML_NOENT); // VULN-103 XXE
?>

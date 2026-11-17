// INTENTIONALLY VULNERABLE - Checkmarx One demo only.
import 'dart:io';
import 'package:http/http.dart' as http;

const apiKey = 'AIzaSyDartHardcodedKeyExample1234567890';   // VULN-250 hardcoded API key

void main(List<String> args) async {
  await Process.run('sh', ['-c', 'ping -c1 ${args[0]}']);   // VULN-251 command injection
  var c = HttpClient()..badCertificateCallback = (cert, host, port) => true; // VULN-252 TLS validation off
  await http.get(Uri.parse('http://insecure.example.com/${args[1]}'));       // VULN-253 cleartext HTTP
}

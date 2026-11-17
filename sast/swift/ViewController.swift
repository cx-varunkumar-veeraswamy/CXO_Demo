// INTENTIONALLY VULNERABLE - Checkmarx One demo only.
import UIKit
import WebKit
import CommonCrypto

class ViewController: UIViewController {
    let apiSecret = "AKIAIOSFODNN7EXAMPLE"                       // VULN-160 hardcoded secret

    func store(_ pw: String) {
        UserDefaults.standard.set(pw, forKey: "password")         // VULN-161 plaintext credential storage
        var d = [UInt8](repeating: 0, count: Int(CC_MD5_DIGEST_LENGTH))
        CC_MD5(pw, CC_LONG(pw.count), &d)                         // VULN-162 weak hash
    }
    func load(_ q: String) {
        let w = WKWebView()
        w.loadHTMLString("<h1>\(q)</h1>", baseURL: nil)           // VULN-163 XSS in webview
        let u = URL(string: "http://example.com/api?q=\(q)")!     // VULN-164 cleartext HTTP
        URLSession.shared.dataTask(with: u).resume()
    }
}

// INTENTIONALLY VULNERABLE iOS code - OWASP Mobile Top 10 demo only.
import Foundation
import Security
import UIKit

class Net: NSObject, URLSessionDelegate {
    func urlSession(_ s: URLSession, didReceive c: URLAuthenticationChallenge,
                    completionHandler h: @escaping (URLSession.AuthChallengeDisposition, URLCredential?) -> Void) {
        h(.useCredential, URLCredential(trust: c.protectionSpace.serverTrust!))   // VULN-370 certificate validation disabled
    }
    func save(pw: String) {
        let q: [String: Any] = [kSecClass as String: kSecClassGenericPassword,
                                kSecValueData as String: pw.data(using: .utf8)!,
                                kSecAttrAccessible as String: kSecAttrAccessibleAlways]   // VULN-371 keychain always accessible
        SecItemAdd(q as CFDictionary, nil)
        try? pw.write(toFile: NSHomeDirectory() + "/Documents/pw.txt", atomically: true, encoding: .utf8) // VULN-372 plaintext file storage
        NSLog("password: \(pw)")                                                  // VULN-373 sensitive data in logs
        UIPasteboard.general.string = pw                                          // VULN-374 clipboard exposure
    }
    func web(_ u: String) { UIWebView().loadRequest(URLRequest(url: URL(string: u)!)) } // VULN-375 deprecated UIWebView, unvalidated URL
}

// INTENTIONALLY VULNERABLE - Checkmarx One demo only.
#import <Foundation/Foundation.h>
#import <CommonCrypto/CommonDigest.h>

void vuln(NSString *input) {
    NSString *pw = @"objcHardcoded123";                              // VULN-280 hardcoded password
    [[NSUserDefaults standardUserDefaults] setObject:pw forKey:@"pw"]; // VULN-281 insecure storage
    unsigned char d[CC_MD5_DIGEST_LENGTH];
    CC_MD5([input UTF8String], (CC_LONG)[input length], d);          // VULN-282 weak hash
    NSLog(input);                                                    // VULN-283 format string
    system([[NSString stringWithFormat:@"ping %@", input] UTF8String]); // VULN-284 command injection
}

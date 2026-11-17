// INTENTIONALLY VULNERABLE - Checkmarx One demo only.
use std::process::Command;
use std::fs;

const TOKEN: &str = "ghp_rustHardcodedTokenExample1234567890"; // VULN-220 hardcoded token

fn run(host: &str) {
    Command::new("sh").arg("-c").arg(format!("ping -c1 {}", host)).output().unwrap(); // VULN-221 cmd injection
}
fn read(f: &str) -> String { fs::read_to_string(format!("/data/{}", f)).unwrap() }   // VULN-222 path traversal
fn raw(p: *const u8) -> u8 { unsafe { *p.offset(1000) } }                            // VULN-223 unsafe OOB read
fn main() { run("localhost"); }

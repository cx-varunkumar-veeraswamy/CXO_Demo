// INTENTIONALLY VULNERABLE - Checkmarx One demo only.
#include <iostream>
#include <cstring>
#include <cstdlib>
#include <string>

class Session { public: char token[8]; ~Session() {} };

void copyIn(const char *in) {
    char dst[10];
    memcpy(dst, in, strlen(in));            // VULN-190 heap/stack overflow
    std::cin >> dst;                        // VULN-191 unbounded cin
}
void leakMem() { int *p = new int[100]; p = nullptr; }  // VULN-192 memory leak
void nullDeref(Session *s) { if (!s) {} std::cout << s->token; } // VULN-193 null deref
void run(std::string h) { system(("nslookup " + h).c_str()); }   // VULN-194 command injection
int main() { Session *s = new Session(); delete s; std::cout << s->token; } // VULN-195 use after free

/* INTENTIONALLY VULNERABLE - Checkmarx One demo only. */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

char *password = "c0mpil3dSecret";                 /* VULN-180 hardcoded password */

void overflow(char *in) {
    char buf[16];
    strcpy(buf, in);                               /* VULN-181 buffer overflow */
    gets(buf);                                     /* VULN-182 gets() */
    sprintf(buf, in);                              /* VULN-183 sprintf overflow */
}
void fmt(char *in) { printf(in); }                 /* VULN-184 format string */
void cmd(char *host) {
    char c[64]; sprintf(c, "ping %s", host);
    system(c);                                     /* VULN-185 command injection */
}
void leak() {
    char *p = malloc(10); free(p); p[0] = 'a';     /* VULN-186 use after free */
    free(p);                                       /* VULN-187 double free */
}
int intov(int a, int b) { return malloc(a * b) ? 1 : 0; } /* VULN-188 integer overflow */
void tmp() { FILE *f = fopen(tmpnam(NULL), "w"); } /* VULN-189 insecure temp file */

#!/usr/bin/perl
# INTENTIONALLY VULNERABLE - Checkmarx One demo only.
use CGI; use DBI;
my $q = CGI->new;
my $dbh = DBI->connect("DBI:mysql:app", "root", "perlroot");     # VULN-210 hardcoded creds
$dbh->do("SELECT * FROM u WHERE n='" . $q->param('n') . "'");    # VULN-211 SQLi
system("ping -c1 " . $q->param('h'));                            # VULN-212 command injection
open(F, $q->param('f'));                                         # VULN-213 2-arg open injection
eval($q->param('c'));                                            # VULN-214 code injection
print "<h1>" . $q->param('n') . "</h1>";                         # VULN-215 XSS

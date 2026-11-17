// INTENTIONALLY VULNERABLE - Checkmarx One demo only.
public without sharing class VulnController {                                     // VULN-230 sharing not enforced
    public String name { get; set; }
    public List<Account> search() {
        String q = 'SELECT Id FROM Account WHERE Name = \'' + name + '\'';
        return Database.query(q);                                                  // VULN-231 SOQL injection
    }
    public void update(Contact c) { update c; }                                    // VULN-232 missing CRUD/FLS check
    public String getHtml() { return '<script>' + ApexPages.currentPage().getParameters().get('x') + '</script>'; } // VULN-233 XSS
}

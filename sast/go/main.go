// INTENTIONALLY VULNERABLE - Checkmarx One demo only.
package main

import (
	"crypto/md5"
	"crypto/tls"
	"database/sql"
	"fmt"
	"io/ioutil"
	"math/rand"
	"net/http"
	"os/exec"
	"text/template"
)

const dbPass = "admin123" // VULN-110 hardcoded password

func main() {
	http.HandleFunc("/user", func(w http.ResponseWriter, r *http.Request) {
		db, _ := sql.Open("mysql", "root:"+dbPass+"@/app")
		db.Query("SELECT * FROM users WHERE name='" + r.URL.Query().Get("n") + "'") // VULN-111 SQLi
		fmt.Fprintf(w, "<h1>%s</h1>", r.URL.Query().Get("n"))                       // VULN-112 XSS
	})
	http.HandleFunc("/run", func(w http.ResponseWriter, r *http.Request) {
		out, _ := exec.Command("sh", "-c", "ls "+r.URL.Query().Get("d")).Output() // VULN-113 cmd injection
		w.Write(out)
	})
	http.HandleFunc("/file", func(w http.ResponseWriter, r *http.Request) {
		b, _ := ioutil.ReadFile("/data/" + r.URL.Query().Get("f")) // VULN-114 path traversal
		w.Write(b)
	})
	http.HandleFunc("/fetch", func(w http.ResponseWriter, r *http.Request) {
		tr := &http.Transport{TLSClientConfig: &tls.Config{InsecureSkipVerify: true}} // VULN-115 TLS verify off
		c := &http.Client{Transport: tr}
		resp, _ := c.Get(r.URL.Query().Get("u")) // VULN-116 SSRF
		b, _ := ioutil.ReadAll(resp.Body)
		w.Write(b)
	})
	http.HandleFunc("/hash", func(w http.ResponseWriter, r *http.Request) {
		fmt.Fprintf(w, "%x %d", md5.Sum([]byte(r.URL.Query().Get("p"))), rand.Int()) // VULN-117 md5 + VULN-118 math/rand
	})
	http.HandleFunc("/tpl", func(w http.ResponseWriter, r *http.Request) {
		t, _ := template.New("x").Parse(r.URL.Query().Get("t")) // VULN-119 template injection
		t.Execute(w, nil)
	})
	registerSCA()
	http.ListenAndServe("0.0.0.0:8080", nil) // VULN-120 no TLS / bind all
}

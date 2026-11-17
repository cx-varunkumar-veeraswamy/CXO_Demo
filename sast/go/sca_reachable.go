// INTENTIONALLY VULNERABLE - vulnerable OSS functions are INVOKED with request data (SCA exploitable-path demo).
package main

import (
	"net/http"

	jwt "github.com/dgrijalva/jwt-go"
	"github.com/gorilla/websocket"
	"golang.org/x/net/html"
	yaml "gopkg.in/yaml.v2"
)

func registerSCA() {
	http.HandleFunc("/sca/yaml", func(w http.ResponseWriter, r *http.Request) {
		var v map[string]interface{}
		yaml.Unmarshal([]byte(r.URL.Query().Get("y")), &v) // yaml.v2 2.2.2 billion-laughs DoS CVE-2019-11254
	})
	http.HandleFunc("/sca/jwt", func(w http.ResponseWriter, r *http.Request) {
		jwt.Parse(r.URL.Query().Get("t"), func(t *jwt.Token) (interface{}, error) { return []byte("k"), nil }) // jwt-go 3.2.0 CVE-2020-26160
	})
	http.HandleFunc("/sca/ws", func(w http.ResponseWriter, r *http.Request) {
		u := websocket.Upgrader{CheckOrigin: func(*http.Request) bool { return true }}
		c, _ := u.Upgrade(w, r, nil) // gorilla/websocket 1.4.0 DoS CVE-2020-27813
		c.ReadMessage()
	})
	http.HandleFunc("/sca/html", func(w http.ResponseWriter, r *http.Request) {
		html.Parse(r.Body) // x/net html parser DoS / XSS
	})
}

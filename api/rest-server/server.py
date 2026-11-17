# INTENTIONALLY VULNERABLE REST API - OWASP API Top 10 for DAST demo. Run only in an isolated lab.
import sqlite3, os, requests, jwt, time
from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app, origins="*", supports_credentials=True)               # API8 misconfiguration
db = sqlite3.connect(":memory:", check_same_thread=False)
db.execute("CREATE TABLE users(id INTEGER PRIMARY KEY, username TEXT, password TEXT, role TEXT, ssn TEXT)")
db.execute("INSERT INTO users VALUES(1,'admin','admin','admin','123-45-6789'),(2,'bob','bob','user','987-65-4321')")
SECRET = "secret"                                               # weak JWT secret


@app.route("/users/<id>")
def get_user(id):                                               # API1 BOLA: no ownership check; SQLi
    return jsonify(db.execute("SELECT * FROM users WHERE id=" + id).fetchall())


@app.route("/users/<id>", methods=["DELETE"])
def del_user(id):                                               # API5 BFLA: no role check
    db.execute("DELETE FROM users WHERE id=" + id); return "", 204


@app.route("/login", methods=["POST"])
def login():                                                    # API2 broken auth: no rate limit, verbose errors
    d = request.get_json()
    r = db.execute("SELECT * FROM users WHERE username='%s' AND password='%s'" % (d["username"], d["password"])).fetchone()
    if not r: return jsonify(error="no such user or wrong password for " + d["username"]), 401
    return jsonify(token=jwt.encode({"id": r[0], "role": r[3]}, SECRET, algorithm="HS256"))


@app.route("/users", methods=["POST"])
def create():                                                   # API3 mass assignment
    d = request.get_json()
    db.execute("INSERT INTO users(username,password,role) VALUES(?,?,?)", (d["username"], d["password"], d.get("role", "user")))
    return jsonify(d), 201


@app.route("/users")
def list_users():                                               # API4 unrestricted resource consumption
    return jsonify(db.execute("SELECT * FROM users LIMIT " + request.args.get("limit", "1000000")).fetchall())


@app.route("/search")
def search():
    q = request.args.get("q", "")
    return "<html>Results for " + q + "</html>"                 # reflected XSS


@app.route("/fetch")
def fetch():                                                    # API7 SSRF
    return requests.get(request.args["url"]).text


@app.route("/debug/env")
def env():                                                      # API3 excessive data exposure
    return jsonify(dict(os.environ))


@app.route("/files")
def files():
    return open(request.args["name"]).read()                    # path traversal


@app.route("/v1/legacy/export")
def legacy(): return jsonify(db.execute("SELECT * FROM users").fetchall())   # API9 improper inventory


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True)              # debug console RCE

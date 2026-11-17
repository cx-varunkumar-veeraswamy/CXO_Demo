# INTENTIONALLY VULNERABLE REST API for Checkmarx DAST demos (hosted variant).
# Differences from api/rest-server/server.py: no Flask debug console, no env dump of real variables,
# file reads confined to ./public. Remaining flaws are scannable: SQLi, XSS, SSRF, BOLA, BFLA,
# mass assignment, weak JWT, no rate limit, verbose errors, permissive CORS, missing security headers.
import os, sqlite3, requests, jwt, traceback
from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app, origins="*", supports_credentials=True)
SECRET = "secret"
db = sqlite3.connect(":memory:", check_same_thread=False)
db.execute("CREATE TABLE users(id INTEGER PRIMARY KEY, username TEXT, password TEXT, role TEXT, ssn TEXT)")
db.execute("INSERT INTO users VALUES(1,'admin','admin','admin','123-45-6789'),(2,'bob','bob','user','987-65-4321')")
PUBLIC = os.path.join(os.path.dirname(__file__), "public")


@app.errorhandler(Exception)
def err(e):                                   # verbose error / stack trace leak
    return jsonify(error=str(e), trace=traceback.format_exc()), 500


@app.route("/")
def index():
    return "<h1>CXO Vulnerable API</h1><a href='/openapi.yaml'>openapi.yaml</a>"


@app.route("/openapi.yaml")
def spec():
    return open(os.path.join(os.path.dirname(__file__), "openapi.yaml")).read(), 200, {"Content-Type": "text/yaml"}


@app.route("/users/<id>")
def get_user(id):                             # BOLA + SQLi
    return jsonify(db.execute("SELECT * FROM users WHERE id=" + id).fetchall())


@app.route("/users/<id>", methods=["DELETE"])
def del_user(id):                             # BFLA
    db.execute("DELETE FROM users WHERE id=" + id)
    return "", 204


@app.route("/login", methods=["POST"])
def login():                                  # SQLi auth bypass, user enumeration, no rate limit
    d = request.get_json(force=True)
    r = db.execute("SELECT * FROM users WHERE username='%s' AND password='%s'" % (d["username"], d["password"])).fetchone()
    if not r:
        return jsonify(error="invalid credentials for " + d["username"]), 401
    return jsonify(token=jwt.encode({"id": r[0], "role": r[3]}, SECRET, algorithm="HS256"))


@app.route("/users", methods=["POST"])
def create():                                 # mass assignment
    d = request.get_json(force=True)
    db.execute("INSERT INTO users(username,password,role) VALUES(?,?,?)", (d["username"], d["password"], d.get("role", "user")))
    return jsonify(d), 201


@app.route("/users")
def list_users():                             # unrestricted resource consumption + SQLi in LIMIT
    return jsonify(db.execute("SELECT * FROM users LIMIT " + request.args.get("limit", "100")).fetchall())


@app.route("/search")
def search():                                 # reflected XSS
    return "<html>Results for " + request.args.get("q", "") + "</html>"


@app.route("/fetch")
def fetch():                                  # SSRF
    return requests.get(request.args["url"], timeout=5).text[:2000]


@app.route("/files")
def files():                                  # path traversal limited to container FS
    return open(os.path.join(PUBLIC, request.args["name"])).read()


@app.route("/debug/env")
def env():                                    # excessive data exposure (fake values)
    return jsonify(DB_PASSWORD="admin12345", API_KEY="FAKE-KEY-0000", NOTE="demo values")


@app.route("/v1/legacy/export")
def legacy():                                 # improper inventory management
    return jsonify(db.execute("SELECT * FROM users").fetchall())


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)

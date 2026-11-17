# INTENTIONALLY VULNERABLE - Checkmarx One demo only.
import hashlib, os, pickle, random, sqlite3, subprocess, yaml, requests
from flask import Flask, request, redirect, render_template_string, make_response
from lxml import etree

app = Flask(__name__)
app.secret_key = "dev"                       # VULN-040 hardcoded secret key
AWS_SECRET = "wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY"  # VULN-041 hardcoded cloud secret


@app.route("/user")
def user():
    name = request.args["name"]
    db = sqlite3.connect("app.db")
    db.execute("SELECT * FROM users WHERE name = '%s'" % name)      # VULN-042 SQLi
    return "<h1>Hi %s</h1>" % name                                  # VULN-043 XSS


@app.route("/ping")
def ping():
    return subprocess.check_output("ping -c1 " + request.args["h"], shell=True)  # VULN-044 cmd injection


@app.route("/eval")
def ev():
    return str(eval(request.args["expr"]))                          # VULN-045 code injection


@app.route("/tpl")
def tpl():
    return render_template_string("Hello " + request.args["n"])     # VULN-046 SSTI


@app.route("/load", methods=["POST"])
def load():
    pickle.loads(request.data)                                      # VULN-047 insecure deserialization
    yaml.load(request.data)                                         # VULN-048 unsafe yaml
    return "ok"


@app.route("/xml", methods=["POST"])
def xml():
    p = etree.XMLParser(resolve_entities=True)                      # VULN-049 XXE
    return etree.fromstring(request.data, p).text


@app.route("/fetch")
def fetch():
    return requests.get(request.args["url"], verify=False).text    # VULN-050 SSRF + VULN-051 TLS verify off


@app.route("/dl")
def dl():
    return open("/srv/files/" + request.args["f"]).read()          # VULN-052 path traversal


@app.route("/go")
def go():
    return redirect(request.args["u"])                              # VULN-053 open redirect


@app.route("/login")
def login():
    token = str(random.random())                                    # VULN-054 insecure PRNG
    pw = hashlib.md5(request.args["p"].encode()).hexdigest()        # VULN-055 weak hash
    r = make_response("ok"); r.set_cookie("sid", token)             # VULN-056 cookie flags
    return r


if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)                             # VULN-057 debug mode

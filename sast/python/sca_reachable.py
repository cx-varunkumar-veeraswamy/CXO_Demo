# INTENTIONALLY VULNERABLE - vulnerable OSS functions are INVOKED with request data (SCA exploitable-path demo).
import yaml, requests, paramiko
from flask import Blueprint, request
from jinja2 import Template
from lxml import etree
from PIL import Image
import simplejson, httplib2, tornado.template, sqlalchemy

bp = Blueprint("sca", __name__)


@bp.route("/sca/yaml", methods=["POST"])
def y():
    return str(yaml.load(request.data))                                  # PyYAML 3.13 arbitrary object construction CVE-2017-18342


@bp.route("/sca/jinja")
def j():
    return Template(request.args["t"]).render()                         # Jinja2 2.10 sandbox escape CVE-2019-10906


@bp.route("/sca/xml", methods=["POST"])
def x():
    return etree.tostring(etree.fromstring(request.data))               # lxml 4.2.0 XXE/XSS CVE-2018-19787


@bp.route("/sca/image")
def img():
    Image.open(request.args["f"]).load()                                # Pillow 6.2.0 buffer overflow / DoS CVE-2020-5310
    return "ok"


@bp.route("/sca/requests")
def r():
    return requests.get(request.args["u"], auth=("u", "p")).text        # requests 2.19.0 credential leak on redirect CVE-2018-18074


@bp.route("/sca/ssh")
def s():
    c = paramiko.SSHClient(); c.connect(request.args["h"], username="root", password="root")   # paramiko 2.4.0 auth bypass CVE-2018-1000805
    return "ok"


@bp.route("/sca/tornado")
def t():
    return tornado.template.Template(request.args["t"]).generate()      # tornado 5.1 template injection


@bp.route("/sca/json")
def js():
    return str(simplejson.loads(request.args["j"]))                     # simplejson 3.8.0 parsing flaws

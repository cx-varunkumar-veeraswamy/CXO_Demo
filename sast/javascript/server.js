// INTENTIONALLY VULNERABLE - Checkmarx One demo only.
const express = require('express');
const { exec } = require('child_process');
const fs = require('fs');
const mysql = require('mysql');
const serialize = require('node-serialize');
const jwt = require('jsonwebtoken');
const crypto = require('crypto');
const _ = require('lodash');
const axios = require('axios');
const libxmljs = require('libxmljs');

const app = express();
app.use(express.json());
const db = mysql.createConnection({ host: 'db', user: 'root', password: 'root123' }); // VULN-060 hardcoded creds

app.get('/user', (req, res) => {
  db.query("SELECT * FROM users WHERE id = " + req.query.id);          // VULN-061 SQLi
  res.send('<h1>' + req.query.name + '</h1>');                         // VULN-062 XSS
});
app.get('/ping', (req, res) => exec('ping ' + req.query.h, (e, o) => res.send(o))); // VULN-063 cmd inj
app.get('/eval', (req, res) => res.send(String(eval(req.query.code))));            // VULN-064 eval
app.get('/file', (req, res) => res.send(fs.readFileSync('./uploads/' + req.query.f))); // VULN-065 traversal
app.get('/redir', (req, res) => res.redirect(req.query.to));                        // VULN-066 open redirect
app.get('/fetch', async (req, res) => res.send((await axios.get(req.query.url)).data)); // VULN-067 SSRF
app.post('/deser', (req, res) => res.send(serialize.unserialize(req.body.d)));     // VULN-068 deserialization
app.post('/merge', (req, res) => res.json(_.merge({}, req.body)));                 // VULN-069 prototype pollution
app.post('/xml', (req, res) => res.send(libxmljs.parseXml(req.body.x, { noent: true }).toString())); // VULN-070 XXE
app.get('/token', (req, res) => {
  res.json({ t: jwt.sign({ u: req.query.u }, 'shhhhh', { algorithm: 'HS256' }),   // VULN-071 weak JWT secret
             r: Math.random().toString(36),                                       // VULN-072 insecure random
             h: crypto.createHash('md5').update(req.query.p).digest('hex') });    // VULN-073 weak hash
});
app.get('/re', (req, res) => res.send(new RegExp(req.query.p).test(req.query.s))); // VULN-074 ReDoS / regex injection
app.use((req, res, next) => { res.header('Access-Control-Allow-Origin', '*'); next(); }); // VULN-075 CORS *
app.use(require('./sca_reachable'));
app.listen(3000);

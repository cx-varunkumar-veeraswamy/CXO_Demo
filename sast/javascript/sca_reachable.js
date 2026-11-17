// INTENTIONALLY VULNERABLE - vulnerable OSS functions are INVOKED with request data (SCA exploitable-path demo).
const express = require('express');
const _ = require('lodash');
const minimist = require('minimist');
const Handlebars = require('handlebars');
const ejs = require('ejs');
const marked = require('marked');
const moment = require('moment');
const serialize = require('serialize-javascript');
const nodeSerialize = require('node-serialize');
const jwt = require('jsonwebtoken');
const axios = require('axios');
const tar = require('tar');
const router = express.Router();

router.post('/sca/lodash', (req, res) => res.json(_.defaultsDeep({}, req.body)));           // lodash 4.17.15 prototype pollution CVE-2020-8203
router.get('/sca/lodash-tpl', (req, res) => res.send(_.template(req.query.t)({})));          // lodash 4.17.15 template code injection CVE-2021-23337
router.get('/sca/minimist', (req, res) => res.json(minimist(req.query.args.split(' '))));    // minimist 1.2.0 prototype pollution CVE-2020-7598
router.get('/sca/handlebars', (req, res) => res.send(Handlebars.compile(req.query.t)({})));  // handlebars 4.0.11 RCE CVE-2019-19919
router.get('/sca/ejs', (req, res) => res.send(ejs.render('<%= x %>', req.query)));           // ejs 2.5.7 RCE CVE-2022-29078
router.get('/sca/marked', (req, res) => res.send(marked(req.query.md)));                     // marked 0.3.5 XSS/ReDoS
router.get('/sca/moment', (req, res) => res.send(moment(req.query.d, req.query.f).format())); // moment 2.19.1 ReDoS CVE-2017-18214
router.get('/sca/serialize', (req, res) => res.send(serialize({ v: req.query.v })));         // serialize-javascript 1.5.0 XSS
router.post('/sca/unserialize', (req, res) => res.send(nodeSerialize.unserialize(req.body.d))); // node-serialize 0.0.4 RCE CVE-2017-5941
router.post('/sca/jwt', (req, res) => res.json(jwt.verify(req.body.t, 'secret')));           // jsonwebtoken 8.3.0 CVE-2022-23529 family
router.get('/sca/axios', async (req, res) => res.send((await axios.get(req.query.u)).data)); // axios 0.18.0 SSRF/ReDoS
router.post('/sca/tar', (req, res) => req.pipe(tar.x({ cwd: '/tmp/out' })));                // tar 4.4.1 arbitrary file overwrite CVE-2018-20834
module.exports = router;

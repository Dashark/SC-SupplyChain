var express = require('express');
var router = express.Router();

var ls_ca = '';
var self_ca = '';
/* GET users listing. */
router.get('/', function(req, res, next) {
  res.send('respond with a resource');
});

router.get('/genkey', function(req, res, next) {
  const { spawn } = require('node:child_process');
  const ls = spawn('openssl', ['genrsa']);

  ls.stdout.on('data', (data) => {
    res.json({ params: req.query, key: `${data}` });
  });
  spawn('openssl', ['genrsa', '-out', '/root/'+req.query['id']+'.pem']);

});

router.get('/pubkey', function(req, res, next) {
  const { spawn } = require('node:child_process');
  const ls = spawn('openssl', ['rsa', '-in', '/root/'+req.query['id']+'.pem', '-pubout']);

  ls.stdout.on('data', (data) => {
    res.json({ params: req.query, key: `${data}` });
  });
  spawn('openssl', ['rsa', '-in', '/root/'+req.query['id']+'.pem', '-out', '/root/'+req.query['id']+'_pub.pem', '-pubout']);

});

router.get('/ca', function(req, res, next) {
  const { spawn } = require('node:child_process');
  const ls = spawn('openssl', ['req', '-new', '-days', '365', '-key', '/root/privkey.pem', '-batch']);
  const x509 = spawn('openssl', ['req', '-new', '-x509', '-days', '365', '-key', '/root/privkey.pem', '-batch']);
  flag = 0;

  ls.stdout.on('data', (data) => {
    ls_ca = `${data}`;
    if (flag == 1)
      res.json({ params: req.query, ca: ls_ca, self_ca: self_ca });
    flag = 1;
  });
  x509.stdout.on('data', (data) => {
    self_ca = `${data}`;
    if (flag == 1)
      res.json({ params: req.query, ca: ls_ca, self_ca: self_ca });
    flag = 1;
  });
  spawn('openssl', ['req', '-new', '-days', '365', '-key', '/root/privkey.pem', '-batch', '-out', '/root/req.csr']);
  spawn('openssl', ['req', '-new', '-x509', '-days', '365', '-key', '/root/privkey.pem', '-batch', '-out', '/root/x509.csa']);
});

router.get('/ca-valid', function(req, res, next) {
  const { spawn } = require('node:child_process');
  const ls = spawn('openssl', ['req', '-verify', '-in', '/root/req.csr']);
  flag = 0;
  ls.stdout.on('data', (data) => {
    ls_ca = `${data}`
    if (flag == 1)
      res.json({ params: req.query, result: ls_ret, ca: ls_ca });
    flag = 1
  });
  ls.stderr.on('data', (data) => {
    ls_ret = `${data}`
    if (flag == 1)
      res.json({ params: req.query, result: ls_ret, ca: ls_ca });
    flag = 1
  });
});

router.get('/envelope', function(req, res, next) {
  const { spawn } = require('node:child_process');
  const ls = spawn('openssl', ['enc', '-des-cbc', '-in', '/root/config.log', '-pass', 'pass:p123']);
  ls.stdout.on('data', (data) => {
    res.json({ params: req.query, key: `${data}` });
  });
});

router.get('/encrypt', function(req, res, next) {
  require("fs").writeFileSync('/root/p_'+req.query['id'], req.query['message'], err => {
    if (err) {
      console.error(err);
    }
  });
  const { spawn } = require('node:child_process');
  const ls = spawn('openssl', ['rsautl', '-encrypt', '-inkey', '/root/'+req.query['id']+'_pub.pem', '-pubin', '-in', '/root/p_'+req.query['id']]);
  ls.stdout.on('data', (data) => {
    res.json({ params: req.query, key: `${data}` });
  });
  spawn('openssl', ['rsautl', '-encrypt', '-inkey', '/root/'+req.query['id']+'_pub.pem', '-pubin', '-in', '/root/p_'+req.query['id'], '-out', '/root/ep_'+req.query['id']]);
});

router.get('/decrypt', function(req, res, next) {
  const { spawn } = require('node:child_process');
  const ls = spawn('openssl', ['rsautl', '-decrypt', '-inkey', '/root/'+req.query['id']+'.pem', '-in', '/root/ep_'+req.query['id']]);
  ls.stdout.on('data', (data) => {
    res.json({ params: req.query, key: `${data}` });
  });
});

module.exports = router;

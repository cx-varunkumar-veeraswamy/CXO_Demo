// INTENTIONALLY VULNERABLE WebSocket server - demo only.
const WebSocket = require('ws');
const { exec } = require('child_process');
const wss = new WebSocket.Server({ port: 8081 });          // ws://, no auth, no origin check
wss.on('connection', (ws) => {
  ws.on('message', (m) => {
    const msg = JSON.parse(m);
    if (msg.cmd) exec(msg.cmd, (e, o) => ws.send(o));       // RCE over WS
    wss.clients.forEach(c => c.send('<b>' + msg.text + '</b>')); // stored XSS broadcast
  });
});

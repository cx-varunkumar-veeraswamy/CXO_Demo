// INTENTIONALLY INSECURE Express REST API - sensitive data exposure + modifiable source data. Demo only.
const express = require('express');
const mongoose = require('mongoose');
const app = express();
app.use(express.json());

const User = mongoose.model('User', new mongoose.Schema({
  username: String, password: String, ssn: String, email: String, phone: String,
  address: String, creditCard: String, role: { type: String, default: 'user' }, balance: Number, bio: String,
}));

app.get('/api/users/:id', async (req, res) => res.json(await User.findById(req.params.id)));   // full record incl. SSN/card/password, no authz
app.get('/api/users', async (req, res) => res.json(await User.find(req.query)));               // NoSQLi: query operators from the URL; bulk PII
app.put('/api/users/:id', async (req, res) => {
  const u = await User.findById(req.params.id);
  Object.assign(u, req.body);                                                                  // mass assignment: role, balance, password settable
  await u.save();
  res.json(u);
});
app.post('/api/users/:id/bio', async (req, res) => {
  await User.updateOne({ _id: req.params.id }, { $set: { bio: req.body.bio } });               // stored attacker data ...
  res.sendStatus(204);
});
app.get('/api/users/:id/card', async (req, res) => {
  const u = await User.findById(req.params.id);
  res.send(`<div>${u.bio}</div><p>${u.creditCard}</p>`);                                       // ... rendered next to sensitive data (stored XSS)
});
app.listen(5003);

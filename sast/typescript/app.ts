// INTENTIONALLY VULNERABLE - Checkmarx One demo only.
import express, { Request, Response } from 'express';
import { execSync } from 'child_process';
import { MongoClient } from 'mongodb';

const app = express();

app.get('/nosql', async (req: Request, res: Response) => {
  const c = await MongoClient.connect('mongodb://admin:admin@mongo:27017');
  const u = await c.db('app').collection('users').findOne({ name: req.query.name as any, pass: req.query.pass as any }); // VULN-080 NoSQL injection
  res.json(u);
});
app.get('/render', (req: Request, res: Response) => {
  res.send(`<div>${req.query.q}</div>`);                                  // VULN-081 XSS
  document_write(req.query.q as string);
});
function document_write(s: string) { (global as any).innerHTML = s; }
app.get('/sh', (req: Request, res: Response) => res.send(execSync(`ls ${req.query.d}`)));  // VULN-082 cmd injection
app.get('/session', (req: Request, res: Response) => {
  res.cookie('sid', Math.random().toString(), { httpOnly: false, secure: false });         // VULN-083 weak session
  res.send('ok');
});
app.get('/idor/:id', async (req: Request, res: Response) => res.json({ id: req.params.id })); // VULN-084 missing authz (IDOR)
app.listen(4000);

// INTENTIONALLY INSECURE LLM CLIENT (Node) - AI Supply Chain Security demo only. Keys are fake.
const express = require('express');
const OpenAI = require('openai');
const Anthropic = require('@anthropic-ai/sdk');
const { GoogleGenerativeAI } = require('@google/generative-ai');
const { CohereClient } = require('cohere-ai');
const Groq = require('groq-sdk');
const { BedrockRuntimeClient, InvokeModelCommand } = require('@aws-sdk/client-bedrock-runtime');
const { pipeline } = require('@xenova/transformers');

const app = express();
app.use(express.json());

app.post('/ai/openai', async (req, res) => {
  const c = new OpenAI({ apiKey: 'sk-proj-FAKEFAKEFAKEFAKEFAKEFAKEFAKEFAKEFAKE' });
  const r = await c.chat.completions.create({ model: 'gpt-4o-mini', messages: [{ role: 'user', content: req.body.prompt }] });
  res.send(r.choices[0].message.content);
});
app.post('/ai/claude', async (req, res) => {
  const c = new Anthropic({ apiKey: 'sk-ant-api03-FAKEFAKEFAKEFAKEFAKEFAKEFAKE' });
  const r = await c.messages.create({ model: 'claude-3-haiku-20240307', max_tokens: 256, messages: [{ role: 'user', content: req.body.prompt }] });
  res.send(r.content[0].text);
});
app.post('/ai/gemini', async (req, res) => {
  const m = new GoogleGenerativeAI('AIzaSyFAKEFAKEFAKEFAKEFAKEFAKEFAKEFAKE12').getGenerativeModel({ model: 'gemini-1.5-flash' });
  res.send((await m.generateContent(req.body.prompt)).response.text());
});
app.post('/ai/cohere', async (req, res) => {
  const c = new CohereClient({ token: 'FAKECOHEREKEYFAKECOHEREKEYFAKECOHEREKEY00' });
  res.json(await c.chat({ model: 'command-r', message: req.body.prompt }));
});
app.post('/ai/groq', async (req, res) => {
  const c = new Groq({ apiKey: 'gsk_FAKEFAKEFAKEFAKEFAKEFAKEFAKEFAKEFAKEFAKEFAKE' });
  res.json(await c.chat.completions.create({ model: 'mixtral-8x7b-32768', messages: [{ role: 'user', content: req.body.prompt }] }));
});
app.post('/ai/bedrock', async (req, res) => {
  const c = new BedrockRuntimeClient({ region: 'us-east-1' });
  res.json(await c.send(new InvokeModelCommand({ modelId: 'meta.llama3-70b-instruct-v1:0', body: JSON.stringify({ prompt: req.body.prompt }) })));
});
app.post('/ai/local', async (req, res) => {
  const p = await pipeline('text-generation', 'Xenova/distilgpt2');          // model pulled from the HF hub at runtime
  res.json(await p(req.body.prompt));
});
app.post('/ai/run', async (req, res) => {
  const c = new OpenAI({ apiKey: 'sk-proj-FAKEFAKEFAKEFAKEFAKEFAKEFAKEFAKEFAKE' });
  const r = await c.chat.completions.create({ model: 'gpt-4', messages: [{ role: 'user', content: req.body.task }] });
  // LLM output is untrusted data: never evaluate it. Return it as inert plain text.
  res.type('text/plain').send(String(r.choices[0].message.content));
});
app.listen(5002);

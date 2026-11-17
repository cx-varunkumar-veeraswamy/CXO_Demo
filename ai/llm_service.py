# INTENTIONALLY INSECURE LLM SERVICE - Checkmarx One AI Supply Chain Security demo only.
# Every model is referenced with a literal name inside a function reachable from an HTTP route,
# so scanners can identify the model, the provider and the call site. Keys are fake.
import os
import requests
from flask import Flask, request, jsonify
from openai import OpenAI
import anthropic
import cohere
import google.generativeai as genai
from mistralai.client import MistralClient
from groq import Groq
import boto3
import ollama
import replicate
from huggingface_hub import InferenceClient
from transformers import AutoModelForCausalLM, AutoTokenizer, AutoModelForSequenceClassification, pipeline
from sentence_transformers import SentenceTransformer
import torch

app = Flask(__name__)
OPENAI_KEY = "sk-proj-FAKEFAKEFAKEFAKEFAKEFAKEFAKEFAKEFAKEFAKE"      # hardcoded keys (secret detection too)
ANTHROPIC_KEY = "sk-ant-api03-FAKEFAKEFAKEFAKEFAKEFAKEFAKEFAKEFAKE"
HF_TOKEN = "hf_FAKEFAKEFAKEFAKEFAKEFAKEFAKEFAKEFA"


# ---------------- Hosted commercial model APIs ----------------
def ask_openai(p):
    c = OpenAI(api_key=OPENAI_KEY)
    return c.chat.completions.create(model="gpt-4o", messages=[{"role": "user", "content": p}]).choices[0].message.content

def ask_openai_legacy(p):
    c = OpenAI(api_key=OPENAI_KEY)
    return c.chat.completions.create(model="gpt-3.5-turbo", messages=[{"role": "user", "content": p}]).choices[0].message.content

def ask_anthropic(p):
    c = anthropic.Anthropic(api_key=ANTHROPIC_KEY)
    return c.messages.create(model="claude-3-5-sonnet-20241022", max_tokens=512, messages=[{"role": "user", "content": p}]).content[0].text

def ask_gemini(p):
    genai.configure(api_key="AIzaSyFAKEFAKEFAKEFAKEFAKEFAKEFAKEFAKE12")
    return genai.GenerativeModel("gemini-1.5-pro").generate_content(p).text

def ask_mistral(p):
    c = MistralClient(api_key="FAKEMISTRALKEYFAKEMISTRALKEY0000")
    return c.chat(model="mistral-large-latest", messages=[{"role": "user", "content": p}]).choices[0].message.content

def ask_cohere(p):
    return cohere.Client("FAKECOHEREKEYFAKECOHEREKEYFAKECOHEREKEY00").chat(model="command-r-plus", message=p).text

def ask_groq_llama(p):
    return Groq(api_key="gsk_FAKEFAKEFAKEFAKEFAKEFAKEFAKEFAKEFAKEFAKEFAKE").chat.completions.create(
        model="llama-3.1-70b-versatile", messages=[{"role": "user", "content": p}]).choices[0].message.content

def ask_deepseek(p):
    c = OpenAI(api_key="sk-FAKEDEEPSEEKFAKEDEEPSEEK0000", base_url="https://api.deepseek.com")
    return c.chat.completions.create(model="deepseek-chat", messages=[{"role": "user", "content": p}]).choices[0].message.content

def ask_xai(p):
    c = OpenAI(api_key="xai-FAKEFAKEFAKEFAKEFAKEFAKEFAKEFAKE", base_url="https://api.x.ai/v1")
    return c.chat.completions.create(model="grok-beta", messages=[{"role": "user", "content": p}]).choices[0].message.content

def ask_perplexity(p):
    c = OpenAI(api_key="pplx-FAKEFAKEFAKEFAKEFAKEFAKEFAKEFAKE", base_url="https://api.perplexity.ai")
    return c.chat.completions.create(model="llama-3.1-sonar-large-128k-online", messages=[{"role": "user", "content": p}]).choices[0].message.content

def ask_bedrock_titan(p):
    import json
    b = boto3.client("bedrock-runtime", region_name="us-east-1")
    return b.invoke_model(modelId="amazon.titan-text-express-v1", body=json.dumps({"inputText": p}))["body"].read()

def ask_bedrock_claude(p):
    import json
    b = boto3.client("bedrock-runtime", region_name="us-east-1")
    return b.invoke_model(modelId="anthropic.claude-v2", body=json.dumps({"prompt": p}))["body"].read()

def ask_azure_openai(p):
    from openai import AzureOpenAI
    c = AzureOpenAI(api_key="FAKEAZUREKEYFAKEAZUREKEY00000000", api_version="2024-02-01", azure_endpoint="https://cxo-demo.openai.azure.com")
    return c.chat.completions.create(model="gpt-4-turbo", messages=[{"role": "user", "content": p}]).choices[0].message.content

def ask_ollama(p):
    return ollama.chat(model="llama3", messages=[{"role": "user", "content": p}])["message"]["content"]

def ask_replicate(p):
    return "".join(replicate.run("meta/meta-llama-3-70b-instruct", input={"prompt": p}))

def ask_hf_inference(p):
    return InferenceClient(token=HF_TOKEN).text_generation(p, model="HuggingFaceH4/zephyr-7b-beta")


# ---------------- Open-weight models downloaded from Hugging Face (literal names) ----------------
def load_local_models():
    AutoModelForCausalLM.from_pretrained("meta-llama/Llama-2-7b-chat-hf", trust_remote_code=True)
    AutoModelForCausalLM.from_pretrained("mistralai/Mistral-7B-Instruct-v0.2", trust_remote_code=True)
    AutoModelForCausalLM.from_pretrained("google/gemma-7b")
    AutoModelForCausalLM.from_pretrained("microsoft/phi-2", trust_remote_code=True)
    AutoModelForCausalLM.from_pretrained("Qwen/Qwen2-7B-Instruct", trust_remote_code=True)
    AutoModelForCausalLM.from_pretrained("deepseek-ai/deepseek-coder-6.7b-instruct", trust_remote_code=True)
    AutoModelForCausalLM.from_pretrained("tiiuae/falcon-7b-instruct", trust_remote_code=True)
    AutoModelForCausalLM.from_pretrained("bigcode/starcoder2-15b")
    AutoModelForCausalLM.from_pretrained("stabilityai/stablelm-2-1_6b", trust_remote_code=True)
    AutoModelForCausalLM.from_pretrained("EleutherAI/gpt-neox-20b")
    AutoModelForCausalLM.from_pretrained("random-user-1234/totally-legit-llama-finetune", trust_remote_code=True)  # unvetted publisher
    AutoModelForSequenceClassification.from_pretrained("distilbert-base-uncased-finetuned-sst-2-english")
    AutoTokenizer.from_pretrained("gpt2")
    SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")
    pipeline("text-generation", model="openai-community/gpt2")
    pipeline("fill-mask", model="bert-base-uncased")
    torch.load("downloaded/model.bin")                 # pickle-based weights, no weights_only
    return "loaded"


ROUTES = {"openai": ask_openai, "gpt35": ask_openai_legacy, "anthropic": ask_anthropic, "gemini": ask_gemini,
          "mistral": ask_mistral, "cohere": ask_cohere, "llama": ask_groq_llama, "deepseek": ask_deepseek,
          "grok": ask_xai, "perplexity": ask_perplexity, "titan": ask_bedrock_titan, "bedrockclaude": ask_bedrock_claude,
          "azure": ask_azure_openai, "ollama": ask_ollama, "replicate": ask_replicate, "hf": ask_hf_inference}


@app.route("/ai/chat/<provider>", methods=["POST"])
def chat(provider):
    prompt = request.json["prompt"]                    # untrusted input straight to the model (prompt injection)
    return jsonify(answer=ROUTES[provider](prompt))


@app.route("/ai/agent", methods=["POST"])
def agent():
    code = ask_openai("Write python for: " + request.json["task"])
    exec(code)                                         # LLM output executed (insecure output handling, LLM02)
    return "done"


@app.route("/ai/models/load")
def models():
    return load_local_models()


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001)

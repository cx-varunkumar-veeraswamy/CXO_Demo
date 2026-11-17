# INTENTIONALLY INSECURE AI SUPPLY CHAIN USAGE - Checkmarx One AI Supply Chain Security demo only.
# 18 models/providers: open-weight models from Hugging Face + hosted APIs. No real keys here.
import pickle, torch
from transformers import AutoModelForCausalLM, AutoTokenizer, pipeline, AutoModel
from sentence_transformers import SentenceTransformer
import openai, anthropic, cohere
import google.generativeai as genai
from mistralai.client import MistralClient
import replicate, requests

# ---- Hugging Face hosted models from many vendors (trust_remote_code = arbitrary code execution) ----
HF_MODELS = {
    "meta":        "meta-llama/Llama-2-7b-chat-hf",
    "mistral":     "mistralai/Mistral-7B-Instruct-v0.1",
    "google":      "google/gemma-7b",
    "microsoft":   "microsoft/phi-2",
    "alibaba":     "Qwen/Qwen-7B-Chat",
    "deepseek":    "deepseek-ai/deepseek-coder-6.7b-instruct",
    "tii":         "tiiuae/falcon-7b-instruct",
    "stability":   "stabilityai/stablelm-2-1_6b",
    "bigscience":  "bigscience/bloom-560m",
    "eleutherai":  "EleutherAI/gpt-j-6b",
    "salesforce":  "Salesforce/codegen-350M-mono",
    "bigcode":     "bigcode/starcoder",
    "01ai":        "01-ai/Yi-6B",
    "nvidia":      "nvidia/Llama3-ChatQA-1.5-8B",
    "unverified":  "random-user-1234/totally-legit-llama-finetune",   # unvetted community model
}
for vendor, name in HF_MODELS.items():
    tok = AutoTokenizer.from_pretrained(name, trust_remote_code=True)               # unpinned revision + remote code
    mdl = AutoModelForCausalLM.from_pretrained(name, trust_remote_code=True)

pipe = pipeline("text-generation", model="gpt2")                                    # unpinned, no hash
emb = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")
weights = torch.load("downloaded/model.bin")                                        # pickle deserialization of untrusted weights
legacy = pickle.load(open("downloaded/classifier.pkl", "rb"))                       # pickled model
raw = requests.get("http://models.example.com/model.safetensors").content           # model fetched over HTTP, no checksum

# ---- Hosted commercial APIs ----
openai.api_key = "sk-proj-AbCdEfGhIjKlMnOpQrStUvWxYz0123456789AbCdEfGhIjKl"          # hardcoded key
oa = openai.ChatCompletion.create(model="gpt-4", messages=[{"role": "user", "content": input()}])  # prompt injection sink

an = anthropic.Anthropic(api_key="sk-ant-api03-FAKEFAKEFAKEFAKEFAKEFAKEFAKEFAKEFAKEFAKEFAKE")
an.messages.create(model="claude-3-opus-20240229", max_tokens=100, messages=[{"role": "user", "content": input()}])

genai.configure(api_key="AIzaSyFAKEFAKEFAKEFAKEFAKEFAKEFAKEFAKE12")
genai.GenerativeModel("gemini-pro").generate_content(input())

co = cohere.Client("FAKECOHEREKEYFAKECOHEREKEYFAKECOHEREKEY00")
co.chat(model="command-r-plus", message=input())

MistralClient(api_key="FAKEMISTRALKEYFAKEMISTRALKEY0000").chat(model="mistral-large-latest", messages=[])
replicate.run("meta/meta-llama-3-70b-instruct", input={"prompt": input()})           # 16th+ provider via Replicate

# LLM output executed directly (insecure output handling - OWASP LLM02)
code = oa["choices"][0]["message"]["content"]
exec(code)

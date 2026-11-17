# INTENTIONALLY INSECURE - AI agent with excessive agency / prompt injection. Demo only.
from langchain.llms import OpenAI, HuggingFaceHub, Bedrock, AzureOpenAI
from langchain.agents import load_tools, initialize_agent
from langchain.chains import PALChain, LLMBashChain

llm = OpenAI(openai_api_key="sk-FAKEFAKEFAKEFAKEFAKEFAKEFAKEFAKEFAKEFAKEFAKEFAKE", temperature=0)
hf  = HuggingFaceHub(repo_id="tiiuae/falcon-40b", huggingfacehub_api_token="hf_FAKEFAKEFAKEFAKEFAKEFAKEFAKEFAKEFA")
br  = Bedrock(model_id="amazon.titan-text-express-v1")                  # Amazon Titan
az  = AzureOpenAI(deployment_name="gpt-35-turbo")                       # Azure OpenAI
tools = load_tools(["terminal", "python_repl", "requests_all"], llm=llm)  # excessive agency: shell + python + net
agent = initialize_agent(tools, llm, agent="zero-shot-react-description")
agent.run(input())                                                      # direct prompt injection -> RCE
LLMBashChain.from_llm(llm).run(input())

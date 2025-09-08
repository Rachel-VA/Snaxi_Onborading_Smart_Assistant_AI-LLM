#******************** Different ways to load models locally ****

#1 import directly from subprocess
import subprocess

result = subprocess.run(
    ["ollama", "run", "dolphin-mistral"],
    input=prompt.encode("utf-8"),
    capture_output=True
)
print(result.stdout.decode("utf-8"))

#*************************2 HTTP requests to Ollama server *****************
import requests

resp = requests.post(
    "http://localhost:11434/api/chat",
    json={
        "model": "dolphin-mistral",
        "messages": [{"role": "user", "content": "hi"}]
    }
)
print(resp.json())



# ***************** 3 Direct model loading with libraries (no Ollama)  *********
from transformers import AutoModelForCausalLM, AutoTokenizer

tokenizer = AutoTokenizer.from_pretrained("mistralai/Mistral-7B-Instruct")
model = AutoModelForCausalLM.from_pretrained("mistralai/Mistral-7B-Instruct")

inputs = tokenizer("hi", return_tensors="pt")
outputs = model.generate(**inputs, max_new_tokens=50)
print(tokenizer.decode(outputs[0]))


# ********************** 4. llama-cpp-python (GGUF models)  ******************
from llama_cpp import Llama

llm = Llama(model_path="mistral-7b-instruct.Q4_K_M.gguf")
print(llm("hi"))




# ********************* 5. Ollama Python client (Snaxi now uses this)  **************
import ollama

response = ollama.chat(
    model="dolphin-mistral",
    messages=[{"role": "user", "content": "hi"}]
)
print(response["message"]["content"])
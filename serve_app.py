import subprocess
import ray
from fastapi import FastAPI, Form
from fastapi.responses import HTMLResponse
from transformers import AutoTokenizer, AutoModelForCausalLM
from ray import serve
import torch
import time

# Start Ray manually
print("🚀 Starting Ray...")
subprocess.run(
    ["ray", "start", "--head", "--port=6379", "--dashboard-host=0.0.0.0", "--include-dashboard=false"],
    check=True
)

# Connect to Ray
ray.init(address="auto")

# Start Serve
serve.start(detached=True)

# Load model
model_path = "./local-model"
tokenizer = AutoTokenizer.from_pretrained(model_path, use_fast=False)
model = AutoModelForCausalLM.from_pretrained(model_path)

# FastAPI app
app = FastAPI()

@serve.deployment
@serve.ingress(app)
class ModelServer:
    @app.get("/", response_class=HTMLResponse)
    async def form(self):
        return """
        <html>
            <head><title>LLM Chat</title></head>
            <body>
                <h2>Talk to LLM</h2>
                <form action='/generate' method='post'>
                    <input name='prompt' type='text' style='width:300px' required />
                    <input type='submit' value='Send' />
                </form>
            </body>
        </html>
        """

    @app.post("/generate", response_class=HTMLResponse)
    async def generate(self, prompt: str = Form(...)):
        inputs = tokenizer(prompt, return_tensors="pt")
        outputs = model.generate(**inputs, max_new_tokens=50)
        result = tokenizer.decode(outputs[0], skip_special_tokens=True)
        return f"<p><b>Prompt:</b> {prompt}</p><p><b>Response:</b> {result}</p><a href='/'>Back</a>"

# Deploy app
serve.run(ModelServer.bind(), route_prefix="/")

# ✅ Keep container alive (block forever)
print("✅ App deployed. Blocking main thread to keep container alive...")
while True:
    time.sleep(3600)

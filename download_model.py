from transformers import AutoTokenizer, AutoModelForCausalLM

model_id = "sshleifer/tiny-gpt2"

# Download with "slow" tokenizer to avoid the corrupted .json
tokenizer = AutoTokenizer.from_pretrained(model_id, use_fast=False)
model = AutoModelForCausalLM.from_pretrained(model_id)

tokenizer.save_pretrained("local-model")
model.save_pretrained("local-model")

print("✅ Model downloaded successfully to ./local-model")

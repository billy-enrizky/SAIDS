import torch
from transformers import pipeline, AutoModelForCausalLM, AutoTokenizer

# Define the model ID and cache directory
model_id = "dfurman/CalmeRys-78B-Orpo-v0.1"
cache_dir = "./cache"  # Specify your cache directory

# Load the model and tokenizer with the cache directory
model = AutoModelForCausalLM.from_pretrained(model_id, cache_dir=cache_dir, torch_dtype=torch.bfloat16)
tokenizer = AutoTokenizer.from_pretrained(model_id, cache_dir=cache_dir)

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
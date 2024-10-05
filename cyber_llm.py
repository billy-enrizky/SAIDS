import torch
from transformers import pipeline, AutoModelForCausalLM, AutoTokenizer

# Define the model ID and cache directory
model_id = "meta-llama/Llama-2-7b-hf"
cache_dir = "./cache"  # Specify your cache directory

# Load the model and tokenizer with the cache directory
model = AutoModelForCausalLM.from_pretrained(model_id, cache_dir=cache_dir, torch_dtype=torch.bfloat16)
tokenizer = AutoTokenizer.from_pretrained(model_id, cache_dir=cache_dir)

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

def get_llama2_reponse(prompt, max_new_tokens=50):
    inputs = tokenizer(prompt, return_tensors="pt").to(device)
    outputs = model.generate(**inputs, max_new_tokens=max_new_tokens, temperature= 0.00001)
    response = tokenizer.decode(outputs[0], skip_special_tokens=True)
    return response

snort_output = """
04/24-15:50:29.236253  [**] [1:498:6]  
ATTACK-RESPONSES id check returned root [**] 
[Classification: Potentially Bad Traffic] [Priority: 2]
TCP 82.165.50.118:80 -> 69.143.202.28:39929
"""

prompt = f"Give Cyber Security Analysis of {snort_output}"
output = get_llama2_reponse(prompt, max_new_tokens=10000)

print(output)

with open('test_output.txt', 'w') as f:
    f.write(output)
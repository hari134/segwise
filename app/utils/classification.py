from transformers import AutoTokenizer, AutoModelForSequenceClassification
from huggingface_hub import hf_hub_download
import torch
import json

repo_id = "anonIN/quantized_distilbert_classification"
device = torch.device("cpu")
model = AutoModelForSequenceClassification.from_pretrained(repo_id).to(device)
tokenizer = AutoTokenizer.from_pretrained(repo_id)

# Download label_map.json from the repository on Hugging Face Hub
label_map_path = hf_hub_download(repo_id, "label_map.json")
with open(label_map_path) as f:
    label_map = json.load(f)

inverse_label_map = {v: k for k, v in label_map.items()}

def classify_review(text):
    inputs = tokenizer(text, return_tensors="pt", truncation=True, max_length=128, padding=True).to(device)
    with torch.no_grad():
        outputs = model(**inputs)
        prediction = torch.argmax(outputs.logits, dim=1).item()
    return inverse_label_map[prediction]

print(classify_review("This app is fantastic!"))

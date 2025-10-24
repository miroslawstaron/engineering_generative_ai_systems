import json
import os
import torch
from transformers import AutoModelForSequenceClassification, AutoTokenizer

def init():
    global model
    global tokenizer

    model_dir = os.getenv('AZUREML_MODEL_DIR')
    model_path = os.path.join(model_dir, 'decBERTa')

    tokenizer = AutoTokenizer.from_pretrained(model_path)
    model = AutoModelForSequenceClassification.from_pretrained(model_path)

def run(raw_data):
    inputs = json.loads(raw_data)
    text = inputs.get('text')

    input_tokens = tokenizer(text, return_tensors='pt')

    with torch.no_grad():
        output = model(**input_tokens)

    predictions = output.logits.argmax(dim=-1).item()
    return json.dumps({"prediction": predictions})

import torch
from transformers import AutoTokenizer, AutoModelForTokenClassification

# Load the fine-tuned model and tokenizer
model_name = "distilbert-fine-tuned"  # Change this to the model you want to test
model_path = "C:/Users/ibsan/Desktop/TenX/week-5/model_output/results/xlm-roberta-fine-tuned"
tokenizer = AutoTokenizer.from_pretrained(model_path)
model = AutoModelForTokenClassification.from_pretrained(model_path)

# Function to perform NER on a given text

def predict_entities(text):
    # Tokenize the input text
    inputs = tokenizer(text, return_tensors="pt", truncation=True, padding=True, max_length=512)
    # Get model predictions
    with torch.no_grad():
        outputs = model(**inputs)
    logits = outputs.logits
    # Get the predicted token classes
    predictions = torch.argmax(logits, dim=2)
    # Convert token IDs to labels
    tokens = tokenizer.convert_ids_to_tokens(inputs.input_ids[0])
    labels = [model.config.id2label[prediction.item()] for prediction in predictions[0]]
    # Return the tokens and their corresponding labels
    return list(zip(tokens, labels))

# Test the function with a sample text
sample_text = "በአዲስ �በባ ውስጥ አዲስ ስልክ በ 5000 ብር ይገኛል።"
entities = predict_entities(sample_text)
print(entities)
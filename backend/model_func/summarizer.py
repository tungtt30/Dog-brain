import torch
from transformers import T5Tokenizer, T5ForConditionalGeneration


device = "cuda"
model_dir = "backend/models/summ_model"
tokenizer = T5Tokenizer.from_pretrained(model_dir)
model = T5ForConditionalGeneration.from_pretrained(model_dir).to(device)
model.eval()

def summ(input_text = "Không có gì để tóm tắt"):
    text = input_text + " </s>"
    inputs = tokenizer(text, return_tensors="pt")
    input_ids, attention_masks = inputs["input_ids"].to(device), inputs["attention_mask"].to(device)
    outputs = model.generate(
        input_ids = input_ids, attention_mask=attention_masks,
        max_length=512,
        early_stopping=True
    )
    line = tokenizer.decode(outputs[0], skip_special_tokens=True, clean_up_tokenization_spaces=True)
    return line
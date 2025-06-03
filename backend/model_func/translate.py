import torch
from transformers import T5Tokenizer, T5ForConditionalGeneration
import json



with open('backend/app_config.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

device = data["device"]
model_dir = "backend/models/trans_model"
tokenizer = T5Tokenizer.from_pretrained(model_dir)
model = T5ForConditionalGeneration.from_pretrained(model_dir).to(device)
model.eval()

def trans(input_text = "Một âm một dương đấy gọi là Đạo, Khí tím đến từ phương đông, Những thứ đã niêm yết ngoài kia, không phải đen thì phải là trắng"):
    inputs = tokenizer(input_text, return_tensors="pt", max_length=512, truncation=True)
    summary_ids = model.generate(inputs["input_ids"].to(device), max_length=512, num_beams=4, early_stopping=True)
    summary = tokenizer.decode(summary_ids[0], skip_special_tokens=True)
    # print(summary)
    return summary
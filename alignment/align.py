from transformers import AutoTokenizer, AutoModel

tokenizer = AutoTokenizer.from_pretrained("sentence-transformers/LaBSE")
model = AutoModel.from_pretrained("sentence-transformers/LaBSE")

sentences = ["Hello World", "Hallo Welt"]

encoded_input = tokenizer(sentences, padding=True, truncation=True, max_length=64, return_tensors='pt')

with torch.no_grad():
    model_output = model(**encoded_input)

embeddings = model_output.pooler_output
embeddings = torch.nn.functional.normalize(embeddings)
print(embeddings.size())
print(embeddings)
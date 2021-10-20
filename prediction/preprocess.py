import torch
from transformers import BertTokenizer, BertModel
import os, csv
from models import SNACSDataset

# MODELS
tokenizer = BertTokenizer.from_pretrained('bert-base-multilingual-cased')
model = BertModel.from_pretrained('bert-base-multilingual-cased',
    output_hidden_states = True,
)

print('Grabbing data')
data = []
sentences = []
current_sentence = []
for entry in os.scandir('../annotations/lp_aryaman'):
    if entry.path.endswith('.csv'):
        with open(entry, 'r') as fin:
            reader = csv.reader(fin)
            for i, row in enumerate(reader):
                if i == 0: continue
                if row[0] == '':
                    sentences.append(current_sentence)
                    current_sentence = []
                else:
                    if row[2]: data.append([row[0], row[2], row[3], len(sentences), len(current_sentence) + 1])
                    current_sentence.append(row[0])
        if current_sentence:
            sentences.append(current_sentence)

print('Tokenizing')
# tokenize sentences
sentences = [tokenizer.tokenize('[CLS] ' + ' '.join(sentence) + ' [SEP]') for sentence in sentences]
indexed_tokens = [tokenizer.convert_tokens_to_ids(sentence) for sentence in sentences]

# Put the model in "evaluation" mode, meaning feed-forward operation.
model.eval()

print('BERTifying')
# Run the text through BERT, and collect all of the hidden states produced
# from all 12 layers.
outputs = []
with torch.no_grad():
    for i, sentence in enumerate(indexed_tokens):
        if i % 10 == 0: print(i)
        if len(sentence) == 0:
            outputs.append([])
            continue
        # Mark each of the 22 tokens as belonging to sentence "1".
        segments_ids = [1] * len(sentence)
        
        # Convert inputs to PyTorch tensors
        tokens_tensor = torch.tensor([sentence])
        segments_tensors = torch.tensor([segments_ids])
        outputs.append(model(tokens_tensor, segments_tensors))

print('Grabbing BERT outputs')
all_embeddings = []
for i, output in enumerate(outputs):
    token_embeddings = torch.stack(output[2], dim=0)
    token_embeddings = torch.squeeze(token_embeddings, dim=1)
    token_embeddings = token_embeddings.permute(1,0,2)
    
    all_embeddings.append(token_embeddings)

print(all_embeddings)
torch.save(all_embeddings, "embeddings.pickle")
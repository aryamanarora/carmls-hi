#!/usr/bin/env python
# coding: utf-8

# In[2]:


import torch
from transformers import BertTokenizer, BertModel

# OPTIONAL: if you want to have more information on what's happening, activate the logger as follows
import logging
#logging.basicConfig(level=logging.INFO)

import matplotlib.pyplot as plt

# Load pre-trained model tokenizer (vocabulary)
tokenizer = BertTokenizer.from_pretrained('bert-base-multilingual-cased')


# In[88]:


import os, csv

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

# this is our training data
print(data[100:105])


# In[89]:


# tokenize sentences
print(' '.join(sentences[0]))
sentences = [tokenizer.tokenize('[CLS] ' + ' '.join(sentence) + ' [SEP]') for sentence in sentences]

print(len(sentences))
print(sentences[:5])


# In[90]:


# Map the token strings to their vocabulary indeces.
indexed_tokens = [tokenizer.convert_tokens_to_ids(sentence) for sentence in sentences]
print(indexed_tokens[0])
print(sentences[0])


# In[81]:


# Load pre-trained model (weights)
model = BertModel.from_pretrained('bert-base-multilingual-cased',
                                  output_hidden_states = True, # Whether the model returns all hidden-states.
                                  )

# Put the model in "evaluation" mode, meaning feed-forward operation.
model.eval()


# In[91]:


# Run the text through BERT, and collect all of the hidden states produced
# from all 12 layers.
outputs = []
with torch.no_grad():
    
    for i, sentence in enumerate(indexed_tokens):
        if len(sentence) == 0:
            outputs.append([])
            continue
        # Mark each of the 22 tokens as belonging to sentence "1".
        segments_ids = [1] * len(sentence)
        print(i)
        
        # Convert inputs to PyTorch tensors
        tokens_tensor = torch.tensor([sentence])
        segments_tensors = torch.tensor([segments_ids])
        
        outputs.append(model(tokens_tensor, segments_tensors))


# In[92]:


outputs[0]


# In[99]:


all_embeddings = []
for i, output in enumerate(outputs):
    print(i)
    # Concatenate the tensors for all layers. We use `stack` here to
    # create a new dimension in the tensor.
    token_embeddings = torch.stack(output[2], dim=0)
    print(token_embeddings.size(), end=" ")
    
    # Remove dimension 1, the "batches".
    token_embeddings = torch.squeeze(token_embeddings, dim=1)
    print(token_embeddings.size(), end=" ")
    
    # Swap dimensions 0 and 1.
    token_embeddings = token_embeddings.permute(1,0,2)
    print(token_embeddings.size())
    all_embeddings.append(token_embeddings)


# In[112]:


cur_word_length = 0
concatenated_embeddings = []
for i, token_embeddings in enumerate(all_embeddings):
    # Stores the token vectors, with shape [22 x 3,072]
    token_vecs_cat = []
    print(i)

    # `token_embeddings` is a [22 x 12 x 768] tensor.
    # print(token_embeddings.size())

    # For each token in the sentence...
    for j, token in enumerate(token_embeddings):

        # `token` is a [12 x 768] tensor

        # Concatenate the vectors (that is, append them together) from the last 
        # four layers.
        # Each layer vector is 768 values, so `cat_vec` is length 3,072.
        cat_vec = torch.cat((token[-1], token[-2], token[-3], token[-4]), dim=0)
        
        # Sum the vectors from the last four layers.
        # sum_vec = torch.sum(token[-4:], dim=0)

        # Use `cat_vec` to represent `token`.
        if not sentences[i][j].startswith('##'):
            token_vecs_cat.append([cat_vec, sentences[i][j]])
    
    concatenated_embeddings.append(token_vecs_cat)

#     print ('Shape is: %d x %d' % (len(token_vecs_cat), len(token_vecs_cat[0])))


# In[117]:


for _, i in enumerate(data[:30]):
    print(_, i, concatenated_embeddings[i[3]][i[4]])


# In[118]:


from scipy.spatial.distance import cosine

# Calculate the cosine similarity between the word bank 
# in "bank robber" vs "river bank" (different meanings).
same_bank = 1 - cosine(concatenated_embeddings[14][6][0], concatenated_embeddings[14][11][0])

# Calculate the cosine similarity between the word bank
# in "bank robber" vs "bank vault" (same meaning).
diff_bank = 1 - cosine(concatenated_embeddings[14][6][0], concatenated_embeddings[14][3][0])

print('Vector similarity for  *similar*  meanings:  %.2f' % same_bank)
print('Vector similarity for *different* meanings:  %.2f' % diff_bank)

diff_bank = 1 - cosine(concatenated_embeddings[4][11][0], concatenated_embeddings[10][1][0])
print('Vector similarity for *different* meanings:  %.2f' % diff_bank)


# In[119]:


print(len(data))


# In[ ]:





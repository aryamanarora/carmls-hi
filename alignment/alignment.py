from transformers import BertTokenizer, BertModel
import torch

tokenizer = BertTokenizer.from_pretrained('bert-base-multilingual-cased')
model = BertModel.from_pretrained("bert-base-multilingual-cased")

def align(text, text2):
    tokens = tokenizer(text, return_tensors='pt')
    tokens2 = tokenizer(text2, return_tensors='pt')
    left = model(**tokens)[0][0][1:-1]
    right = model(**tokens2)[0][0][1:-1]

    cos = torch.nn.CosineSimilarity(dim=0, eps=1e-6)
    S = [[0 for i in range(len(right))] for j in range(len(left))]
    A, M = [[0 for i in range(len(right))] for j in range(len(left))], [[0 for i in range(len(right))] for j in range(len(left))]
    for pos_i, i in enumerate(left):
        for pos_j, j in enumerate(right):
            S[pos_i][pos_j] = float(cos(i, j))
            
    for _ in range(1):
        for i in range(len(left)):
            for j in range(len(right)):
                if max(sum([x[j] for x in A]), sum(A[i])) == 0:
                    M[i][j] = 1
                elif min(sum([x[j] for x in A]), sum(A[i])) > 0:
                    M[i][j] = 0
                else:
                    M[i][j] = 0.5
        
        maxes_i = [[0, -1]] * len(left)
        maxes_j = [[0, -1]] * len(right)
        for i in range(len(left)):
            for j in range(len(right)):
                val = S[i][j] * M[i][j]
                if val > maxes_i[i][0]: maxes_i[i] = [val, j]
                if val > maxes_j[j][0]: maxes_j[j] = [val, i]
        
        for i in range(len(left)):
            if maxes_j[maxes_i[i][1]][1] == i:
                A[i][maxes_i[i][1]] += 1
    

    print(text)
    print(text2)
    res = []
    real_i, real_j = -1, -1
    for pos_i, i in enumerate(A):
        w_i = tokenizer.decode(tokens.input_ids[0][pos_i + 1:pos_i + 2])
        if not w_i.startswith('##'): real_i += 1
        real_j = -1
        for pos_j, j in enumerate(i):
            w_j = tokenizer.decode(tokens2.input_ids[0][pos_j + 1:pos_j + 2])
            if not w_j.startswith('##'): real_j += 1
            if j == 1:
                res.append([real_i, real_j])
    
    return res

with open('test.e', 'r') as en, open('test.h', 'r') as hi,  open('res.out', 'w') as fout:
    while True:
        english = en.readline()
        hindi = hi.readline()
        english = english.replace('<s snum=', '').replace('</s>', '').strip()
        hindi = hindi.replace('<s snum=', '').replace('</s>', '').strip()
        if not english:
            break
        num, english = english.split('>')
        hindi = hindi.split('>')[1]

        res = align(english, hindi)
        for i in res:
            fout.write(f'{num} {i[0] + 1} {i[1] + 1}\n')
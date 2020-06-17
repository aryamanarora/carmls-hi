import stanza
import sys
import os
import csv

nlp = stanza.Pipeline(lang='hi', processors='tokenize,mwt,pos,lemma,depparse')

global words
with open(sys.argv[1], 'r') as fin:
    words = fin.read()

code = sys.argv[1].replace('/', '_')
doc = nlp(words)

out = sys.argv[1].replace('.txt', '.csv')

with open(out, 'w') as fout:
    write = csv.writer(fout)
    for i, sent in enumerate(doc.sentences):
        text = sent.text.replace("\n", " ")
        for i, word in enumerate(sent.words):
            write.writerow([i + 1, word.text])
        write.writerow(['', ''])
            

# os.system(f'python streusle/conllulex2csv.py {out} {out.replace(".conllulex", ".csv")}')
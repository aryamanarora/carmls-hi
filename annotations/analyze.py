import glob
import csv
from collections import defaultdict
import stanza

nlp = stanza.Pipeline(lang='hi', processors='tokenize,mwt,pos,lemma,depparse', tokenize_pretokenized=True)
count = defaultdict(int)

for file in glob.glob('./**/*.csv'):
    with open(file, 'r') as fin:
        reader = csv.reader(fin)
        sent = ""
        sent_arr = []
        for i, line in enumerate(reader):
            if i % 100 == 0: print(i)
            try:
                sent += line[0] + ' '
                sent_arr.append(line)
                if line[0] == '':
                    if sent != ' ' and sent != '':
                        # doc = nlp(sent)
                        for i, word in enumerate(sent_arr):
                            if word[2] != '':
                                try:
                                    # dat = doc.sentences[0].words[i]
                                    # if dat.deprel == 'case':
                                    #     head = doc.sentences[0].words[dat.head - 1]
                                    #     count[f'{word[2]} {head.deprel}'] += 1
                                    # else:
                                    #     count[f'{word[2]} {dat.deprel}'] += 1
                                    count[(word[1], word[2], word[3])] += 1
                                except:
                                    print(word)
                                    pass
                    sent = ''
                    sent_arr = []
            except:
                pass
def so(k):
    return -k[1]
for k in sorted(count.items(), key=so):
    print(f'{k[0][0]},{k[0][1]},{k[0][2]},{k[1]}')
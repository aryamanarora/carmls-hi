import stanza
import csv

nlp = stanza.Pipeline(lang='hi', processors='tokenize,pos,lemma,depparse', tokenize_pretokenized=True)

# columns
# id, word, lemma, upos, xpos, feats, head, deprel, [deps, misc], smwe, [lexcat, lexlemma], ss, ss2, [wmwe, wlemma, lextag]

res = ''
for i in range(1, 28):
    print(i)
    with open(f'../annotations/lp_adjudicated_cleaned/{i}.csv', 'r') as fin:
        reader = csv.reader(fin)

        # get all sentences from this file,
        # maintaining our tokenisation
        sents, sent = [], []
        for row in reader:
            if row[0] == '':
                if sent != []: sents.append(sent)
                sent = []
            else:
                sent.append(row)
        sents.append(sent)

        # merge sentences for stanza
        flat = '\n'.join([' '.join([y[0] for y in x]) for x in sents])
        doc = nlp(flat)

        # to conllulex
        for sent_id, sent in enumerate(doc.sentences):
            # print(sent.text, [x[0] for x in sents[sent_id]])
            res += f'\n# sent_id = lp_hi_{i}_{sent_id}'
            res += f'\n# text = {sent.text}'
            for word_id, word in enumerate(sent.words):
                # generate row for each word, first normal CONLLU stuff
                output = [word.id, word.text, word.lemma, word.upos, word.xpos, word.feats, word.head, word.deprel]
                output.extend([''] * 2)

                non_initial = False
                if sents[sent_id][word_id][4]:
                    if sents[sent_id][word_id][4].split(':')[1] != '1':
                        non_initial = True

                # now LEX features
                output.extend([sents[sent_id][word_id][4], 'P' if sents[sent_id][word_id][2] else '', sents[sent_id][word_id][1] if not non_initial else ''])
                output.append('p.' + sents[sent_id][word_id][2])
                output.append('p.' + sents[sent_id][word_id][3])
                output.extend([''] * 4)
                output = ['_' if x in ['', 'p.'] else x for x in output]

                # add to output
                res += '\n' + '\t'.join(map(str, output))
            res += '\n'

with open('../hindi.conllulex', 'w') as fout:
    fout.write(res)



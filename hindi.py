import stanza

nlp = stanza.Pipeline(lang='hi', processors='tokenize,mwt,pos,lemma,depparse')

global words
with open('input.txt', 'r') as fin:
    words = fin.read()

doc = nlp(words)

with open('output.conllulex', 'w') as fout:
    for sent in doc.sentences:
        fout.write(f'\n# text = {sent.text}')
        for i, word in enumerate(sent.words):
            fout.write(f'\n{i + 1}\t{word.text}\t{word.lemma}\t{word.upos}\t{word.xpos}')
            fout.write(f'\t{word.feats if word.feats else "_"}')
            fout.write(f'\t{word.head}\t{word.deprel}')
            add = "\t".join(["_"] * 11)
            fout.write(f'\t{add}')
        fout.write(f'\n')
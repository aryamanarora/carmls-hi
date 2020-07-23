from gensim.models import Word2Vec
from sklearn.decomposition import PCA
from matplotlib import pyplot
import csv
import stanza
import glob

nlp = stanza.Pipeline(lang='hi', processors='tokenize,mwt,pos,lemma,depparse', tokenize_pretokenized=True)

sents = []
for file in glob.glob('./**/*.csv'):
    with open(file, 'r') as fin:
        reader = csv.reader(fin)
        sent = []
        for i, line in enumerate(reader):
            if i % 100 == 0: print(i)
            try:
                if line[0] == '':
                    sents.append(sent)
                    sent = []
                else:
                    word = line[0]
                    if line[1] != '':
                        doc = nlp(line[0]).sentences[0].words[0]
                        if doc.upos == 'PRON':
                            sent.append(doc.lemma)
                        word = line[1]
                    if line[2] != '':
                        word += '_' + line[2] + '_' + line[3]
                    if line[4] == '' or line[4].endswith(':1'):
                        sent.append(word)
            except:
                pass

model = Word2Vec(sents, min_count=1)

X = model[model.wv.vocab]
pca = PCA(n_components=2)
result = pca.fit_transform(X)

pyplot.scatter(result[:, 0], result[:, 1])
words = list(model.wv.vocab)
for i, word in enumerate(words):
	pyplot.annotate(word, xy=(result[i, 0], result[i, 1]))
pyplot.show()
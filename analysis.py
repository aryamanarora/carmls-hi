import glob
import csv
import json

sent = []
sents = []
header = []
for file in glob.glob('annotations/**/annotated.csv', recursive=True):
    with open(file) as fin:
        reader = csv.reader(fin)
        for row in reader:
            if not header:
                header = row
                continue
            if row[0].startswith('#'):
                if sent: sents.append(sent)
                sent = []
            if row[0].isdigit():
                sent.append(dict(zip(header, row)))

with open('sents.json', 'w') as fout:
    fout.write(json.dumps(sents, indent=2))
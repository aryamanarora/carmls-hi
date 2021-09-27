import glob
import csv
from sklearn.metrics import cohen_kappa_score, accuracy_score, f1_score, adjusted_mutual_info_score
from collections import Counter
import math
import scipy.stats
import sys
import matplotlib.pyplot as plt
import pandas as pd

class Row():
    def __init__(self, token, lemma, scene, function, dic):
        self.token = token
        self.lemma = lemma
        self.scene = scene
        self.function = function
        self.construal = scene + function
        self.dict = dic
    
    def is_snacs(self):
        return self.scene != "" and self.function != ""
    
    def match(self, t):
        return self.lemma == t

    def __getitem__(self, key):
        return self.dict[key]

def main(lang):
    print(lang)

    rows = []

    case_markers = ['ने', 'से', 'को', 'का', 'में', 'पर', 'तक']
    focus_markers = ['भी', 'ही', 'तो']

    if lang == 'hindi':
        for file in glob.glob('./lp_adjudicated_cleaned/*.csv'):
            with open(file, 'r') as fin:
                reader = csv.reader(fin)
                for i, row in enumerate(reader):
                    if row[0]:
                        rows.append(Row(row[0], row[1], row[2], row[3], row))
    elif lang == 'korean':
        with open('lp_other/little_prince_ko.tsv', 'r') as fin:
            reader = csv.reader(fin, delimiter='\t')
            next(reader)
            for row in reader:
                row = [x.replace('_', '') for x in row]
                rows.append(Row(row[3], row[5], row[6], row[7], row))
    elif lang == 'chinese':
        with open('lp_other/chinese.conllulex', 'r') as fin:
            reader = csv.reader(fin, delimiter='\t')
            for row in reader:
                if row:
                    row = [x.replace('_', '') for x in row]
                    rows.append(Row(row[1], row[2], row[13], row[14], row))
    elif lang == 'english':
        for file in glob.glob('lp_adjudicated_en/*.csv'):
            with open(file, 'r') as fin:
                reader = csv.reader(fin)
                header = []
                for i, row in enumerate(reader):
                    if i == 0:
                        header = row
                        continue
                    if row:
                        if row[0].isdigit():
                            rows.append(Row(row[1], row[1].lower(), row[3], row[4], row))
    elif lang == 'english-streusel':
        with open('lp_other/english_streusle.conllulex', 'r') as fin:
            reader = csv.reader(fin, delimiter='\t')
            for row in reader:
                if row:
                    if len(row) == 19:
                        row = [x.replace('_', '') for x in row]
                        if not row[13].startswith('p'):
                            row[13] = ""
                            row[14] = ""
                        rows.append(Row(row[1], row[2], row[13], row[14], row))
    elif lang == 'english-pastrie':
        with open('lp_other/pastrie.conllulex', 'r') as fin:
            reader = csv.reader(fin, delimiter='\t')
            for row in reader:
                if row:
                    if len(row) == 19:
                        row = [x.replace('_', '') for x in row]
                        rows.append(Row(row[1], row[2], row[13], row[14], row))
    elif lang == 'german':
        with open('lp_other/german_old.csv', 'r') as fin:
            reader = csv.reader(fin)
            for row in reader:
                if row[0].isdigit():
                    row = [x.replace('_', '') for x in row]
                    rows.append(Row(row[1], row[2], row[13], row[14], row))

    print(f'Total tokens: {len(rows)}')
    print(f'Total labelled tokens: {sum(not row.match("") for row in rows)}')

    print()
    print(f'Total targets: {sum((row.is_snacs() and row.lemma != "") for row in rows)}')
    if lang == 'hindi':
        print(f'Total case marker targets: {sum(row.lemma in case_markers and row.is_snacs() for row in rows)}')
        print(f'Total focus marker targets: {sum(row.lemma in focus_markers and row.is_snacs() for row in rows)}')
    print(f'Total other targets: {sum(row.lemma not in focus_markers and row.lemma not in case_markers and row.lemma != "" and row.is_snacs() for row in rows)}')

    print()
    print(f'Kinds of targets: {len(set([row.lemma for row in rows if row.is_snacs()]))}')

    print()
    scene_roles = set([row.scene for row in rows if row.scene])
    functions = set([row.function for row in rows if row.function])
    print(f'Kinds of scene role: {len(scene_roles)}')
    print(f'Kinds of function: {len(functions)}')
    print(f'Kinds of supersense: {len(scene_roles.union(functions))}')
    print(f'Kinds of construals: {len(set([row.construal for row in rows if row.scene != ""]))}')
    print(f'Kinds of same construals: {len(set([row.construal for row in rows if row.is_snacs()and row.scene == row.function]))}')
    print(f'Kinds of different construals: {len(set([row.construal for row in rows if row.is_snacs()and row.scene != row.function]))}')

    print()
    print(f'Total same construals: {sum(row.scene == row.function and row.is_snacs()for row in rows)}')
    print(f'Total different construals: {sum(row.scene != row.function and row.is_snacs()for row in rows)}')

    if lang == 'hindi':
        print()
        scene_roles = [(row[6], row[11]) for row in rows if row.scene and row[6] and row[11]]
        print(f'Scene role Cohen\'s kappa: {cohen_kappa_score([x[0] for x in scene_roles], [x[1] for x in scene_roles])}')
        functions = [(row[7], row[12]) for row in rows if row.scene and row[6] and row[11]]
        print(f'Function Cohen\'s kappa: {cohen_kappa_score([x[0] for x in functions], [x[1] for x in functions])}')
        construals = [(row[6] + row[7], row[11] + row[12]) for row in rows if row.scene and row[6] and row[11]]
        print(f'Construal Cohen\'s kappa: {cohen_kappa_score([x[0] for x in construals], [x[1] for x in construals])}')

    # def is_valid(row, i=None):
    #     if i:
    #         return row[1] == i and (row[4].endswith(":1") or row[4] == "") and row[1] != ""
    #     return (row[4].endswith(":1") or row[4] == "") and row[1] != ""

    print()
    targets = set([row.lemma for row in rows if row.is_snacs()])

    scene_roles = [row.scene for row in rows if row.scene and row.function]
    functions = [row.function for row in rows if row.scene and row.function]
    print(f'AMI between scene role and function: {adjusted_mutual_info_score(scene_roles, functions)}')

    most_common = {}
    for i in targets:
        most_common[i] = Counter([row.scene for row in rows if row.is_snacs() and row.lemma == i]).most_common(1)[0][0]
    preds = [most_common[row.lemma] for row in rows if row.is_snacs()]
    gold = [row.scene for row in rows if row.is_snacs()]
    print(f'Most common scene, accuracy = micro-f1: {accuracy_score(gold, preds)}')

    most_common = {}
    for i in targets:
        most_common[i] = Counter([row.function for row in rows if row.is_snacs() and row.lemma == i]).most_common(1)[0][0]
    preds = [most_common[row.lemma] for row in rows if row.is_snacs()]
    gold = [row.function for row in rows if row.is_snacs()]
    print(f'Most common function, accuracy = micro-f1: {accuracy_score(gold, preds)}')

    most_common = {}
    for i in targets:
        most_common[i] = Counter([row.construal for row in rows if row.is_snacs() and row.lemma == i]).most_common(1)[0][0]
    preds = [most_common[row.lemma] for row in rows if row.is_snacs()]
    gold = [row.construal for row in rows if row.is_snacs()]
    print(f'Most common construal, accuracy = micro-f1: {accuracy_score(gold, preds)}')

    print()
    print('Entropy per target')
    entropies = {}
    for i in targets:
        entropy = 0
        labels = [row.construal for row in rows if row.is_snacs() and row.lemma == i]
        total = Counter(labels)
        for j in total:
            entropy -= (total[j] / len(labels)) * math.log(total[j] / len(labels), 2)
        entropies[i] = entropy

    x = sorted(entropies.items(), key=lambda x: -x[1])
    print(x)
    return x

if __name__ == '__main__':
    main(sys.argv[1])
    # entropies = {}
    # fig, axes = plt.subplots(3, 2, sharey=True)
    # langs = ['hindi', 'korean', 'chinese', 'german', 'english', 'english-streusel']
    # i = 0
    # for row in range(3):
    #     for col in range(2):
    #         res = pd.DataFrame(dict(main(langs[i])), index=[0])
    #         res = res.T
    #         print(res)
    #         res.hist(bins=40, ax=axes[row, col], range=[0, 5])
    #         axes[row, col].title.set_text(langs[i])
    #         i += 1
    #         if i >= len(langs):
    #             break
    #     if i >= len(langs):
    #         break
    # plt.show()

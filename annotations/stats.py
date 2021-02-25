import glob
import csv
from collections import defaultdict

total_tokens, labelled_tokens = 0, 0
all_tokens = 0
have_role, have_func = 0, 0
questions = 0
case_makers = 0
same = 0

adps = set()
construals = set()
supersenses = set()
scene_roles, functions = set(), set()

top_construals = defaultdict(int)
top_scene_roles, top_functions = defaultdict(int), defaultdict(int)
top_adps = defaultdict(int)

for file in glob.glob('./**/*.csv'):
    # only first 7 chapters
    # if int(file.split('/')[-1].split('.')[0]) > 7: continue
    with open(file, 'r') as fin:
        reader = csv.reader(fin)
        sent = ""
        sent_arr = []
        for i, line in enumerate(reader):
            # if i % 100 == 0: print(i)
            try:
                sent += line[0] + ' '
                sent_arr.append(line)
                if line[0] == '':
                    if sent != ' ' and sent != '':
                        # doc = nlp(sent)
                        for i, word in enumerate(sent_arr):
                            if word[0]: total_tokens += 1
                            if word[1]:
                                all_tokens += 1
                            if word[1] and (word[4] == '' or word[4].endswith(':1')):
                                labelled_tokens += 1
                                if not (word[1] in ['ने', 'को', 'से', 'का', 'में', 'पर', 'तक']): continue
                                adps.add(word[1])
                                top_adps[word[1]] += 1
                                construals.add((word[2], word[3]))
                                top_construals[(word[2], word[3])] += 1
                                supersenses.add(word[2])
                                supersenses.add(word[3])
                                scene_roles.add(word[2])
                                top_scene_roles[word[2]] += 1
                                functions.add(word[3])
                                top_functions[word[3]] += 1
                                if not word[2] or not word[3]:
                                    print(word)
                                if word[1] in ['ने', 'को', 'से', 'पर', 'तक', 'में', 'का']:
                                    case_makers += 1
                                if word[2] == word[3]:
                                    same += 1
                            elif word[2] or word[3]:
                                print(word)
                            if word[2]: have_role += 1
                            if word[3]: have_func += 1
                            if '*Q*' in word[5]:
                                questions += 1
                    sent = ''
                    sent_arr = []
            except:
                pass

print(f'{all_tokens} total tokens annotated in some way')
print(f'{labelled_tokens} / {total_tokens} tokens labelled ({labelled_tokens / total_tokens}), {len(adps)} types')
print(f'{have_role} tokens have a scene role ({have_role / labelled_tokens})')
print(f'{have_func} tokens have a function ({have_func / labelled_tokens})')
print(f'{same} tokens have the same scene role and function ({same / labelled_tokens})')
print(f'{questions} questions')
print(f'{case_makers} targets are basic case markers')
print(f'{len(construals)} types of construals')
print(f'{len(supersenses)} types of supersenses')
print(f'{len(scene_roles)} types of scene roles')
print(f'{len(functions)} types of fxns')
print([(k, v / labelled_tokens) for k, v in sorted(top_adps.items(), key=lambda x: -x[1])][:10])
print([(k, v / labelled_tokens) for k, v in sorted(top_construals.items(), key=lambda x: -x[1])][:10])
print([(k, v / labelled_tokens) for k, v in sorted(top_scene_roles.items(), key=lambda x: -x[1])][:10])
print([(k, v / labelled_tokens) for k, v in sorted(top_functions.items(), key=lambda x: -x[1])][:10])
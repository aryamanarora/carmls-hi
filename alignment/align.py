import csv
import simalign

model = simalign.SentenceAligner()

with open('../annotations/lp_adjudicated_en/2.csv', 'r') as en, open('../annotations/lp_adjudicated/2.csv', 'r') as hi:
    reader_en, reader_hi = csv.reader(en), csv.reader(hi)
    en_data, hi_data = [], []
    sent = []
    for row in reader_en:
        if row[1] != "":
            if sent != []: en_data.append(sent)
        sent.append(row)
    if sent != []: en_data.append(sent)
    for row in reader_hi:
        if row[1] != "":
            if sent != []: hi_data.append(sent)
        sent.append(row)
    if sent != []: hi_data.append(sent)
    print('checking', [x[1] for x in en_data[0]])
    print([x[1] for x in hi_data[0]])
    # print(model.get_word_aligns([x[1] for x in en_data[0]], [x[1] for x in hi_data[0]])['mwmf'])

    # while True:
    #     english = en.readline()
    #     hindi = hi.readline()
    #     english = english.replace('<s snum=', '').replace('</s>', '').strip()
    #     hindi = hindi.replace('<s snum=', '').replace('</s>', '').strip()
    #     if not english:
    #         break
    #     num, english = english.split('>')
    #     hindi = hindi.split('>')[1]

    #     res = model.get_word_aligns(english, hindi)['mwmf']
    #     for i in res:
    #         fout.write(f'{num} {i[0] + 1} {i[1] + 1}\n')
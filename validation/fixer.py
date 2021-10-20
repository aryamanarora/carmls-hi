import csv
from validation import targets, supersenses, scene_roles, snacs

for i in range(1, 28):
    with open(f'../annotations/lp_adjudicated/{i}.csv', 'r') as fin, open(f'../annotations/lp_adjudicated_cleaned/{i}.csv', 'w') as fout:
        rows = []
        reader = csv.reader(fin)
        writer = csv.writer(fout)
        for line, row in enumerate(reader):
            if line == 0:
                writer.writerow(row)
                continue
            
            row[0] = row[0].strip()
            
            for x in targets:
                row[x] = row[x].strip()
                if row[x] == 'की' or row[x] == 'के':
                    row[x] = 'का'
                if row[x] == 'सी':
                    row[x] = 'सा'
            
            for x in supersenses:
                row[x] = row[x].strip()
                if '/' in row[x] or '?' in row[x]:
                    row[x] = '??'

            for x in scene_roles:
                if row[x] == "" and row[x + 1] != "":
                    row[x] = row[x + 1]
                if row[x + 1] == "" and row[x] != "":
                    row[x + 1] = row[x]

            writer.writerow(row)
            

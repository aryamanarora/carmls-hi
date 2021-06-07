import glob
import csv

rows = []

case_markers = ['ने', 'से', 'को', 'का', 'में', 'पर', 'तक']
focus_markers = ['भी', 'ही', 'तो']

for file in glob.glob('./lp_adjudicated_cleaned/*.csv'):
    with open(file, 'r') as fin:
        reader = csv.reader(fin)
        for i, row in enumerate(reader):
            if row[0]:
                rows.append(row)

print(f'Total tokens: {len(rows)}')
print(f'Total labelled tokens: {sum(row[1] != "" for row in rows)}')

print()
print(f'Total targets: {sum(row[1] != "" and (row[4].endswith(":1") or row[4] == "") for row in rows)}')
print(f'Total case marker targets: {sum(row[1] in case_markers and (row[4].endswith(":1") or row[4] == "") for row in rows)}')
print(f'Total focus marker targets: {sum(row[1] in focus_markers and (row[4].endswith(":1") or row[4] == "") for row in rows)}')
print(f'Total other targets: {sum(row[1] not in focus_markers and row[1] not in case_markers and row[1] != "" and (row[4].endswith(":1") or row[4] == "") for row in rows)}')

print()
print(f'Kinds of targets: {len(set([row[1] for row in rows if row[1] != ""]))}')

print()
scene_roles = set([row[2] for row in rows if row[2] != ""])
functions = set([row[3] for row in rows if row[3] != ""])
print(f'Kinds of scene role: {len(scene_roles)}')
print(f'Kinds of function: {len(functions)}')
print(f'Kinds of supersense: {len(scene_roles.union(functions))}')
print(f'Kinds of construals: {len(set([row[2] + row[3] for row in rows if row[2] != ""]))}')
print(f'Kinds of same construals: {len(set([row[2] + row[3] for row in rows if row[2] != "" and row[2] == row[3]]))}')
print(f'Kinds of different construals: {len(set([row[2] + row[3] for row in rows if row[2] != "" and row[2] != row[3]]))}')

print()
print(f'Total same construals: {sum(row[2] == row[3] and row[2] != "" for row in rows)}')
print(f'Total different construals: {sum(row[2] != row[3] and row[2] != "" for row in rows)}')
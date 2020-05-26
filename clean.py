import glob
import os

files = glob.glob('annotations/**/annotated.csv', recursive=True)
files.sort()
for file in files:
    print(file)
    os.system(f'python streusle/csv2conllulex.py {file} {file.replace(".csv", ".conllulex")}')
os.system(f'cat {" ".join([file.replace(".csv", ".conllulex") for file in files])} > annotations/all.conllulex')
#!/usr/bin/python3

import re, load_transcript

# I really need a module for constants...
seasons = [
    's1',
    's2',
    's3',
    's4',
    's5',
    's6',
    's7',
]

allLines = load_transcript.getAllLines()

listLines = []
for season in seasons:
    for episode in allLines[season]:
        listLines += episode

def get_names(lines):
    all_names = []

    for line in lines:
        all_names += re.findall(r'^[A-Z]+:', line)

    return [name.replace(':', '') for name in set(all_names)]

#unique_names = [name.replace(':', '') for name in list(set(re.findall(r'[A-Z)]+:', listLines)))]
# 


all_names = get_names(listLines)

with open('names2.txt', 'w') as f:
    for name in all_names:
        f.write(f'{name}\n')

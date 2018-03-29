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

listLines = ''
for season in seasons:
    for episode in allLines[season]:
        listLines += ' '.join(episode)

unique_names = [name.replace(':', '') for name in list(set(re.findall(r'[A-Z)]+:', listLines)))]

with open('names.txt', 'w') as f:
    for name in unique_names:
        f.write(f'{name}\n')
            


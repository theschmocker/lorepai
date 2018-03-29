#!/usr/bin/python3

import paths, os

seasons = [
    's1',
    's2',
    's3',
    's4',
    's5',
    's6',
    's7',
]

def getLines(pathToFile):
    lines = []
    with open(pathToFile) as f:
        lines = [line.replace('\n', '') for line in f.readlines()]
    return lines

def getTranscriptsForSeason(season):
    seasonPath = paths.getSeasonPath(season)
    # Ensure that episodes are in the right order
    filePaths = sorted(os.listdir(seasonPath), key=lambda x: int(x.replace('.txt', '')))
    filePaths = [os.path.join(seasonPath, f) for f in filePaths]
    return filePaths

def getLinesInSeason(season):
    return [getLines(f) for f in getTranscriptsForSeason(season)]

def getAllLines():
    allLines = {}
    for season in seasons:
        allLines[season] = getLinesInSeason(season)
    return allLines

import os

baseDir = os.path.dirname(os.path.realpath(__file__))

def getSeasonPath(season):
    return os.path.join(baseDir, 'transcripts/{}'.format(season))



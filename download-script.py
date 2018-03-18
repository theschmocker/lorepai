#!/usr/bin/python3

import requests, bs4, os, re

baseURL = 'https://crazy-internet-people.com/site/gilmoregirls/pages'
seasons = [
        's1',
        's2',
        's3',
        's4',
        's5',
        's6',
        's7',
]

def isPage(page):
    return re.match('\d+\.html', page) is not None

def getPagesForSeason(season):
    url = baseURL + '/{}/{}s'.format(season, season)
    directory = requests.get(url)
    directory.raise_for_status()
    dirSoup = bs4.BeautifulSoup(directory.text, 'html.parser')
    tags = dirSoup.select('a')
    links = [tag.string.replace(' ', '') for tag in tags]
    links = list(filter(isPage, links))
    links = sorted(links, key=lambda x: int(re.sub('\.html', '', x)))
    print(links)
    links = [url + '/' + link for link in links]
    
    return links

def extractLines(page):
    print('\nDownloading {} ...'.format(page))
    res = requests.get(page)
    res.raise_for_status()

    pageSoup = bs4.BeautifulSoup(res.text, 'html.parser')
    content = pageSoup.select('p font[size="2"]')[0].getText()

    # Fix weird formatting of transcript html
    content = content.replace('\t', '')
    content = re.sub('(\n)+', '\n', content)
    allLines = content.split('\n')

    # Only grab characters' lines
    allLines = list(filter(lambda x: re.match(r'^[A-Z]+:', x) and not x.startswith('DISCLAIMER'), allLines))
    
    # Fix weird apostrophe stuff
    allLines = [line.replace('\x91', "'").replace('\x92', "'") for line in allLines]

    # Remove non-dialog
    allLines = [re.sub(r'\[.*?\]', '', line) for line in allLines]

    return allLines

def buildTranscriptDirs():
    baseDir = os.path.dirname(os.path.realpath(__file__))
    transcriptPath = os.path.join(baseDir, 'transcripts/')
    # Make base path
    os.makedirs(transcriptPath, exist_ok=True)
    # Make subdirectory for each season
    for season in seasons:
        os.makedirs(os.path.join(transcriptPath, season), exist_ok=True)

def downloadSeason(season):
    baseDir = os.path.dirname(os.path.realpath(__file__))
    seasonPath = os.path.join(baseDir, 'transcripts/{}'.format(season))
    
    pages = getPagesForSeason(season)
    for index, page in enumerate(pages):
        lines = [line + '\n' for line in extractLines(page)]

        with open(os.path.join(seasonPath, '{}.txt'.format(index + 1)), 'w') as f:
            for line in lines:
                f.write(line)

def main():
    for season in seasons:
        downloadSeason(season)

if __name__ == '__main__':
    buildTranscriptDirs()
    main()









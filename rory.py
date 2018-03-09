#!/usr/bin/python3

import requests, bs4, re

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
    links = [url + '/' + link for link in links]
    return links


def getRorysLinesFrom(page):
    print('\nDownloading {} ...'.format(page))
    res = requests.get(page)
    res.raise_for_status()
    print('Getting Rory\'s lines from {} ...'.format(page))

    pageSoup = bs4.BeautifulSoup(res.text, 'html.parser')
    content = pageSoup.select('p font[size="2"]')[0].getText()
    content = content.replace('\t', '')
    content = re.sub('(\n)+', '\n', content)
    allLines = content.split('\n')
    onlyRory = list(filter(lambda x: x.startswith('RORY:'), allLines))
    onlyRory = [line.replace('\x91', "'").replace('\x92', "'") for line in onlyRory]
    return onlyRory

def getMentions(lines, name):
    return sum([line.count(name) for line in lines])

def seasonScore(season, dean=0, jess=0):
    return (season, {"Dean": dean, "Jess": jess})

def printAllSeasons(data):
    for each in data:
        season = each[0].replace('s', 'Season ')
        scores = each[1]
        names = list(scores.keys())
        print(season)
        print(' - {0}: {1}'.format(names[0], scores[names[0]])) 
        print(' - {0}: {1}'.format(names[1], scores[names[1]])) 
        print('\n')

def getTotalScores(data):
    totalScores = {'Dean': 0, 'Jess': 0}

    scoreList = [item[1] for item in data]

    totalScores['Dean'] = sum([score['Dean'] for score in scoreList])
    totalScores['Jess'] = sum([score['Jess'] for score in scoreList])

    return totalScores

def printTotalScores(scores):
    print('GRAND TOTAL')
    print('-----------')
    print(' - Dean: {} mentions in series.'.format(scores['Dean']))
    print(' - Jess: {} mentions in series.'.format(scores['Jess']))

def getData():
    data = []
    try:
        for season in seasons:
            pages = getPagesForSeason(season)
            deanInSeason = 0
            jessInSeason = 0
            for page in pages:
                lines = getRorysLinesFrom(page)
                deanInSeason += getMentions(lines, 'Dean')
                jessInSeason += getMentions(lines, 'Jess')
            data.append(seasonScore(season, deanInSeason, jessInSeason))
            
    except KeyboardInterrupt:
        print('\n\nProgram Exiting')
        exit()
    return data

def main():
    data = getData()
    printAllSeasons(data)
    printTotalScores(getTotalScores(data))
    
main()


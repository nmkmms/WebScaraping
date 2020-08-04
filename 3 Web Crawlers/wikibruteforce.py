from urllib.request import urlopen
from urllib.error import HTTPError, URLError
from bs4 import BeautifulSoup as bsoup
import datetime
import random
import re


random.seed(datetime.datetime.now())

link = '/wiki/Kevin_Bacon'


def getLinks(articleUrl: str):
    """Return all wiki-links connected to given one."""
    try:
        html = urlopen(f'https://en.wikipedia.org{articleUrl}')
    except HTTPError as _:
        return None
    except URLError as _:
        print('The server could not be found!')

    try:
        bs = bsoup(html, 'html.parser')
    except AttributeError as e:
        print(e)
        return articleUrl

    return bs.find('div', {'id': 'bodyContent'}).find_all(
        'a', href=re.compile('^(/wiki/)((?!:).)*$'))


def main():
    """Run parser & choose random links."""
    links = getLinks(link)
    counter = 1
    while len(links):
        newArticle = random.choice(links).attrs['href']
        print(f'Step {counter}:\n\t{newArticle}')
        links = getLinks(newArticle)
        counter += 1


if __name__ == '__main__':
    main()
    
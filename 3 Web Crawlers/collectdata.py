import sys
from urllib.request import urlopen
from urllib.error import HTTPError, URLError
from bs4 import BeautifulSoup as bsoup
import re

# Found pages:
PAGES = set()

# Starting url:
URL = 'https://en.wikipedia.org'


def getLinks(pageUrl: str):
    """Find links on given page, print info, works recursively."""
    global PAGES
    current_page = f"{URL}{pageUrl}"
    print(current_page)

    try:
        html = urlopen(current_page)
    except HTTPError:
        print('HTTPError clause.')
        return None
    except URLError:
        print(f'{current_page} could not be found!', file=sys.stderr)
        return None
    
    bs = bsoup(html, 'html.parser')
    try:
        # Title
        print(bs.h1.get_text())
        # Short info
        print(bs.find(id='mw-content-text').find_all('p', class_='')[0].get_text())
        # Link to edit
        print(bs.find(id='ca-edit').find('span').find('a').attrs['href'])
    except AttributeError:
        print('This page missing some info. Continuing...')

    for link in bs.find_all('a', href=re.compile('^(/wiki/)')):
        if 'href' in link.attrs:
            if link.attrs['href'] not in PAGES:
                # New page found
                newPage = link.attrs['href']
                print('-' * 20)
                print(newPage)
                PAGES.add(newPage)
                getLinks(newPage)


def main():
    """Run app."""
    print('*' * 30)
    print(f'Working with {URL} page')
    print('*' * 30)

    getLinks('')


if __name__ == '__main__':
    main()

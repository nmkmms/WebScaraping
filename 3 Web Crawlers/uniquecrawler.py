from urllib.request import urlopen
from urllib.error import HTTPError, URLError
from bs4 import BeautifulSoup as bsoup
import re


PAGES = set()

URL = 'http://en.wikipedia.org'

def getLinks(pageUrl: str):
    """Fill PAGES set with unique links from URL website."""
    global PAGES
    current_page = f'{URL}{pageUrl}'

    try:
        html = urlopen(current_page)
    except HTTPError as _:
        return None
    except URLError as _:
        print(f'The {current_page} could not be found!')

    try:    
        bs = bsoup(html, 'html.parser')
    except AttributeError as e:
        print(e)
        return current_page

    for link in bs.find_all('a', href=re.compile('^(/wiki/)')):
        if 'href' in link.attrs:
            if link.attrs['href'] not in PAGES:
                # New page found
                newPage = link.attrs['href']
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

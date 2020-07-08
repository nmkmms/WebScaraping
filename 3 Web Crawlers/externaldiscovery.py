from urllib.request import urlopen
from urllib.parse import urlparse
from urllib.error import HTTPError, URLError
from bs4 import BeautifulSoup
import re
import datetime
import random

# Found pages
PAGES = set()

# Starting URL:
URL = 'http://oreilly.com'

# Random seed
random.seed(datetime.datetime.now())


def getInternalLinks(bs: BeautifulSoup, includeUrl: str) -> list:
    """Retrive a list of all Internal links on a page."""
    parsed = urlparse(includeUrl)
    includeUrl = f'{parsed.scheme}://{parsed.netloc}'

    # Set of found links
    internalLinks = set()

    # Find all links that begin with a "/"
    for link in bs.find_all('a', 
            href=re.compile('^(/|.*' + includeUrl + ')')):
        temp_link = link.attrs['href']
        if temp_link is not None:
            if temp_link not in internalLinks:
                if temp_link.startswith('/'):
                    internalLinks.add(includeUrl + temp_link)
                else:
                    internalLinks.add(temp_link)
    
    return list(internalLinks)


def getExternalLinks(bs: BeautifulSoup, excludeUrl: str) -> list:
    """Retrieve a list of all external links on a page."""
    # Set of found links:
    externalLinks = set()

    # Find all links that starts with "http" that
    # do not contain the current URL
    for link in bs.find_all('a',
            href=re.compile('^(http|www)((?!' + excludeUrl + ').)*$')):
        temp_link = link.attrs['href']
        if temp_link is not None:
            if temp_link not in externalLinks:
                externalLinks.add(temp_link)
    
    return list(externalLinks)


def getRandomExternalLink(startingPage: str) -> str:
    """Return random external link from geiven page.
    
    If not exists, tries to find a new one from internal links.
    """
    try:
        html = urlopen(startingPage)
    except HTTPError:
        print("HTTPError clause")
        return startingPage
    except URLError:
        print(f'{startingPage} could not be found!')
        return None

    bs = BeautifulSoup(html, 'html.parser')

    # List of external links on given page
    externalLinks = getExternalLinks(bs, 
        urlparse(startingPage).netloc)

    if len(externalLinks) == 0:
        print('No external links, looking around the site for one')
        parsed = urlparse(startingPage)
        domain = f'{parsed.scheme}://{parsed.netloc}'

        # List of internal links on given page
        internalLinks = getInternalLinks(bs, domain)

        return getRandomExternalLink(random.choice(internalLinks))
    else:
        return random.choice(externalLinks)

    
def followExternalOnly(startingSite: str):
    """Discover external links only."""
    externalLink = getRandomExternalLink(startingSite)
    print(f'Random external link is:\n\t{externalLink}')
    followExternalOnly(externalLink)


# Collects a list of all external URLs found on the site
allExtLinks = set()
allIntLinks = set()


def getAllExternalLinks(siteUrl: str):
    try:
        html = urlopen(siteUrl)
        parsed = urlparse(siteUrl)
    except HTTPError:
        print('HTTPError clause')
        return None
    except URLError:
        print(f'{siteUrl} could not be found!')
        return None

    domain = f'{parsed.scheme}://{parsed.netloc}'
    bs = BeautifulSoup(html, 'html.parser')

    internalLinks = getInternalLinks(bs, domain)
    externalLinks = getExternalLinks(bs, domain)

    for link in externalLinks:
        if link not in allExtLinks:
            allExtLinks.add(link)
            print(link)

    for link in internalLinks:
        if link not in allIntLinks:
            allIntLinks.add(link)
            print(link)


if __name__ == '__main__':
    # followExternalOnly(URL)

    allIntLinks.add(URL)
    getAllExternalLinks(URL)

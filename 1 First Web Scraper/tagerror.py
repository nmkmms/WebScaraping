from urllib.request import urlopen
from urllib.error import HTTPError
from bs4 import BeautifulSoup as BSoup

def getTitle(url: str) -> str:
    """Return title of given url page."""
    try:
        html = urlopen(url)
    except HTTPError as _:
        return None
    
    try:
        bs = BSoup(html, 'html.parser')
        title = bs.body.title
    except AttributeError as _:
        return None
    
    return title


title = getTitle('http://www.pythonscraping.com/pages/page1.html')
print(title if title else 'Title could not be found!')
from urllib.request import urlopen
from bs4 import BeautifulSoup as bsoup
import re

url = 'http://en.wikipedia.org/wiki/Kevin_Bacon'

html = urlopen(url)
bs = bsoup(html, 'html.parser')

for link in bs.find('div', {'id': 'bodyContent'}).find_all(
    'a', href=re.compile('^(/wiki/)((?!:).)*$')):
    if 'href' in link.attrs:
        print(link.attrs['href'])
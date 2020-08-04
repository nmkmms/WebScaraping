from urllib.request import urlopen
from bs4 import BeautifulSoup as bsoup
import re

url = 'http://www.pythonscraping.com/pages/page3.html'

html = urlopen(url)
bs = bsoup(html, 'html.parser')

images = bs.find_all('img',
    {'src': re.compile('\.\.\/img\/gifts\/img.*\.jpg')})
for image in images:
    print(image['src'])

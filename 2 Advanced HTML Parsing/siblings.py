from urllib.request import urlopen
from bs4 import BeautifulSoup as bsoup

url = 'http://www.pythonscraping.com/pages/page3.html'

html = urlopen(url)
bs = bsoup(html, 'html.parser')

giftList = bs.find('table', {'id': 'giftList'})
for sibling in giftList.tr.next_siblings:
    print(sibling)
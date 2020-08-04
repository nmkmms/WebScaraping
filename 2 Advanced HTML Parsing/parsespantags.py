from urllib.request import urlopen
from bs4 import BeautifulSoup as bsoup

url = 'http://www.pythonscraping.com/pages/warandpeace.html'

html = urlopen(url)
bs = bsoup(html, 'html.parser')

nameList = bs.find_all('span', {'class': 'green'})
for name in nameList:
    print(name.get_text())

nameList = bs.find_all(text='the prince')
print(f'"the prince" frequency: {len(nameList)}')

title = bs.find(id='title')
print(f'Title: {title}')
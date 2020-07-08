from urllib.request import urlopen
from bs4 import BeautifulSoup as bsoup

url = 'http://www.pythonscraping.com/pages/page3.html'

html = urlopen(url)
bs = bsoup(html, 'html.parser')

print(bs.find('img',
              {'src': '../img/gifts/img1.jpg'})
      .parent.previous_sibling.get_text())
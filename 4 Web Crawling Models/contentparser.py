import requests
from bs4 import BeautifulSoup


class Content:
    def __init__(self, url, title, body):
        self.url = url
        self.title = title
        self.body = body

def getPage(url):
    req = requests.get(url)
    return BeautifulSoup(req.text, 'html.parser')
    

def scrapeNYTimes(url):
    bs = getPage(url)
    title = bs.find('h1').text
    lines = bs.find_all('p', {'class': 'story-content'})
    body = '\n'.join([line.text for line in lines])
    return Content(url, title, body)


def scrapeBrookings(url):
    bs = getPage(url)
    title = bs.find('h1').text
    body = bs.find('div', {'class': 'blog-content'}).text
    return Content(url, title, body)


BrUrl = 'https://www.brookings.edu/blog/future-development' \
'/2018/01/26/delivering-inclusive-urban-access-3-unc' \
'omfortable-truths/'

br_content = scrapeBrookings(BrUrl)
print(f'Title: {br_content.title}')
print(f'URL: {br_content.url}')
print(br_content.body)

NYUrl = 'https://www.nytimes.com/2018/01/25/opinion/sunday/' \
'silicon-valley-immortality.html' 

ny_content = scrapeBrookings(BrUrl)
print(f'Title: {ny_content.title}')
print(f'URL: {ny_content.url}')
print(ny_content.body)

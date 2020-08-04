import requests
from bs4 import BeautifulSoup

class Content:
    """Common base class for all articles/pages."""

    def __init__(self, topic, title, body, url):
        self.topic = topic
        self.title = title
        self.body = body
        self.url = url

    def print(self):
        """Flexible printing function controls output."""
        print(f'New article found for topic: {self.topic}')
        print(f'TITLE: {self.title}')
        # print(f'BODY:\n{self.body}')
        print(f'URL: {self.url}')


class Website:
    """Contains info about website structure."""

    def __init__(self, name, url, searchUrl, resultListing,
    resultUrl, absoluteUrl, titleTag, bodyTag):
        self.name = name
        self.url = url
        self.searchUrl = searchUrl
        self.resultListing = resultListing
        self.resultUrl = resultUrl
        self.absoluteUrl = absoluteUrl
        self.titleTag = titleTag
        self.bodyTag = bodyTag

class Crawler:

    def getPage(self, url):
        try:
            req = requests.get(url)
        except requests.exceptions.RequestException:
            return None
        return BeautifulSoup(req.text, 'html.parser')

    def safeGet(self, pageObj, selector):
        childObj = pageObj.select(selector)
        if childObj is not None and len(childObj):
            return childObj[0].get_text()
        return ''

    def search(self, topic, site):
        """Search a given website for a givem topic.
        
        Records all pages found.
        """
        bs = self.getPage(site.searchUrl + topic)
        searchResults = bs.select(site.resultListing)
        for result in searchResults:
            url = result.select(site.resultUrl)[0].attrs['href']
            # Check to see whether it's a relative or an abs URL
            if site.absoluteUrl:
                bs = self.getPage(url)
            else:
                bs = self.getPage(site.url + url)

            if bs is None:
                print('Something was wrong with that page or URL. Skipping!')
                return

            title = self.safeGet(bs, site.titleTag)
            body = self.safeGet(bs, site.bodyTag)
            if title and body:
                content = Content(topic, title, body, url)
                content.print()


crawler = Crawler()

siteData = [
    ['O\'Reilly Media', 'http://oreilly.com',
        'https://ssearch.oreilly.com/?q=','article.product-result',
        'p.title a', True, 'h1', 'section#product-description'],
    ['Reuters', 'http://reuters.com',
        'http://www.reuters.com/search/news?blob=',
        'div.search-result-content','h3.search-result-title a',
        False, 'h1', 'div.StandardArticleBody_body_1gnLA'],
    ['Brookings', 'http://www.brookings.edu',
        'https://www.brookings.edu/search/?s=',
        'div.list-content article', 'h4.title a', True, 'h1',
        'div.post-body']
]
sites = list(map(lambda row: Website(*row), siteData))
topics = ['python', 'data science']

for topic in topics:
    print(f"GETTING INFO ABOUT: {topic}")
    for targetSite in sites:
        crawler.search(topic, targetSite)
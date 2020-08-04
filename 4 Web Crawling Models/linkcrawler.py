import re
import requests
from collections import namedtuple
from bs4 import BeautifulSoup

# Define Website class
Website = namedtuple('Website', 'name url targetPattern absoluteUrl titleTag bodyTag')

class Content:
    def __init__(self, url, title, body):
        self.url = url
        self.title = title
        self.body = body

    def print(self):
        print(f'URL: {self.url}')
        print(f'TITLE: {self.title}')
        print(f'BODY: {self.body}')

class Crawler:
    def __init__(self, site: Website):
        self.site = site
        self.visited = set()

    def getPage(self, url):
        try:
            req = requests.get(url)
        except requests.exceptions.RequestException:
            return None
        return BeautifulSoup(req.text, 'html.parser')

    def safeGet(self, pageObj, selector):
        selectedElems = pageObj.select(selector)
        if selectedElems is not None and len(selectedElems):
            return '\n'.join([elem.get_text() for elem in selectedElems])
        return ''

    def parse(self, url):
        bs = self.getPage(url)
        if bs is not None:
            title = self.safeGet(bs, self.site.titleTag)
            body = self.safeGet(bs, self.site.bodyTag)
            if title and body:
                content = Content(url, title, body)
                content.print()

    def crawl(self):
        """
        Get pages from website home page.
        """
        bs = self.getPage(self.site.url)
        targetPages = bs.findAll('a', 
            href=re.compile(self.site.targetPattern))
        # print(targetPages)
        for targetPage in targetPages:
            targetPage = targetPage.attrs['href']
            if targetPage not in self.visited:
                self.visited.add(targetPage)
                if not self.site.absoluteUrl:
                    targetPage = f'{self.site.url}{targetPage}'
                self.parse(targetPage)


reuters = Website('Reuters', 'https://www.reuters.com',
    '^(/article/)', False, 'h1', 'div.StandardArticleBody_body')
crawler = Crawler(reuters)
crawler.crawl()

import requests
from bs4 import BeautifulSoup

class Content:
    """
    Common base class for all articles/pages.
    """

    def __init__(self, url, title, body):
        self.url = url
        self.title = title
        self.body = body

    def print(self):
        """
        Flexible printing function controls output.
        """
        print(f'URL: {self.url}')
        print(f'Title: {self.title}')
        print(f'Body: {self.body}')


class Website:
    """
    Contains information about website structure.
    """

    def __init__(self, name, url, titleTag, bodyTag):
        self.name = name
        self.url = url
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
        """
        Utility function used to get a content string from a
        BeautifulSoup object and a selector. Returns an empty
            string if no object is found for the given selector.
        """
        selectedElems = pageObj.select(selector)
        if selectedElems:
            return '\n'.join(
                [elem.get_text() for elem in selectedElems]
            )
        return ''

    def parse(self, site, url):
        """
        Extract content from a given page URL.
        """
        bs = self.getPage(url)
        if bs:
            title = self.safeGet(bs, site.titleTag)
            body = self.safeGet(bs, site.bodyTag)
            if title is not None and body is not None:
                content = Content(url, title, body)
                content.print()


crawler = Crawler()

siteData = [
    ['O\'Reilly Media', 'http://oreilly.com',
        'h1', 'div.title-description'],
    ['Reuters', 'http://reuters.com', 'h1',
        'div.StandardArticleBody_body'],
    ['Brookings', 'http://www.brookings.edu',
        'h1', 'div.post-body'],
    ['New York Times', 'http://nytimes.com',
        'h1', 'section.meteredContent']
]
websites = list(map(lambda row: Website(*row), siteData))
# for web in websites:
#     print(web.name, web.url, web.titleTag, web.bodyTag)

pages = [
    'http://shop.oreilly.com/product/0636920028154.do',
    'http://www.reuters.com/article/us-usa-epa-pruitt-idUSKBN19W2D0',
    'https://www.brookings.edu/blog/'\
'techtank/2016/03/01/idea-to-retire-old-methods-of-policy-education/',
    'https://www.nytimes.com/2018/01/'\
'28/business/energy-environment/oil-boom.html'
]

for i, page in enumerate(pages):
    crawler.parse(websites[i], page)
    print('\n\n\n')
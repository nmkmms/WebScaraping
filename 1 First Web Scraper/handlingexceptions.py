from urllib.request import urlopen
from urllib.error import HTTPError
from urllib.error import URLError

try:
    html = urlopen('http://www.pythonscraping.com/pages/page1.html')
except HTTPError as e:
    print(e)
    # return null, break, or do some other "plan B"
except URLError as e:
    print('The server could not be found!')
else:
    # program continues. Note: If you return or break in the
    # exception catch, you do not need to use th "else" statement
    print(html.read())
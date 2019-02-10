from parsers.baseparser import BaseParser

from BeautifulSoup import BeautifulSoup, Tag


class DiePresseParser(BaseParser):
    categories = [
        'innenpolitik',
        'ausland',
        'wirtschaft',
        'panorama',
        'kultur',
        'meinung',
        'techscience',
        'sport',
        'motor',
        'schaufenster',
        'bildung',
        'karriere',
        'recht',
        'zeitgeschichte',
        'science',
        'immobilien',
    ]

    domains = ["www.diepresse.com"]
    feeder_pat = "^https?://diepresse.com/home/.*/\d+/(?!.*#kommentare)"
    feeder_pages = ['http://diepresse.com/home/' + category for category in categories]

    def _parse(self, html):
        soup = BeautifulSoup(html, convertEntities=BeautifulSoup.HTML_ENTITIES, fromEncoding='utf-8')
        self.meta = soup.findAll('meta')

        # fill in title
        title = soup.find('h1', 'article__headline')
        if title is None:
            self.real_article = False
            return
        self.title = title.getText()
        self.date = soup.find('meta', attrs={'property': 'article:published_time'}).get('content')

        # fill in author
        author = soup.find('a', attrs={'class': 'article__author'})
        if author is None:
            self.byline = "nicht genannt"
        else:
            self.byline = author.text.strip()

        div = soup.find('div', 'article__body')

        self.body = '\n' + '\n\n'.join([x.getText() for x in div.childGenerator()
                                        if isinstance(x, Tag) and x.name == 'p'])

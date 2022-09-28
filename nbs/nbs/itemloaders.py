from scrapy.loader import ItemLoader
from  w3lib.html import remove_tags
import unicodedata
from html import unescape
from itemloaders.processors import MapCompose, TakeFirst


def clean_html(html):

        c_html = []
        for p in html:
            pp = remove_tags(p)
            pp = ' '.join(pp.split())
            c_html.append(pp)
        html = unicodedata.normalize("NFKD",' '.join(c_html))
        html = unescape(html)
        html = html.strip()
        return html

def clean_date(date):
    return date.replace('. ', '-')

def clean_urls(urls):
    clean_urls = []
    for url in urls:
        if url.startswith('/'):
            url = 'https://nbs.sk' + url
        if url == '#':
            continue
        clean_urls.append(url)
    return [clean_urls]

class nbsLoader(ItemLoader):

    default_output_processor = TakeFirst()
    body_in = MapCompose(clean_html)
    date_in = MapCompose(clean_date)
    links_in = MapCompose(clean_urls)
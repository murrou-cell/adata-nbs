import requests
import scrapy
from scrapy import Selector, Request
import json
from nbs.items import NbsItem
from nbs.itemloaders import nbsLoader


class NbsSpider(scrapy.Spider):
    name = 'nbs_article'
    
    def start_requests(self):
        urls = ['https://nbs.sk/en/press/news-overview/']
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse_links)

    def post_call(self,gbconfig):
        payload = json.dumps({
            "gbConfig": json.dumps(gbconfig),
            "lang": "en",
            "limit": 20,
            "offset": 0,
            "filter": {
                "lang": "en"
            },
            "onlyData": True
            })
        
        headers = {'Content-Type': 'application/json'}
        
        return requests.post(
            url = 'https://nbs.sk/wp-json/nbs/v1/post/list?_locale=user',
            data=payload,
            headers=headers
        )

    def parse_links(self,response):
        selector = 'div[data-name="post-list"]'
        xhrData = response.css(selector)

        data_gbconfig=xhrData.css("::attr(data-gbconfig)").get()

        resp = self.post_call(data_gbconfig)

        jresp = json.loads(resp.text)['html']

        jresp = Selector(text=jresp)
        
        items = jresp.css('a.archive-results__item')

        for item in items:
            link = item.css("::attr(href)").get()
            name = item.css("h2::text").get()
            date = item.css("div.date::text").get()
            yield Request(link, callback=self.parse_body, 
                  meta= {'name': name, 'url': link, 'date': date})

    def parse_body(self, response):
        excl = [
            response.status == 200,
            response.meta['url'].find('/dokument/') == -1,# WE DON'T NEED DOCS
            response.meta['url'].find('https://nbs.sk/') != -1# WE NEED ARTICLES FROM nbs
        ]
        if all(excl):
            date = response.meta['date']
            name = response.meta['name']
            link = response.meta['url']

            base = response.css('div.nbs-content') 
            internal_links = base.css('a')
            links = []
            for a in internal_links:
                links.append(a.css("::attr(href)").get())

            labels = response.css('ul.menu--labels').css('div.label')
            labels_done = []
            for label in labels:
                labels_done.append(label.css("::text").get())

            html = base.css('p').getall()
            if len(html) < 1:
                html = response.css('article.nbs-post').css('p').getall()

            nbslo = nbsLoader(item=NbsItem())

            nbslo.add_value('title', name)
            nbslo.add_value('body', [html])
            nbslo.add_value('date', date)
            nbslo.add_value('url', link)
            nbslo.add_value('labels', [labels_done])
            nbslo.add_value('links', [links])

            yield nbslo.load_item()

        

import re
import json
import scrapy
from pprint import pprint
from bs4 import BeautifulSoup as bs

from ..items import SiteParserItem

'''
Проверить!
'''
class TwelvestoreezSpider(scrapy.Spider):
    name = "twelvestoreez"
    allowed_domains = ["12storeez.com"]
    start_urls = ["https://12storeez.com/sitemap.xml"]

    def parse(self, response):
        soup = bs(response.text, 'xml')
        table = [i.text for i in soup.findAll('loc')]
        products = sum(list(filter(None, [re.findall(r'https://12storeez.com/catalog/.*', i) for i in table])), [])
        for product_link in products:
            yield scrapy.Request(
                url=product_link,
                callback=self.parse_product,
                errback=self.handle_error
            )

    def parse_product(self, response):
        data = SiteParserItem()
        try:
            if response.css('div.catalog-grid') is None:
                rez = json.loads(response.css('body script::text').get())
                data['is_available'] = True if response.css(
                    'span.ProductSalePoint-module__subscribeNoteTitle___1auhG::text').get() != 'Товар продан' else False
                data['item_name'] = rez['name']
                data['item_price'] = int(round(float(rez['offers'][0]['price'])))
                data['item_image'] = rez['image']
                data['source_url'] = response.url
                return data
        except Exception as e:
            pprint({
                'error': e,
                'url': response.url
            })

    def handle_error(self, failure):
        pass

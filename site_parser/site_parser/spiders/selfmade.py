import re
import scrapy
from bs4 import BeautifulSoup as bs

from ..items import SiteParserItem


class SelfmadeSpider(scrapy.Spider):
    name = "selfmade"
    allowed_domains = ["selfmade.ru"]
    start_urls = ["https://selfmade.ru/sitemap.xml"]

    def parse(self, response):
        soup = bs(response.text, 'xml')
        table = [i.text for i in soup.findAll('loc')]
        products = sum(list(filter(None, [re.findall(r'https://selfmade.ru/product/.*', i) for i in table])), [])
        for product_link in products:
            yield scrapy.Request(
                url=product_link,
                callback=self.product_id_parser,
                errback=self.handle_error
            )

    def product_id_parser(self, response):
        product_id = int(response.css('div::attr("data-recently-view")').get())
        yield scrapy.Request(
            url=f'https://selfmade.ru/products_by_id/{product_id}.json',
            callback=self.parse_product,
            errback=self.handle_error,
            method='POST'
        )

    def parse_product(self, response):
        data = SiteParserItem()
        rez = response.json()['products'][0]
        data['is_available'] = True
        data['item_name'] = rez['title']
        if int(round(float(rez['price_min']))) == int(round(float(rez['price_max']))):
            data['item_price'] = int(round(float(rez['price_min'])))
        else:
            data['item_price'] = int(round(float(rez['price_man'])))
        data['item_image'] = rez['images'][0]['original_url']
        data['source_url'] = response.urljoin(rez['url'])
        return data

    def handle_error(self, failure):
        pass

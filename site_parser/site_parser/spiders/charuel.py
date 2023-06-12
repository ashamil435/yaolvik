import re
import scrapy
from bs4 import BeautifulSoup as bs

from ..items import SiteParserItem

class CharuelSpider(scrapy.Spider):
    name = "charuel"
    allowed_domains = ["www.charuel.ru"]
    start_urls = ["https://www.charuel.ru/sitemap.xml"]

    def parse(self, response):
        soup = bs(response.text, 'xml')
        table = [i.text for i in soup.findAll('loc')]
        products = sum(list(filter(None, [re.findall(r'https://www.charuel.ru/catalogue/.*', i) for i in table])), [])
        for product_link in products:
            yield scrapy.Request(
                url=product_link,
                callback=self.parse_product,
                errback=self.handle_error
            )

    def parse_product(self, response):
        data = SiteParserItem()
        if response.css('div.product').get() is not None:
            if response.css('div.product__price-current::text').get().rstrip() == '':
                data['is_available'] = False
                data['item_price'] = None
            else:
                data['is_available'] = True
                data['item_price'] = int(response.css('div.product__price-current::text').get().replace(' руб.', '').replace(' ', '').strip())
            data['item_name'] = response.css('h1.product__title::text').get().strip()
            data['item_image'] = response.css('meta[property="og:image"]::attr(content)').get().strip()
            data['source_url'] = response.url
            return data

    def handle_error(self, failure):
        pass

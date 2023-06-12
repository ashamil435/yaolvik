import re
import scrapy
from bs4 import BeautifulSoup as bs

from ..items import SiteParserItem


class ZarinaSpider(scrapy.Spider):
    name = "zarina"
    allowed_domains = ["zarina.ru"]
    start_urls = ["https://zarina.ru/sitemap-iblock-20.xml"]

    def parse(self, response):
        soup = bs(response.text, 'xml')
        table = [i.text for i in soup.findAll('loc')]
        products = sum(list(filter(None, [re.findall(r'https://zarina.ru/catalog/product/.*', i) for i in table])), [])
        for product_link in products:
            yield scrapy.Request(
                url=product_link,
                callback=self.parse_product,
                errback=self.handle_error
            )

    def parse_product(self, response):
        data = SiteParserItem()
        data['is_available'] = True
        data['item_price'] = int(response.css('div.product__price-current::text').get().strip().replace(' ₽', ''))
        data['item_name'] = response.css('h1.product__title::text').get()
        data['item_image'] = response.css('div.product__media-item img::attr("data-src")').get()
        data['source_url'] = response.url
        return data

    def handle_error(self, failure):
        pass
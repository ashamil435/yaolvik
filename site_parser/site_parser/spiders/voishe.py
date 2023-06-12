import re
import scrapy
from bs4 import BeautifulSoup as bs

from ..items import SiteParserItem


class VoisheSpider(scrapy.Spider):
    name = "voishe"
    allowed_domains = ["www.voishe.ru"]
    start_urls = ["https://www.voishe.ru/sitemap-store.xml"]

    def parse(self, response):
        soup = bs(response.text, 'xml')
        products = [i.text for i in soup.findAll('loc')]
        for product_link in products:
            yield scrapy.Request(
                url=product_link,
                callback=self.parse_product,
                errback=self.handle_error
            )

    def parse_product(self, response):
        data = SiteParserItem()
        data['is_available'] = True
        data['item_name'] = response.css('h1.js-store-prod-name::text').get().strip()
        data['item_price'] = int(round(float(response.css('div.js-store-prod-price-val::text').get().strip().replace(',', '.'))))
        data['item_image'] = re.findall(r'url\((.*?)\)', response.css('div.t-container div.js-product-img').get())[0]
        data['source_url'] = response.url
        return data

    def handle_error(self, failure):
        pass

import re
import scrapy
from bs4 import BeautifulSoup as bs

from ..items import SiteParserItem


class CharmstoreSpider(scrapy.Spider):
    name = "charmstore"
    allowed_domains = ["charmstore.club"]
    start_urls = ["https://charmstore.club/sitemap-iblock-37.xml"]

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
        if response.css('div.product-info') and response.url != 'https://charmstore.club/product/dostavka_zakaza/':
            data['is_available'] = True
            data['item_name'] = response.css('div.adaptive-block div.title::text').get().strip()
            data['item_price'] = int((response.css('span.price_value::text').get().replace('\xa0', '').strip()))
            data['item_image'] = response.urljoin(response.css('div.swiper-slide--img-wrapper img::attr("data-src")').get())
            data['source_url'] = response.url
            return data

    def handle_error(self, failure):
        pass


import scrapy
from bs4 import BeautifulSoup as bs

from ..items import SiteParserItem


class CantikhandSpider(scrapy.Spider):
    name = "cantikhand"
    allowed_domains = ["cantikhand.com"]
    start_urls = ["https://cantikhand.com/sitemap-store.xml"]

    def parse(self, response):
        soup = bs(response.text, 'xml')
        products = [i.text for i in soup.findAll('loc')]
        products.pop(0)
        for product_link in products:
            yield scrapy.Request(
                url=product_link,
                callback=self.parse_product,
                errback=self.handle_error
            )

    def parse_product(self, response):
        data = SiteParserItem()
        data['is_available'] = True
        data['item_name'] = response.css('meta[property="og:description"]::attr(content)').get().strip()
        data['item_price'] = int(round(float(response.css('meta[itemprop="price"]::attr(content)').get().strip())))
        data['item_image'] = response.css('meta[property="og:image"]::attr(content)').get().strip()
        data['source_url'] = response.url
        return data

    def handle_error(self, failure):
        pass

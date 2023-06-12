import scrapy
from bs4 import BeautifulSoup as bs

from ..items import SiteParserItem


class SobrightdressSpider(scrapy.Spider):
    name = "sobrightdress"
    allowed_domains = ["sobrightdress.com"]
    start_urls = ["https://sobrightdress.com/sitemap-store.xml"]

    def parse(self, response):
        soup = bs(response.text, 'xml')
        products = [i.text for i in soup.findAll('loc')]
        products.remove('https://sobrightdress.com/catalog/tproduct/1-295804020251-dostavka-do-punkta-vidachi')
        products.remove('https://sobrightdress.com/catalog/tproduct/1-163249288331-doplata')
        for product_link in products:
            yield scrapy.Request(
                url=product_link,
                callback=self.parse_product,
                errback=self.handle_error
            )

    def parse_product(self, response):
        data = SiteParserItem()
        data['is_available'] = True
        data['item_name'] = response.css('meta[property="og:title"]::attr(content)').get().strip()
        data['item_price'] = int(round(float(response.css('meta[itemprop="price"]::attr(content)').get().strip())))
        data['item_image'] = response.css('meta[itemprop="image"]::attr(content)').get().strip()
        data['source_url'] = response.url
        return data

    def handle_error(self, failure):
        pass

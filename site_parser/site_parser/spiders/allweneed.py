import re
import scrapy
from bs4 import BeautifulSoup as bs

from ..items import SiteParserItem


class AllweneedSpider(scrapy.Spider):
    name = "allweneed"
    allowed_domains = ["allweneed.ru"]
    start_urls = ["https://allweneed.ru/sitemap.xml"]

    def parse(self, response):
        soup = bs(response.text, 'xml')
        table = [i.text for i in soup.findAll('loc')]
        products = ['https://api.allweneed.ru/api/ru/catalog/products/' + i.split('/')[-1] for i in
                    sum(list(filter(None, [re.findall(r'https://allweneed.ru/product/.*', i) for i in table])), [])]
        for product_link in products:
            yield scrapy.Request(
                url=product_link,
                callback=self.parse_product,
                errback=self.handle_error
            )

    def parse_product(self, response):
        data = SiteParserItem()
        data['is_available'] = response.json()['in_stock']
        data['item_price'] = int(round(float(response.json()['price'])))
        data['item_name'] = response.json()['title']
        name = response.json()['slug']
        data['item_image'] = response.urljoin(response.json()['image'])
        category = response.json()['category']['slug']
        data['source_url'] = f'https://allweneed.ru/product/{category}/{name}'
        return data

    def handle_error(self, failure):
        pass


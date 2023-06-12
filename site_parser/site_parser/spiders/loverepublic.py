import re
import scrapy
from bs4 import BeautifulSoup as bs

from ..items import SiteParserItem


class LoverepublicSpider(scrapy.Spider):
    name = "loverepublic"
    allowed_domains = ["loverepublic.ru"]
    start_urls = ["https://loverepublic.ru/upload/sitemap-iblock-4.xml",
                  "https://loverepublic.ru/upload/sitemap-iblock-46.xml"]

    def parse(self, response):
        soup = bs(response.text, 'xml')
        table = [i.text for i in soup.findAll('loc')]
        products = sum(list(filter(None, [re.findall(r'https://loverepublic.ru/catalog/.*', i) for i in table])), [])
        for product_link in products:
            yield scrapy.Request(
                url=product_link,
                callback=self.product_id_parser,
                errback=self.handle_error
            )

    def product_id_parser(self, response):
        if response.css('article.catalog-element').get() is not None:
            product_id = int(response.css('article.catalog-element::attr("data-id")').get())
            yield scrapy.Request(
                url=f'https://api.loverepublic.ru/web/v1/catalog/products/{product_id}/stock',
                callback=self.parse_product,
                errback=self.handle_error
            )

    # noinspection PyTypeChecker
    def parse_product(self, response):
        data = SiteParserItem()
        rez: dict = response.json()
        data['is_available'] = rez['data']['isAvailable']
        data['item_name'] = rez['data']['detailName'].strip()
        data['item_price'] = int(rez['data']['sku'][0]['properties']['starayaTsena']['value'])
        data['item_image'] = next((link for link in rez['data']['images']['original'] if link.endswith('_0.jpg')), None)
        data['source_url'] = response.urljoin(rez['data']['link'])
        return data

    def handle_error(self, failure):
        pass


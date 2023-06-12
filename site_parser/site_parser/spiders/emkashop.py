import re
import scrapy

from ..items import SiteParserItem


class EmkashopSpider(scrapy.Spider):
    name = 'emkashop'
    allowed_domains = ['emkashop.ru']
    start_urls = ['https://emkashop.ru/catalog']

    def parse(self, response):
        pages = int(re.findall(r'\d{2}', response.css('div.pager li a::attr("href")').getall()[-1])[0])
        table = [response.url + f'?page={i}' for i in range(1, pages+1)]
        for catalog_page in table:
            yield scrapy.Request(
                url=catalog_page,
                callback=self.parse_catalog,
                errback=self.handle_error
            )

    def parse_catalog(self, response):
        data = SiteParserItem()
        for product in response.css('div.catalog div.lazy'):
            data['is_available'] = True
            data['item_name'] = product.css('span.always-hide::text').get().strip()
            data['item_price'] = int(product.css('div.product-price span::text').get().replace(' ', ''))
            data['item_image'] = product.css('div.img-elem img::attr("src")').get()
            data['source_url'] = product.css('div.img-elem a::attr("href")').get().strip()
            yield data


    def handle_error(self, failure):
        pass
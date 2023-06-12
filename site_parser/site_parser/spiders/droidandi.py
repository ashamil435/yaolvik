import scrapy
from pprint import pprint

from ..items import SiteParserItem


class DroidandiSpider(scrapy.Spider):
    name = "droidandi"
    allowed_domains = ["droidandi.com"]
    start_urls = [f"https://droidandi.com/collection/all?page={i}" for i in range(1, 30)]

    def parse(self, response):
        data = SiteParserItem()
        table = response.css('div.catalog-list div.product-preview__content')
        for product in table:
            try:
                if product.css('span.product-preview__price-cur::text').get() is None:
                    data['is_available'] = False
                    data['item_price'] = None
                else:
                    data['is_available'] = True
                    data['item_price'] = int(product.css('span.product-preview__price-cur::text ').get().strip().replace('\xa0', '').replace('₽', '').replace(' ', ''))
                data['item_name'] = product.css('div.product-preview__title a::text').get()
                data['item_image'] = product.css('div.img-ratio__inner source::attr("data-srcset")').get()
                data['source_url'] = response.urljoin(product.css('div.img-ratio__inner a::attr("href")').get())
                yield data
            except Exception as e:
                pprint({
                    'error': e,
                    'page': response.url,
                    'url': response.urljoin(product.css('div.img-ratio__inner a::attr("href")').get())
                })
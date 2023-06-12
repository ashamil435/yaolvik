import scrapy

from ..items import SiteParserItem


class NudestorySpider(scrapy.Spider):
    name = "nudestory"
    allowed_domains = ["nudestory.ru"]
    start_urls = [f"https://nudestory.ru/catalog/?PAGEN_3={i}" for i in range(1, 35)]

    def parse(self, response):
        data = SiteParserItem()
        table = response.css('div.catalog__content-items div.catalog__item')
        for product in table:
            data['is_available'] = True
            data['item_name'] = product.css('a.catalog__item--link p.main-new__desc::text').get().strip()
            data['item_price'] = int(response.css('a.catalog__item--link p.main-new__price::text').get().strip().replace('\xa0', '').replace(' руб.', '').replace(' ', ''))
            data['item_image'] =  response.urljoin(product.css('img::attr("src")').get())
            data['source_url'] = response.urljoin(product.css('a.catalog__item--link::attr("href")').get())
            yield data

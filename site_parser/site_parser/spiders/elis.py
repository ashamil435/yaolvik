import scrapy

from ..items import SiteParserItem

class ElisSpider(scrapy.Spider):
    name = "elis"
    allowed_domains = ["elis.ru"]
    start_urls = [f"https://elis.ru/catalog/?PAGEN_1={i}" for i in range(1, 52)]

    def parse(self, response):
        data = SiteParserItem()
        table = response.css('div.catalog__grid div.card')
        for product in table:
            data['is_available'] = True
            data['item_name'] = product.css('a.card__title ::text').get()
            data['item_price'] = int(response.css('span.card__price::text').get().strip().replace(' ₽', '').replace(' ', ''))
            data['item_image'] = response.urljoin(product.css('img.swiper-slide::attr("src")').get())
            data['source_url'] = response.urljoin(product.css('a.card__title::attr("href")').get())
            yield data
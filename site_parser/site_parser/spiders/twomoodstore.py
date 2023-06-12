import scrapy

from ..items import SiteParserItem


class TwomoodstoreSpider(scrapy.Spider):
    name = "twomoodstore"
    allowed_domains = ["www.2moodstore.com"]
    start_urls = [f"https://www.2moodstore.com/collection/all/?PAGEN_1={i}" for i in range(1, 31, 1)]

    def parse(self, response):
        data = SiteParserItem()
        table = response.css('div.cards-row div.card-info')
        for product in table:
            data['is_available'] = True
            data['item_name'] = product.css('div.card-title a::text').get()
            data['item_price'] = product.css('div.card-prices span.card-price::text').get().replace('\xa0', '').replace('₽', '').replace(' ', '').strip()
            data['item_image'] = product.css('img::attr("src")').get()
            data['source_url'] = response.urljoin(product.css('div.card-title a::attr("href")').get())
            yield data


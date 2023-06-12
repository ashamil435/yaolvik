import scrapy

from ..items import SiteParserItem


class Studio29Spider(scrapy.Spider):
    name = "studio29"
    allowed_domains = ["studio-29.ru"]
    start_urls = [f"https://studio-29.ru/catalog/?PAGEN_2={i}" for i in range(1, 14)]

    def parse(self, response):
        data = SiteParserItem()
        table = response.css('div.catalog div.item_block')
        for product in table:
            data['is_available'] = True
            data['item_name'] = product.css('div.text a::text').get().strip()
            data['item_price'] = int(
                response.css('div.price span.values_wrapper::text').get().strip().replace('\xa0', '').replace(' ₽', '').replace(' ', ''))
            data['item_image'] = response.urljoin(product.css('div.images img::attr("src")').get())
            data['source_url'] = response.urljoin(product.css('div.cat-img a::attr("href")').get())
            yield data

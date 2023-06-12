import re
import scrapy
from bs4 import BeautifulSoup as bs

from ..items import SiteParserItem


class TottiShopSpider(scrapy.Spider):
    name = "totti_shop"
    allowed_domains = ["totti-shop.ru"]
    start_urls = ["https://totti-shop.ru/server-sitemap.xml"]

    def parse(self, response):
        soup = bs(response.text, 'xml')
        table = [i.text for i in soup.findAll('loc')]
        products = sum(list(filter(None,
                                   [re.findall(r'https://totti-shop.ru/product-card/.*', i) for i in table])), [])
        for product_link in products:
            yield scrapy.Request(
                url=product_link,
                callback=self.parse_product,
                errback=self.handle_error
            )

    def parse_product(self, response):
        data = SiteParserItem()
        data['is_available'] = True
        data['item_name'] = response.css('h1::text').get()
        data['item_price'] = int(response.css('div.Card_priceBlock__KqZym h1::text').get().replace(' руб.', '').replace(' ', '').strip())
        data['item_image'] = response.urljoin(response.xpath('//*[@id="__next"]/main/div[2]/div/div/div[1]/div[1]/img').css('img::attr("src")').get())
        data['source_url'] = response.url
        return data

    def handle_error(self, failure):
        pass
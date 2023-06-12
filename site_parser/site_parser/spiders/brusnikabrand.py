import scrapy

from ..items import SiteParserItem


class BrusnikabrandSpider(scrapy.Spider):
    name = "brusnikabrand"
    allowed_domains = ["brusnikabrand.com"]
    urls = ['https://brusnikabrand.com/catalog/novinki/',
                  'https://brusnikabrand.com/lookbook/urban-self-expression/',
                  'https://brusnikabrand.com/catalog/sport/',
                  'https://brusnikabrand.com/catalog/linen_collection/',
                  'https://brusnikabrand.com/catalog/platya_kombinezony_1/',
                  'https://brusnikabrand.com/catalog/dzhempery_1/',
                  'https://brusnikabrand.com/catalog/topy_1/',
                  'https://brusnikabrand.com/catalog/bodi/',
                  'https://brusnikabrand.com/catalog/rubashki_1/',
                  'https://brusnikabrand.com/catalog/bryuki_1/',
                  'https://brusnikabrand.com/catalog/dzhinsy/',
                  'https://brusnikabrand.com/catalog/yubki/',
                  'https://brusnikabrand.com/catalog/futbolki_/',
                  'https://brusnikabrand.com/catalog/vodolazki_1/',
                  'https://brusnikabrand.com/catalog/zhakety_/',
                  'https://brusnikabrand.com/catalog/kardigany_/',
                  'https://brusnikabrand.com/catalog/bombery/',
                  'https://brusnikabrand.com/catalog/zhilety_/',
                  'https://brusnikabrand.com/catalog/verkhnyaya_odezhda_1/',
                  'https://brusnikabrand.com/catalog/komplekty_1/',
                  'https://brusnikabrand.com/catalog/shorty/',
                  'https://brusnikabrand.com/catalog/aksessuary_1/',
                  'https://brusnikabrand.com/catalog/deti_1/',
                  'https://brusnikabrand.com/catalog/sale/']

    start_urls = sum(list(map(lambda x: [f"{x}?PAGEN_5={i}" for i in range(1, 11)], urls)), [])

    def parse(self, response):
        data = SiteParserItem()
        table = response.css('div.big-grid div.catalog-item')
        for product in table:
            data['is_available'] = True
            data['item_name'] = product.css('div.catalog-item-title span span::text').get()
            data['item_price'] = int(product.css('div.catalog-item-price span.product-item-price-current::text').get().replace('\xa0', '').replace(
                '₽', '').replace(' ', '').strip())
            data['item_image'] = response.urljoin(product.css('img::attr("src")').get())
            data['source_url'] = response.urljoin(product.css('div.catalog-item a.catalog-item-swiper::attr("href")').get())
            yield data


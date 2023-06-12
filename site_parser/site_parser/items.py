# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class SiteParserItem(scrapy.Item):
    is_available: bool = scrapy.Field()
    item_name: str = scrapy.Field()
    item_price: int = scrapy.Field()
    item_image: str = scrapy.Field()
    source_url: str = scrapy.Field()

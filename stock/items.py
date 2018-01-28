# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class EndOfDocumentItem(scrapy.Item):
	pass

class StockCodeItem(scrapy.Item):
    code = scrapy.Field()
    name = scrapy.Field()
    isin_code = scrapy.Field()
    listed_date = scrapy.Field()
    market_type = scrapy.Field()
    industry_type = scrapy.Field()
    cfi_code = scrapy.Field()
    crawled_at = scrapy.Field()
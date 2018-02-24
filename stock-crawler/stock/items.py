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


class FinancialStatementEntryItem(scrapy.Item):
    title = scrapy.Field()
    statement_date = scrapy.Field()
    stock_code = scrapy.Field()
    metric_index = scrapy.Field()
    metric_name = scrapy.Field()
    metric_value = scrapy.Field()
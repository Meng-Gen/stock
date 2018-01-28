# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

from stock.items import EndOfDocumentItem
from stock.items import StockCodeItem
from stock.stores import StockCodeStore


class StockCodePipeline(object):
    store = StockCodeStore()

    def process_item(self, item, spider):
        if isinstance(item, StockCodeItem):
            self.store.add(item)
        elif isinstance(item, EndOfDocumentItem):
        	self.store.flush()
        return item
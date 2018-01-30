# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

from stock.items import EndOfDocumentItem
from stock.items import FinancialStatementEntryItem
from stock.items import StockCodeItem
from stock.stores import FinancialStatementEntryStore
from stock.stores import StockCodeStore


class StockCodePipeline(object):
    store = StockCodeStore()

    def process_item(self, item, spider):
        """Process the parsed item.

        Process the parsed item. If the item is a StockCodeItem, add it in the
        store as a cached item (going to be flushed into the store). If the
        item is an EndOfDocumentItem, flush all cached items into the store.

        Args:
            item: A StockCodeItem
            spider: A StockCodeSpider
        """
        if isinstance(item, StockCodeItem):
            self.store.add(item)
        elif isinstance(item, EndOfDocumentItem):
            self.store.flush()
        return item


class FinancialStatementEntryPipeline(object):
    store = FinancialStatementEntryStore()

    def process_item(self, item, spider):
        """Process the parsed item.

        Process the parsed item. If the item is a FinancialStatementEntryItem,
        add it in the store as a cached item (going to be flushed into the
        store). If the item is an EndOfDocumentItem, flush all cached items into
        the store.

        Args:
            item: A FinancialStatementEntryItem
            spider: A spider
        """
        if isinstance(item, FinancialStatementEntryItem):
            self.store.add(item)
        elif isinstance(item, EndOfDocumentItem):
            self.store.flush()
        return item
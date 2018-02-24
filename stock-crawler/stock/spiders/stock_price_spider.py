# -*- coding: utf-8 -*-

import json
import re
import scrapy

from datetime import datetime
from stock.items import EndOfDocumentItem
from stock.items import FinancialStatementEntryItem
from stock.stores import StockCodeStore
from stock.utils import datetime_utils
from stock.utils import metric_value_utils


class StockPriceSpider(scrapy.Spider):
    name = "StockPrice"
    custom_settings = {
        'ITEM_PIPELINES': {
            'stock.pipelines.FinancialStatementEntryPipeline': 300
        }
    }

    def start_requests(self):
        stock_codes = StockCodeStore().get()
        for stock_code in stock_codes:
            for date in self._iterate_years():
                url = 'http://www.twse.com.tw/exchangeReport/FMSRFK?response=json&date={date}&stockNo={stock_code}' \
                    .format(date=date, stock_code=stock_code)
                yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        json_response = json.loads(response.body_as_unicode())

        stock_code = self._parse_stock_code(json_response)

        # Parse metric names. The first one represents the year of the trading
        # date and the second one represents the month of the trading date.
        metric_names = json_response['fields']

        for metric_values in json_response['data']:
            if len(metric_values) != len(metric_names):
                raise ValueError(u'Could not parse metric values: {0}'.format(metric_values))

            statement_date = datetime_utils. \
                build_datetime_from_roc_era_and_month(metric_values[0], metric_values[1])

            for i in range(2, len(metric_names)):
                item = FinancialStatementEntryItem()
                item['title'] = u'個股月成交資訊'
                item['statement_date'] = statement_date
                item['stock_code'] = stock_code
                item['metric_index'] = i - 2
                item['metric_name'] = metric_names[i].strip()
                item['metric_value'] = metric_value_utils.normalize(metric_values[i])
                yield item
        yield EndOfDocumentItem()

    def _iterate_years(self):
        start_date = datetime(year=2014, month=1, day=1)
        end_date = datetime.now()
        for each_year in datetime_utils.year_range(start_date, end_date):
            yield each_year.strftime('%Y%m%d')

    def _parse_stock_code(self, json_response):
        """Parse the stock code.

        Get stock codes from JSON document.

        Args:
            json_response: A JSON document.

        Returns:
            A string of stock code.
        """
        title = json_response['title']
        pattern = u'([0-9]+)年([0-9]+) (.+) 月成交資訊'
        stock_code = re.match(pattern, title).group(2)
        return stock_code
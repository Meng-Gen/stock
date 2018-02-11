import json
import scrapy

from datetime import datetime
from stock.items import EndOfDocumentItem
from stock.items import StockPriceItem
from stock.stores import StockCodeStore
from stock.utils import datetime_utils
from stock.utils import metric_value_utils


class StockPriceSpider(scrapy.Spider):
    name = "StockPrice"
    custom_settings = {
        'ITEM_PIPELINES': {
            'stock.pipelines.StockPricePipeline': 300
        }
    }

    def start_requests(self):
        stock_codes = StockCodeStore().get()
        for stock_code in stock_codes:
            for date in self._iterate_months():
                url = 'http://www.tse.com.tw/exchangeReport/STOCK_DAY?response=json&date={date}&stockNo={stock_code}' \
                    .format(date=date, stock_code=stock_code)
                yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        json_response = json.loads(response.body_as_unicode())

        stock_code = self._parse_stock_code(json_response)

        # Parse metric names.
        metric_names = json_response['fields']

        # Parse metric values to build metric map. Then build stock price items
        # for further usage.
        for metric_values in json_response['data']:
            if len(metric_values) != len(metric_names):
                raise ValueError(u'Could not parse metric values: {0}'.format(metric_values))

            metric = {}
            for i in range(len(metric_names)):
                metric[metric_names[i]] = metric_values[i]

            item = StockPriceItem()
            item['code'] = stock_code
            item['date'] = datetime_utils. \
                build_datetime_from_roc_era_with_month_and_day(metric[u'\u65e5\u671f'])
            item['volume'] = metric_value_utils.normalize(metric[u'\u6210\u4ea4\u80a1\u6578'])
            item['open'] = metric_value_utils.normalize(metric[u'\u958b\u76e4\u50f9'])
            item['high'] = metric_value_utils.normalize(metric[u'\u6700\u9ad8\u50f9'])
            item['low'] = metric_value_utils.normalize(metric[u'\u6700\u4f4e\u50f9'])
            item['close'] = metric_value_utils.normalize(metric[u'\u6536\u76e4\u50f9'])
            yield item
        yield EndOfDocumentItem()

    def _iterate_months(self):
        start_date = datetime(year=2017, month=1, day=1)
        end_date = datetime.now()
        for each_month in datetime_utils.month_range(start_date, end_date):
            yield each_month.strftime('%Y%m%d')

    def _parse_stock_code(self, json_response):
        """Parse the stock code.

        Get stock codes from JSON document.

        Args:
            json_response: A JSON document.

        Returns:
            A string of stock code.
        """
        title_tokens = json_response['title'].split()
        if len(title_tokens) != 4:
            raise ValueError(u'Could not parse stock code: {0}'.format(json_response))

        date, stock_code, name, description = title_tokens
        return stock_code

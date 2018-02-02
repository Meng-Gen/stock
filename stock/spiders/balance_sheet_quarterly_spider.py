import scrapy

from stock.items import EndOfDocumentItem
from stock.items import FinancialStatementEntryItem
from stock.stores import StockCodeStore
from stock.utils import datetime_utils
from stock.utils import metric_value_utils


class BalanceSheetQuarterlySpider(scrapy.Spider):
    name = "BalanceSheetQuarterly"
    custom_settings = {
        'ITEM_PIPELINES': {
            'stock.pipelines.FinancialStatementEntryPipeline': 300
        }
    }

    def start_requests(self):
        stock_codes = StockCodeStore().get()
        for stock_code in stock_codes:
            url = 'http://jdata.yuanta.com.tw/z/zc/zcp/zcpa/zcpa_{stock_code}.djhtm' \
                .format(stock_code=stock_code)
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        title, stock_code = self._parse_title_and_stock_code(response)

        XPATH_ROOT = '//*[@id="oMainTable"]/tr'
        rows = response.xpath(XPATH_ROOT)

        # Parse the first row. It is the content of statement dates. The first
        # entry is the name and then the following entries are statement dates.
        name_and_statement_dates = rows[0].xpath('td/text()').extract()

        # Parse the following rest rows. Each row is containing of metrics of
        # different statement dates. The first entry is the name and then the
        # following entries are values.
        for i in range(1, len(rows)):
            name_and_values = rows[i].xpath('td/text()').extract()
            for j in range(1, len(name_and_values)):
                item = FinancialStatementEntryItem()
                item['title'] = title
                item['statement_date'] = datetime_utils. \
                    build_datetime_from_roc_era_with_quarter(name_and_statement_dates[j])
                item['stock_code'] = stock_code
                item['metric_index'] = i - 1
                item['metric_name'] = name_and_values[0]
                item['metric_value'] = \
                    metric_value_utils.normalize(name_and_values[j])
                yield item
        yield EndOfDocumentItem()

    def _parse_title_and_stock_code(self, response):
        """Parse the title and the stock code of the financial statement.

        First, get the string list of titles from the xpath of the scrapy
        response instance.

        The size of the string list should be equal to one. Then parse the
        string representing the title in the format, u'{title}-{stock_code}'.
        For example: u'\u500b\u80a1\u8cc7\u7522\u8ca0\u50b5\u5408\u4f75\u5e74\u8868-2330'.

        Args:
            response: A scrapy response instance.

        Returns:
            A string list of the title and the stock code of the financial
            statement. For example:
            [u'\u500b\u80a1\u8cc7\u7522\u8ca0\u50b5\u5408\u4f75\u5e74\u8868', u'2330']
        """
        XPATH_ROOT = '/html/head/title/text()'

        titles = response.xpath(XPATH_ROOT).extract()
        if len(titles) != 1:
            raise ValueError(u'The length of titles is not equal to 1: {0}'.format(titles))

        title = titles[0]
        title_and_stock_code = title.split('-')
        if len(title_and_stock_code) != 2:
            raise ValueError(u'Could not parse title: {0}'.format(title))

        return title_and_stock_code

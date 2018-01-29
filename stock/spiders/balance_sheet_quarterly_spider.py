import scrapy

from stock.items import EndOfDocumentItem
from stock.items import FinancialStatementItem
from stock.utils import datetime_utils
from stock.utils import metric_value_utils


class BalanceSheetQuarterlySpider(scrapy.Spider):
    name = "BalanceSheetQuarterly"
    custom_settings = {
        'ITEM_PIPELINES': {
            'stock.pipelines.BalanceSheetPipeline': 300
        }
    }

    def start_requests(self):
        urls = [
            'http://jdata.yuanta.com.tw/z/zc/zcp/zcpa/zcpa_2330.djhtm'
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        title, stock_code = self._parse_title_and_stock_code(response)
        unit_of_metric_value = self._parse_unit_of_metric_value(response)

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
                item = FinancialStatementItem()
                item['title'] = title
                item['statement_date'] = datetime_utils. \
                    build_datetime_from_roc_era_with_quarter(name_and_statement_dates[j])
                item['stock_code'] = stock_code
                item['metric_index'] = i - 1
                item['metric_name'] = name_and_values[0]
                item['metric_value'] = \
                    metric_value_utils.normalize(name_and_values[j]) * \
                    unit_of_metric_value
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
            raise ValueError('The length of titles is not equal to 1: {0}'.format(titles))

        title = titles[0]
        title_and_stock_code = title.split('-')
        if len(title_and_stock_code) != 2:
            raise ValueError('Could not parse title: {0}'.format(title))

        return title_and_stock_code

    def _parse_unit_of_metric_value(self, response):
        """Parse the unit of the metric value.

        Get the string of unit from the xpath of the scrapy response instance,
        and parse the string representing the unit in the format, u'\u55ae\u4f4d:{unit}'.
        For example: u'\u55ae\u4f4d:\u767e\u842c'.

        Args:
            response: A scrapy response instance.

        Returns:
            A string of the title of the financial statement. For example:
            u'\u500b\u80a1\u8cc7\u7522\u8ca0\u50b5\u5408\u4f75\u5e74\u8868'.
        """
        XPATH_ROOT = '//*[@id="oScrollHead"]/td/div/text()'

        units = response.xpath(XPATH_ROOT).extract()
        if len(units) != 1:
            raise ValueError('The length of units is not equal to 1: {0}'.format(units))

        unit = units[0]
        if unit == u'\u55ae\u4f4d:\u767e\u842c':
            return 1000000
        else:
            raise ValueError('Could not parse unit: {0}'.format(unit))

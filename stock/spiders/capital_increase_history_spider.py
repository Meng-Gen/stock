import scrapy

from stock.items import EndOfDocumentItem
from stock.items import FinancialStatementEntryItem
from stock.stores import StockCodeStore
from stock.utils import datetime_utils
from stock.utils import metric_value_utils


class CapitalIncreaseHistorySpider(scrapy.Spider):
    name = "CapitalIncreaseHistory"
    custom_settings = {
        'ITEM_PIPELINES': {
            'stock.pipelines.FinancialStatementEntryPipeline': 300
        }
    }

    def start_requests(self):
        stock_codes = StockCodeStore().get()
        for stock_code in stock_codes:
            url = 'http://jdata.yuanta.com.tw/z/zc/zcb/zcb_{stock_code}.djhtm' \
                .format(stock_code=stock_code)
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        title, stock_code = self._parse_title_and_stock_code(response)

        XPATH_ROOT = '//*[@id="SysJustIFRAMEDIV"]/table/tr/td/table/tr/td/table/tr'
        rows = response.xpath(XPATH_ROOT)

        # Parse the first row.  The first entry is the date frame, and then the
        # following entries are metric names.
        date_frame_and_metric_names = rows[1].xpath('td/text()').extract()

        # Parse the following rest rows. Each row is containing of metric
        # values on different month. The first entry is the statement date (a
        # specific month) and then the following entries are metric values.
        for i in range(2, len(rows) - 2):
            statement_date_and_metric_values = rows[i].xpath('td/text()').extract()
            for j in range(1, len(statement_date_and_metric_values)):
                item = FinancialStatementEntryItem()
                item['title'] = title
                item['statement_date'] = datetime_utils. \
                    build_datetime_from_roc_era(statement_date_and_metric_values[0])
                item['stock_code'] = stock_code
                item['metric_index'] = j - 1
                item['metric_name'] = date_frame_and_metric_names[j]
                item['metric_value'] = \
                    metric_value_utils.normalize(statement_date_and_metric_values[j])
                yield item
        yield EndOfDocumentItem()

    def _parse_title_and_stock_code(self, response):
        """Parse the title and the stock code of the financial statement.

        First, get the string list of titles from the xpath of the scrapy
        response instance.

        The size of the string list should be equal to one. Then parse the
        string representing the title in the format, u'{title}-{stock_code}'.
        For example: u'\u500b\u80a1\u640d\u76ca\u5408\u4f75\u8ca1\u5831\u5b63\u8868-2330'.

        Args:
            response: A scrapy response instance.

        Returns:
            A string list of the title and the stock code of the financial
            statement. For example:
            [u'\u500b\u80a1\u640d\u76ca\u5408\u4f75\u8ca1\u5831\u5b63\u8868', u'2330']
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

import scrapy

from stock.items import EndOfDocumentItem
from stock.items import FinancialStatementEntryItem
from stock.stores import StockCodeStore
from stock.utils import datetime_utils
from stock.utils import metric_value_utils


class DividendPolicySpider(scrapy.Spider):
    name = "DividendPolicy"
    custom_settings = {
        'ITEM_PIPELINES': {
            'stock.pipelines.FinancialStatementEntryPipeline': 300
        }
    }

    def start_requests(self):
        stock_codes = StockCodeStore().get()
        for stock_code in stock_codes:
            url = 'http://jdata.yuanta.com.tw/z/zc/zcc/zcc_{stock_code}.djhtm' \
                .format(stock_code=stock_code)
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        title, stock_code = self._parse_title_and_stock_code(response)
        metric_names = self._parse_metric_names(response)

        XPATH_ROOT = '//*[@id="SysJustIFRAMEDIV"]/table/tr/td/table/tr/td/table/td/text()'
        entries = response.xpath(XPATH_ROOT).extract()

        # 9 = num_entry_per_row = one date frame + the number of metric names.
        # We expect that there are 9 entries in each one row.
        num_entry_per_row = len(metric_names) + 1
        if len(entries) % num_entry_per_row != 0:
            raise ValueError(u"Could not parse entries")

        # Parse entries directly. First we divide every entries into rows in
        # sequence. Then the first entry of the row is the statement date, and
        # the rest entries are metric values as usual.
        for i in range(len(entries) // num_entry_per_row):
            for j in range(1, num_entry_per_row):
                item = FinancialStatementEntryItem()
                item['title'] = title
                item['statement_date'] = datetime_utils. \
                    build_datetime_from_year(entries[num_entry_per_row * i])
                item['stock_code'] = stock_code
                item['metric_index'] = j - 1
                item['metric_name'] = metric_names[j - 1].strip()
                item['metric_value'] = \
                    metric_value_utils.normalize(entries[num_entry_per_row * i + j])
                yield item
        yield EndOfDocumentItem()

    def _parse_metric_names(self, response):
        """Parse the date frame and metric names of the financial statement.

        We expect four rows to be parsed. The first row should be the header
        and the second row should be the chart. Therefore we skip them.

        For the third row, the first entry is the date frame, and then the
        following four entries are metric names. The first metric name has
        three sub-metric names listed in the fourth row. The second metric name
        is similar to the first one. The third and the fourth metric names are
        as usual.

        Args:
            response: A scrapy response instance.

        Returns:
            A string list of 8 metric names.
        """
        XPATH_ROOT = '//*[@id="SysJustIFRAMEDIV"]/table/tr/td/table/tr/td/table/tr'
        rows = response.xpath(XPATH_ROOT)
        if len(rows) != 4:
            raise ValueError(u"Could not parse metric names")

        # Use string() instead since the last entry contains <br/> tags.
        # Otherwise, we use text() for speed.
        date_frame_and_metric_names = [_.xpath('string(.)').extract()[0] for _ in rows[2].xpath('td')]
        if len(date_frame_and_metric_names) != 5:
            raise ValueError(u"Could not parse metric names")

        submetric_names = rows[3].xpath('td/text()').extract()
        if len(submetric_names) != 6:
            raise ValueError(u"Could not parse metric names")

        return [
            date_frame_and_metric_names[1] + submetric_names[0],
            date_frame_and_metric_names[1] + submetric_names[1],
            date_frame_and_metric_names[1] + submetric_names[2],
            date_frame_and_metric_names[2] + submetric_names[0],
            date_frame_and_metric_names[2] + submetric_names[1],
            date_frame_and_metric_names[2] + submetric_names[2],
            date_frame_and_metric_names[3],
            date_frame_and_metric_names[4],
        ]

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

import scrapy

from stock.items import StockCodeItem

from datetime import datetime


class StockCodeSpider(scrapy.Spider):
    name = "StockCode"
    custom_settings = {
        'ITEM_PIPELINES': {
            'stock.pipelines.StockCodePipeline': 300
        }
    }

    def start_requests(self):
        urls = [
            'http://isin.twse.com.tw/isin/C_public.jsp?strMode=2',
            'http://isin.twse.com.tw/isin/C_public.jsp?strMode=4'
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        for row in response.xpath('//html/body/table[@class="h4"]/tr'):
            entries = row.xpath('./td/text()').extract()
            if len(entries) != 6: 
                continue
            yield self._build_item(entries)

    def _build_item(self, entries):
        item = StockCodeItem()
        item['code'], item['name'] = self._parse_code_and_name(entries[0])
        item['isin_code'] = entries[1]
        item['listed_date'] = self._parse_listed_date(entries[2])
        item['market_type'] = entries[3]
        item['industry_type'] = entries[4]
        item['cfi_code'] = entries[5]
        return item
            
    def _parse_code_and_name(self, data):
        """Parse the code and the name the specific stock code.

        Parse the string representing the code and the name in the format, 
        u'{code}  {name}'. For example: u'2330  \u53f0\u7a4d\u96fb'.

        Args:
            data: A string combined with he code and the name.

        Returns:
            A string list of the parsed code and the parsed name. For example: 
            [u'2330', u'\u53f0\u7a4d\u96fb'].

        Raises:
            ValueError: An error occurred parsing the code and the name.
        """
        code_and_name = data.split()
        if len(code_and_name) != 2:
            raise ValueError('Could not parse code and name: {0}'.format(data))
        return code_and_name

    def _parse_listed_date(self, data):
        """Parse the listed date of the specific stock code.

        Parse the string representing the date in the format, u'YYYY/MM/DD'.
        For example: u'1962/02/09'.

        Args:
            data: A string of the listed date.

        Returns:
            A datetime instance of the parsed listed date. For example:
            datetime.datetime(1962, 2, 9, 0, 0).
        """
        return datetime.strptime(data, '%Y/%m/%d')

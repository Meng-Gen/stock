# Stock Crawler 

### Installation

  - Web crawling framework: [scrapy](https://scrapy.org/)
  - Database toolkit for python: [sqlalchemy](https://www.sqlalchemy.org/)
  - Powerful extensions to datetime: [dateutil](https://dateutil.readthedocs.io/)

### Setup

Initialize database: stock/stock-crawler/stock/mysql/schema.sql.

### Crawl

Crawl stock code first.
```sh
$ scrapy crawl StockCode
```
As we get a bunch of stock codes, then crawl the rest data
```sh
$ scrapy crawl BalanceSheetQuarterly
$ scrapy crawl BalanceSheetYearly
$ scrapy crawl CapitalIncreaseHistory
$ scrapy crawl CashFlowQuarterly
$ scrapy crawl CashFlowYearly
$ scrapy crawl DividendPolicy
$ scrapy crawl FinancialAnalysisQuarterly
$ scrapy crawl FinancialAnalysisYearly
$ scrapy crawl IncomeStatementQuarterly
$ scrapy crawl IncomeStatementYearly
$ scrapy crawl OperatingRevenue
$ scrapy crawl Profitability
$ scrapy crawl StockPrice
```
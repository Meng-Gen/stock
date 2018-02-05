# -*- coding: utf-8 -*-

# Scrapy settings for stock project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     https://doc.scrapy.org/en/latest/topics/settings.html
#     https://doc.scrapy.org/en/latest/topics/downloader-middleware.html
#     https://doc.scrapy.org/en/latest/topics/spider-middleware.html

BOT_NAME = 'stock'

SPIDER_MODULES = ['stock.spiders']
NEWSPIDER_MODULE = 'stock.spiders'


# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'stock (+http://www.yourdomain.com)'

# Obey robots.txt rules
#ROBOTSTXT_OBEY = True

# Configure maximum concurrent requests performed by Scrapy (default: 16)
#CONCURRENT_REQUESTS = 32

# Configure a delay for requests for the same website (default: 0)
# See https://doc.scrapy.org/en/latest/topics/settings.html#download-delay
# See also autothrottle settings and docs
#DOWNLOAD_DELAY = 3
# The download delay setting will honor only one of:
#CONCURRENT_REQUESTS_PER_DOMAIN = 16
#CONCURRENT_REQUESTS_PER_IP = 16

# Disable cookies (enabled by default)
#COOKIES_ENABLED = False

# Disable Telnet Console (enabled by default)
#TELNETCONSOLE_ENABLED = False

# Override the default request headers:
#DEFAULT_REQUEST_HEADERS = {
#   'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
#   'Accept-Language': 'en',
#}

# Enable or disable spider middlewares
# See https://doc.scrapy.org/en/latest/topics/spider-middleware.html
#SPIDER_MIDDLEWARES = {
#    'stock.middlewares.StockSpiderMiddleware': 543,
#}

# Enable or disable downloader middlewares
# See https://doc.scrapy.org/en/latest/topics/downloader-middleware.html
#DOWNLOADER_MIDDLEWARES = {
#    'stock.middlewares.StockDownloaderMiddleware': 543,
#}

# Enable or disable extensions
# See https://doc.scrapy.org/en/latest/topics/extensions.html
#EXTENSIONS = {
#    'scrapy.extensions.telnet.TelnetConsole': None,
#}

# Configure item pipelines
# See https://doc.scrapy.org/en/latest/topics/item-pipeline.html
#ITEM_PIPELINES = {
#    'stock.pipelines.StockPipeline': 300,
#}

# Enable and configure the AutoThrottle extension (disabled by default)
# See https://doc.scrapy.org/en/latest/topics/autothrottle.html
AUTOTHROTTLE_ENABLED = True
# The initial download delay
AUTOTHROTTLE_START_DELAY = 5
# The maximum download delay to be set in case of high latencies
AUTOTHROTTLE_MAX_DELAY = 60
# The average number of requests Scrapy should be sending in parallel to
# each remote server
AUTOTHROTTLE_TARGET_CONCURRENCY = 1.0
# Enable showing throttling stats for every response received:
#AUTOTHROTTLE_DEBUG = False

# Enable and configure HTTP caching (disabled by default)
# See https://doc.scrapy.org/en/latest/topics/downloader-middleware.html#httpcache-middleware-settings
#HTTPCACHE_ENABLED = True
#HTTPCACHE_EXPIRATION_SECS = 0
#HTTPCACHE_DIR = 'httpcache'
#HTTPCACHE_IGNORE_HTTP_CODES = []
#HTTPCACHE_STORAGE = 'scrapy.extensions.httpcache.FilesystemCacheStorage'

# Configure metadata of financial statement title
STATEMENT_TITLE_METADATA = {
    # consolidated balance sheet (yearly)
    u'\u500b\u80a1\u8cc7\u7522\u8ca0\u50b5\u5408\u4f75\u5e74\u8868': {
        'DateFrame': 'Yearly',
        'Name': 'BalanceSheet',
        'IsSnapshot': True,
        'IsConsolidated': True,
    },
    # consolidated balance sheet (quarterly)
    u'\u500b\u80a1\u8cc7\u7522\u8ca0\u50b5\u5408\u4f75\u8ca1\u5831\u5b63\u8868': {
        'DateFrame': 'Quarterly',
        'Name': 'BalanceSheet',
        'IsSnapshot': True,
        'IsConsolidated': True,
    },
    # consolidated income statement (yearly)
    u'\u500b\u80a1\u640d\u76ca\u5408\u4f75\u5e74\u8868': {
        'DateFrame': 'Yearly',
        'Name': 'IncomeStatement',
        'IsSnapshot': False,
        'IsConsolidated': True,
    },
    # consolidated income statement (quarterly)
    u'\u500b\u80a1\u640d\u76ca\u5408\u4f75\u8ca1\u5831\u5b63\u8868': {
        'DateFrame': 'Quarterly',
        'Name': 'IncomeStatement',
        'IsSnapshot': False,
        'IsConsolidated': True,
    },
    # consolidated cash flow statement (yearly)
    u'\u500b\u80a1\u73fe\u91d1\u6d41\u91cf\u5e74\u8868\u5408\u4f75\u8ca1\u5831': {
        'DateFrame': 'Yearly',
        'Name': 'CashFlow',
        'IsSnapshot': False,
        'IsConsolidated': True,
    },
    # consolidated cash flow statement (quarterly)
    u'\u500b\u80a1\u73fe\u91d1\u6d41\u91cf\u5b63\u8868\u5408\u4f75\u8ca1\u5831': {
        'DateFrame': 'Quarterly',
        'Name': 'CashFlow',
        'IsSnapshot': False,
        'IsConsolidated': True,
    },
    # consolidated operating revenue (monthly)
    u'\u500b\u80a1\u5408\u4f75\u6708\u71df\u6536': {
        'DateFrame': 'Monthly',
        'Name': 'OperatingRevenue',
        'IsSnapshot': False,
        'IsConsolidated': True,
    },
    # capital increase history (yearly)
    u'\u500b\u80a1\u80a1\u672c\u5f62\u6210': {
        'DateFrame': 'Yearly',
        'Name': 'CapitalIncreaseHistory',
        'IsSnapshot': True,
        'IsConsolidated': False,
    },
    # dividend policy (yearly)
    u'\u500b\u80a1\u80a1\u5229\u653f\u7b56': {
        'DateFrame': 'Yearly',
        'Name': 'DividendPolicy',
        'IsSnapshot': True,
        'IsConsolidated': False,
    },
    # consolidated profitability (quarterly)
    u'\u500b\u80a1\u7372\u5229\u80fd\u529b': {
        'DateFrame': 'Quarterly',
        'Name': 'Profitability',
        'IsSnapshot': False,
        'IsConsolidated': True,
    },
    # consolidated financial analysis (yearly)
    u'\u500b\u80a1\u8ca1\u52d9\u6bd4\u7387\u5408\u4f75\u5e74\u8868': {
        'DateFrame': 'Yearly',
        'Name': 'FinancialAnalysis',
        'IsSnapshot': False,
        'IsConsolidated': True,
    },
    # consolidated financial analysis (quarterly)
    u'\u500b\u80a1\u8ca1\u52d9\u6bd4\u7387\u5408\u4f75\u8ca1\u5831\u5b63\u8868': {
        'DateFrame': 'Quarterly',
        'Name': 'FinancialAnalysis',
        'IsSnapshot': False,
        'IsConsolidated': True,
    },
}
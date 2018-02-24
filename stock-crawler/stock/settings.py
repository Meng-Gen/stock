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
DOWNLOAD_DELAY = 3
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
#AUTOTHROTTLE_ENABLED = True
# The initial download delay
#AUTOTHROTTLE_START_DELAY = 5
# The maximum download delay to be set in case of high latencies
#AUTOTHROTTLE_MAX_DELAY = 60
# The average number of requests Scrapy should be sending in parallel to
# each remote server
#AUTOTHROTTLE_TARGET_CONCURRENCY = 1.0
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
    u'個股資產負債合併年表': {
        'DateFrame': 'Yearly',
        'Name': 'BalanceSheet',
        'IsSnapshot': True,
        'IsConsolidated': True,
    },
    u'個股資產負債合併財報季表': {
        'DateFrame': 'Quarterly',
        'Name': 'BalanceSheet',
        'IsSnapshot': True,
        'IsConsolidated': True,
    },
    u'個股損益合併年表': {
        'DateFrame': 'Yearly',
        'Name': 'IncomeStatement',
        'IsSnapshot': False,
        'IsConsolidated': True,
    },
    u'個股損益合併財報季表': {
        'DateFrame': 'Quarterly',
        'Name': 'IncomeStatement',
        'IsSnapshot': False,
        'IsConsolidated': True,
    },
    u'個股現金流量年表合併財報': {
        'DateFrame': 'Yearly',
        'Name': 'CashFlow',
        'IsSnapshot': False,
        'IsConsolidated': True,
    },
    u'個股現金流量季表合併財報': {
        'DateFrame': 'Quarterly',
        'Name': 'CashFlow',
        'IsSnapshot': False,
        'IsConsolidated': True,
    },
    u'個股合併月營收': {
        'DateFrame': 'Monthly',
        'Name': 'OperatingRevenue',
        'IsSnapshot': False,
        'IsConsolidated': True,
    },
    u'個股股本形成': {
        'DateFrame': 'Yearly',
        'Name': 'CapitalIncreaseHistory',
        'IsSnapshot': True,
        'IsConsolidated': False,
    },
    u'個股股利政策': {
        'DateFrame': 'Yearly',
        'Name': 'DividendPolicy',
        'IsSnapshot': True,
        'IsConsolidated': False,
    },
    u'個股獲利能力': {
        'DateFrame': 'Quarterly',
        'Name': 'Profitability',
        'IsSnapshot': False,
        'IsConsolidated': True,
    },
    u'個股財務比率合併年表': {
        'DateFrame': 'Yearly',
        'Name': 'FinancialAnalysis',
        'IsSnapshot': False,
        'IsConsolidated': True,
    },
    u'個股財務比率合併財報季表': {
        'DateFrame': 'Quarterly',
        'Name': 'FinancialAnalysis',
        'IsSnapshot': False,
        'IsConsolidated': True,
    },
    u'個股月成交資訊': {
        'DateFrame': 'Monthly',
        'Name': 'StockPrice',
        'IsSnapshot': False,
        'IsConsolidated': True,
    },
}
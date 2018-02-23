#-*- coding: utf-8 -*-

from singleton import Singleton


class MetricNames():
    __metaclass__ = Singleton

    metric_names = {
        'CapitalIncreaseByCash': u'現金增資',
        'CapitalIncreaseByEarnings': u'盈餘轉增資',
        'CapitalIncreaseBySurplus': u'公積及其他',
        'NetProfit': u'經常利益',
        'Assets': u'資產總額',
        'Liabilities': u'負債總額',
        'Equity': u'股東權益總額',
        'CurrentAssets': u'流動資產',
        'CurrentLiabilities': u'流動負債',
        'Inventories': u'存貨',
        'PrepaidAccounts': u'預付費用及預付款',
        'CostOfGoodsSold': u'營業成本',
        'Sales': u'營業收入淨額',
        'AccountsReceivable': u'應收帳款及票據',
        'AccountsPayable': u'應付帳款及票據',
        'CashFlowFromOperatingActivities': u'來自營運之現金流量',
        'CashFlowFromInvestingActivities': u'投資活動之現金流量',
        'CashFlowFromFinancingActivities': u'理財活動之現金流量',
        'OperatingRevenue': u'合併營收',
        'LongTermLiabilities': u'長期負債',
        'FixedAssets': u'固定資產',
        'IncomeBeforeTax': u'稅前淨利',
        'NetProfitBeforeTax': u'稅前淨利', # same as IncomeBeforeTax
        'InterestExpense': u'利息支出',
        'SellingExpenses': u'營業費用─推銷費用',
        'AdministrativeExpenses': u'營業費用─管理費用',
        'GrossProfit': u'營業毛利',
        'OperatingProfit': u'營業利益',
        'ShortTermDebt': u'短期借款',
        'LongTermInvestments': u'長期投資',
        'CashDividendsFromRetainedEarnings': u'現金股利盈餘發放',
        'CashDividendsFromCapitalReserve': u'現金股利公積發放',
        'CashDividends': u'現金股利小計',
        'StockDividendsFromRetainedEarnings': u'股票股利盈餘發放',
        'StockDividendsFromCapitalReserve': u'股票股利公積發放',
        'StockDividends': u'股票股利小計',
        'EmployeeStockBonusRatio': u'員工配股率(%)',
        'BookValue': u'每股淨值(元)',
    }

    def get(self, good_metric_name):
        return self.metric_names[good_metric_name]
from singleton import Singleton


class MetricNames():
    __metaclass__ = Singleton

    metric_names = {
        'CapitalIncreaseByCash': u'\u73fe\u91d1\u589e\u8cc7',
        'CapitalIncreaseByEarnings': u'\u76c8\u9918\u8f49\u589e\u8cc7',
        'CapitalIncreaseBySurplus': u'\u516c\u7a4d\u53ca\u5176\u4ed6',
        'NetProfit': u'\u7d93\u5e38\u5229\u76ca',
        'Assets': u'\u8cc7\u7522\u7e3d\u984d',
        'Liabilities': u'\u8ca0\u50b5\u7e3d\u984d',
        'Equity': u'\u80a1\u6771\u6b0a\u76ca\u7e3d\u984d',
        'CurrentAssets': u'\u6d41\u52d5\u8cc7\u7522',
        'CurrentLiabilities': u'\u6d41\u52d5\u8ca0\u50b5',
        'Inventories': u'\u5b58\u8ca8',
        'PrepaidAccounts': u'\u9810\u4ed8\u8cbb\u7528\u53ca\u9810\u4ed8\u6b3e',
        'CostOfGoodsSold': u'\u71df\u696d\u6210\u672c',
        'Sales': u'\u71df\u696d\u6536\u5165\u6de8\u984d',
        'AccountsReceivable': u'\u61c9\u6536\u5e33\u6b3e\u53ca\u7968\u64da',
        'AccountsPayable': u'\u61c9\u4ed8\u5e33\u6b3e\u53ca\u7968\u64da',
        'CashFlowFromOperatingActivities': u'\u4f86\u81ea\u71df\u904b\u4e4b\u73fe\u91d1\u6d41\u91cf',
        'CashFlowFromInvestingActivities': u'\u6295\u8cc7\u6d3b\u52d5\u4e4b\u73fe\u91d1\u6d41\u91cf',
        'CashFlowFromFinancingActivities': u'\u7406\u8ca1\u6d3b\u52d5\u4e4b\u73fe\u91d1\u6d41\u91cf',
        'OperatingRevenue': u'\u5408\u4f75\u71df\u6536',
        'LongTermLiabilities': u'\u9577\u671f\u8ca0\u50b5',
        'FixedAssets': u'\u56fa\u5b9a\u8cc7\u7522',
        'IncomeBeforeTax': u'\u7a05\u524d\u6de8\u5229',
        'InterestExpense': u'\u5229\u606f\u652f\u51fa',
        'SellingExpenses': u'\u71df\u696d\u8cbb\u7528\u2500\u63a8\u92b7\u8cbb\u7528',
        'AdministrativeExpenses': u'\u71df\u696d\u8cbb\u7528\u2500\u7ba1\u7406\u8cbb\u7528',
        'GrossProfit': u'\u71df\u696d\u6bdb\u5229',
        'OperatingProfit': u'\u71df\u696d\u5229\u76ca',
        'ShortTermDebt': u'\u77ed\u671f\u501f\u6b3e',
        'LongTermInvestments': u'\u9577\u671f\u6295\u8cc7',
        'CashDividends': u'\u73fe\u91d1\u80a1\u5229',
        'StockDividendsFromRetainedEarnings': u'\u76c8\u9918\u914d\u80a1',
        'StockDividendsFromCapitalReserve': u'\u516c\u7a4d\u914d\u80a1',
        'EmployeeStockBonusRatio': u'\u54e1\u5de5\u914d\u80a1\u7387',
        'BookValue': u'\u6bcf\u80a1\u6de8\u503c(\u5143)',
    }

    def get(self, good_metric_name):
        return self.metric_names[good_metric_name]
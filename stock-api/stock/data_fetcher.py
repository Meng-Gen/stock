from capital_increase_history_service import CapitalIncreaseHistoryService
from capital_structure_service import CapitalStructureService
from cash_flow_service import CashFlowService
from dupont_service import DupontService
from dividend_policy_service import DividendPolicyService
from expected_rate_of_return_service import ExpectedRateOfReturnService
from liquidity_service import LiquidityService
from operating_revenue_service import OperatingRevenueService
from profitability_service import ProfitabilityService
from revenue_index_service import RevenueIndexService
from stock_code_service import StockCodeService

import json


class DataFetcher():
    def get_all_stocks(self):
        data = {
            'stocks': StockCodeService().get()
        }
        return json.dumps(data)

    def analyze(self, stock):
        data = {
            'stock': stock,
            'analysis': {
                'CapitalStructure': CapitalStructureService().get(stock),
                'CapitalIncreaseHistory': CapitalIncreaseHistoryService().get(stock),
                'CashFlow': CashFlowService().get(stock),
                'DuPont': DupontService().get(stock),
                'DividendPolicy': DividendPolicyService().get(stock),
                'ExpectedRateOfReturn': ExpectedRateOfReturnService().get(stock),
                'Liquidity': LiquidityService().get(stock),
                'OperatingRevenue': OperatingRevenueService().get(stock),
                'Profitability': ProfitabilityService().get(stock),
                'RevenueIndex': RevenueIndexService().get(stock),
            }
        }
        return json.dumps(data, default=str)
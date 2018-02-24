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
    services = {
        'capital_structure': CapitalStructureService(),
        'capital_increase_history': CapitalIncreaseHistoryService(),
        'cash_flow': CashFlowService(),
        'dupont': DupontService(),
        'dividend_policy': DividendPolicyService(),
        'expected_rate_of_return': ExpectedRateOfReturnService(),
        'liquidity': LiquidityService(),
        'operating_revenue': OperatingRevenueService(),
        'profitability': ProfitabilityService(),
        'revenue_index': RevenueIndexService(),
    }

    def get_all_stocks(self):
        data = {
            'stocks': StockCodeService().get()
        }
        return json.dumps(data)

    def analyze(self, analysis, stock):
        data = {
            'stock': stock,
            'name': analysis,
            'analysis': self._get_analysis_data(analysis, stock),
        }
        return json.dumps(data, default=str)

    def _get_analysis_data(self, analysis, stock):
        if analysis in self.services:
            return self.services[analysis].get(stock)
        else:
            return None
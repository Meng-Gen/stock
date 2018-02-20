from capital_increase_history_service import CapitalIncreaseHistoryService
from dupont_service import DupontService
from stock_code_service import StockCodeService

import json


class DataFetcher():
    def get_all_stocks(self):
        data = {
            "stocks": StockCodeService().get()
        }
        return json.dumps(data)

    def analyze(self, stock):
        data = {
            "stock": stock,
            "analysis": [
                self._analyze_dupont(stock),
                CapitalIncreaseHistoryService().get(stock),
            ]
        }
        return json.dumps(data, default=str)

    def _analyze_dupont(self, stock):
        service = DupontService()
        return {
            "name": "DuPontAnalysis",
            "data": [
                {
                    "name": "ROE",
                    "data": service.roe(stock),
                },
                {
                    "name": "EquityMultiplier",
                    "data": service.equity_multiplier(stock),
                }
            ]
        }
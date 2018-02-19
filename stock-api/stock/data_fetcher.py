from stock_code_service import StockCodeService
from dupont_service import DupontService

import json


class DataFetcher():
    def get_all_stocks(self):
        service = StockCodeService()
        data = {
            "stocks": service.get()
        }
        return json.dumps(data)

    def analyze(self, stock):
        data = {
            "stock": stock,
            "analysis": [
                self._analyze_dupont(stock)
            ]
        }
        return json.dumps(data)

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
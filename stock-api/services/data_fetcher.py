from services.stock_code_service import StockCodeService
from services.dupont_service import DupontService

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
                    "data": service.get_roe(stock),
                },
                {
                    "name": "EquityMultiplier",
                    "data": service.get_equity_multiplier(stock),
                }
            ]
        }
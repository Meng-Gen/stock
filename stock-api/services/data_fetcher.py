from services.stock_code_service import StockCodeService
from services.financial_statement_entry_service import FinancialStatementEntryService

import json


class DataFetcher():
    stock_code_service = StockCodeService()
    entry_service = FinancialStatementEntryService()

    def get_all_stocks(self):
        data = {
            "stocks": self.stock_code_service.get()
        }
        return json.dumps(data)

    def analysis(self, stock):
        data = {
            "stock": stock,
            "analysis": [
                {
                    "name": "DuPontAnalysis",
                    "data": [
                        {
                            "name": "ROE",
                            "data": self.entry_service.get_roe(stock),
                        },
                        {
                            "name": "EquityMultiplier",
                            "data": self.entry_service.get_equity_multiplier(stock),
                        }
                    ]
                }
            ]
        }
        return json.dumps(data)
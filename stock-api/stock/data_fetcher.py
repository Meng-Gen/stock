from capital_increase_history_service import CapitalIncreaseHistoryService
from dupont_service import DupontService
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
                'DuPont': DupontService().get(stock),
                'CapitalIncreaseHistory': CapitalIncreaseHistoryService().get(stock),
            }
        }
        return json.dumps(data, default=str)
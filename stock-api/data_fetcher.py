from services import DupontService
from services import StockCodeService

import json


class DataFetcher():
    stock_code_service = StockCodeService()

    def get_all_stocks(self):
    	data = {
    	    "stocks": self.stock_code_service.get()
    	}
        return json.dumps(data)

    def analysis(self, stock):    
        return '{stock}'.format(stock=stock)
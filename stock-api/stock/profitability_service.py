from base_service import BaseService


class ProfitabilityService(BaseService):
    def get(self, stock_code):
        return [
            {
                'date_frame': u'Yearly',
                'data': self.filter_list(self.build_data_safely(stock_code, u'Yearly')),
            },
            {
                'date_frame': u'Quarterly',
                'data': self.filter_list(self.build_data_safely(stock_code, u'Quarterly')),
            },
        ]

    def build_data(self, stock_code, date_frame):
        sales = self.get_metric(stock_code, date_frame, 'Sales')
        gross_profit = self.get_metric(stock_code, date_frame, 'GrossProfit')
        operating_profit = self.get_metric(stock_code, date_frame, 'OperatingProfit')
        net_profit = self.get_metric(stock_code, date_frame, 'NetProfit')
        net_profit_before_tax = self.get_metric(stock_code, date_frame, 'NetProfitBeforeTax')
        cost_of_goods_sold = self.get_metric(stock_code, date_frame, 'CostOfGoodsSold')
        inventories = self.get_metric(stock_code, date_frame, 'Inventories')
        accounts_receivable = self.get_metric(stock_code, date_frame, 'AccountsReceivable')
        accounts_payable = self.get_metric(stock_code, date_frame, 'AccountsPayable')

        # GrossProfitMargin = GrossProfit / Sales
        gross_profit_margin = self.get_ratio(gross_profit, sales)

        # OperatingProfitMargin = OperatingProfit / Sales
        operating_profit_margin = self.get_ratio(operating_profit, sales)
    
        # NetProfitBeforeTaxMargin = NetProfitBeforeTax / Sales
        net_profit_before_tax_margin = self.get_ratio(net_profit_before_tax, sales)

        # NetProfitMargin = NetProfit / Sales
        net_profit_margin = self.get_ratio(net_profit, sales)

        # Inventory Turnover Ratio = Cost of goods sold / Inventory
        inventory_turnover_ratio = self.get_ratio(cost_of_goods_sold, inventories, 4.0)
        # DIO = 365 / Inventory Turnover Ratio 
        dio = inventory_turnover_ratio.inverse().scalar(365.0)

        # Receivables Turnover Ratio = Sales / Accounts receivable
        receivables_turnover_ratio = self.get_ratio(sales, accounts_receivable, 4.0)
        # DSO = 365 / Receivables Turnover Ratio
        dso = receivables_turnover_ratio.inverse().scalar(365.0)

        # AccountsPayableTurnoverRatio = Cost of goods sold / Accounts payable
        accounts_payable_turnover_ratio = self.get_ratio(cost_of_goods_sold, accounts_payable)

        # DPO = 365 / AccountsPayableTurnoverRatio
        dpo = accounts_payable_turnover_ratio.inverse().scalar(365.0)

        # CCC = DIO + DSO - DPO
        ccc = dio + dso - dpo

        return [
            self.build_metric_data(gross_profit_margin, 'GrossProfitMargin'),
            self.build_metric_data(operating_profit_margin, 'OperatingProfitMargin'),
            self.build_metric_data(net_profit_before_tax_margin, 'NetProfitBeforeTaxMargin'),
            self.build_metric_data(net_profit_margin, 'NetProfitMargin'),
            self.build_metric_data(dio, 'DaysInventoryOutstanding'),
            self.build_metric_data(dso, 'DaysSalesOutstanding'),
            self.build_metric_data(dpo, 'DaysPayableOutstanding'),
            self.build_metric_data(ccc, 'CashConversionCycle'),
        ]
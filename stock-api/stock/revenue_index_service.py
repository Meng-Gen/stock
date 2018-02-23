from base_service import BaseService


class RevenueIndexService(BaseService):
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
        inventories = self.get_metric(stock_code, date_frame, 'Inventories')
        sales = self.get_metric(stock_code, date_frame, 'Sales')
        accounts_receivable = self.get_metric(stock_code, date_frame, 'AccountsReceivable')
        gross_profit = self.get_metric(stock_code, date_frame, 'GrossProfit')
        selling_expenses = self.get_metric(stock_code, date_frame, 'SellingExpenses')
        administrative_expenses = self.get_metric(stock_code, date_frame, 'AdministrativeExpenses')
        accounts_payable = self.get_metric(stock_code, date_frame, 'AccountsPayable')

        inventory_growth_rate = self.get_growth_rate(inventories)
        sales_growth_rate = self.get_growth_rate(sales)
        accounts_receivable_growth_rate = self.get_growth_rate(accounts_receivable)
        gross_profit_growth_rate = self.get_growth_rate(gross_profit)
        selling_and_administrative_expenses_growth_rate = \
            self.get_growth_rate(selling_expenses + administrative_expenses)
        accounts_payable_growth_rate = self.get_growth_rate(accounts_payable)

        # InventoryIndex = InventoryGrowthRate - SalesGrowthRate
        inventory_index = inventory_growth_rate - sales_growth_rate

        # AccountsReceivableIndex = AccountsReceivableGrowthRate - SalesGrowthRate
        accounts_receivable_index = accounts_receivable_growth_rate - sales_growth_rate

        # GrossProfitIndex = SalesGrowthRate - GrossProfitGrowthRate
        gross_profit_index = sales_growth_rate - gross_profit_growth_rate

        # SellingAndAdministrativeExpensesIndex = SellingAndAdministrativeExpensesGrowthRate - SalesGrowthRate
        selling_and_administrative_expenses_index = \
            selling_and_administrative_expenses_growth_rate - sales_growth_rate

        # AccountsPayableIndex = SalesGrowthRate - AccountsPayableGrowthRate
        accounts_payable_index = sales_growth_rate - accounts_payable_growth_rate

        return [
            self.build_metric_data(inventory_index, 'InventoryIndex'),
            self.build_metric_data(accounts_receivable_index, 'AccountsReceivableIndex'),
            self.build_metric_data(gross_profit_index, 'GrossProfitIndex'),
            self.build_metric_data(selling_and_administrative_expenses_index, 'SellingAndAdministrativeExpensesIndex'),
            self.build_metric_data(accounts_payable_index, 'AccountsPayableIndex'),
        ]

    def get_growth_rate(self, metric):
        prev_metric = metric.moving_average(2).shift()
        return self.get_ratio(metric - prev_metric, prev_metric)
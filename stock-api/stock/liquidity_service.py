from base_service import BaseService


class LiquidityService(BaseService):
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
        current_assets = self.get_metric(stock_code, date_frame, 'CurrentAssets')
        current_liabilities = self.get_metric(stock_code, date_frame, 'CurrentLiabilities')
        inventories = self.get_metric(stock_code, date_frame, 'Inventories')
        prepaid_accounts = self.get_metric(stock_code, date_frame, 'PrepaidAccounts')
        income_before_tax = self.get_metric(stock_code, date_frame, 'IncomeBeforeTax')
        interest_expense = self.get_metric(stock_code, date_frame, 'InterestExpense')

        # CurrentRatio = CurrentAssets / CurrentLiabilities
        current_ratio = self.get_ratio(current_assets, current_liabilities)

        # QuickAssets = CurrentAssets - Inventories - PrepaidAccounts
        quick_assets = current_assets - inventories - prepaid_accounts
        # QuickRatio = QuickAssets / CurrentLiabilities
        quick_ratio = self.get_ratio(quick_assets, current_liabilities)

        # EBDIT = IncomeBeforeTax + InterestExpense
        ebdit = income_before_tax + interest_expense
        # InterestProtectionMultiples = EBDIT / InterestExpense
        interest_protection_multiples = self.get_ratio(ebdit, interest_expense)

        return [
            self.build_metric_data(current_ratio, 'CurrentRatio'),
            self.build_metric_data(quick_ratio, 'QuickRatio'),
            self.build_metric_data(interest_protection_multiples, 'InterestProtectionMultiples'),
        ]
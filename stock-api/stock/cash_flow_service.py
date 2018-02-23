from base_service import BaseService


class CashFlowService(BaseService):
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
        net_profit = self.get_metric(stock_code, date_frame, 'NetProfit')
        cash_flow_from_operating_activities = self.get_metric(stock_code, date_frame, 'CashFlowFromOperatingActivities')
        cash_flow_from_investing_activities = self.get_metric(stock_code, date_frame, 'CashFlowFromInvestingActivities')
        cash_flow_from_financing_activities = self.get_metric(stock_code, date_frame, 'CashFlowFromFinancingActivities')
        long_term_investments = self.get_metric(stock_code, date_frame, 'LongTermInvestments')
        assets = self.get_metric(stock_code, date_frame, 'Assets')

        # FreeCashFlow = CashFlowFromOperatingActivities + CashFlowFromInvestingActivities
        free_cash_flow = cash_flow_from_operating_activities + cash_flow_from_investing_activities

        # AccumulatedFreeCashFlow
        accumulated_free_cash_flow = free_cash_flow.accumulate()

        # LongTermInvestmentsToAssetsRatio = LongTermInvestments / Assets
        long_term_investments_to_assets_ratio = self.get_ratio(long_term_investments, assets)

        return [
            self.build_metric_data(cash_flow_from_operating_activities),
            self.build_metric_data(cash_flow_from_investing_activities),
            self.build_metric_data(cash_flow_from_financing_activities),
            self.build_metric_data(free_cash_flow, 'FreeCashFlow'),
            self.build_metric_data(accumulated_free_cash_flow, 'AccumulatedFreeCashFlow'),
            self.build_metric_data(long_term_investments_to_assets_ratio, 'LongTermInvestmentsToAssetsRatio'),
        ]
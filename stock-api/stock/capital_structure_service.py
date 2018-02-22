from base_service import BaseService


class CapitalStructureService(BaseService):
    def get(self, stock_code):
        return [
            {
                'date_frame': u'Yearly',
                'data': self.filter_list(self.build_data(stock_code, u'Yearly')),
            },
            {
                'date_frame': u'Quarterly',
                'data': self.filter_list(self.build_data(stock_code, u'Quarterly')),
            },
        ]

    def build_data(self, stock_code, date_frame):
        assets = self.get_metric(stock_code, date_frame, 'Assets')
        liabilities = self.get_metric(stock_code, date_frame, 'Liabilities')
        equity = self.get_metric(stock_code, date_frame, 'Equity')
        long_term_liabilities = self.get_metric(stock_code, date_frame, 'LongTermLiabilities')
        current_liabilities = self.get_metric(stock_code, date_frame, 'CurrentLiabilities')
        fixed_assets = self.get_metric(stock_code, date_frame, 'FixedAssets')

        # EquityRatio = Equity / Assets
        equity_ratio = self.get_ratio(equity, assets)

        # LiabilitiesRatio = Liabilities / Assets
        liabilities_ratio = self.get_ratio(liabilities, assets)

        # EquityMultiplier = Assets / Equity
        equity_multiplier = self.get_ratio(assets, equity)

        # TrueLiabilitiesRatio = LongTermLiabilities / (Assets - CurrentLiabilities)
        true_liabilities_ratio = self.get_ratio(long_term_liabilities, assets - current_liabilities)

        # LongTermCapitalToFixedAssetsRatio = (LongTermLiabilities + Equity) / FixedAssets
        long_term_capital_to_fixed_assets_ratio = self.get_ratio(long_term_liabilities + equity, fixed_assets)

        return [
            self.build_metric_data(equity_ratio, 'EquityRatio'),
            self.build_metric_data(liabilities_ratio, 'LiabilitiesRatio'),
            self.build_metric_data(equity_multiplier, 'EquityMultiplier'),
            self.build_metric_data(true_liabilities_ratio, 'TrueLiabilitiesRatio'),
            self.build_metric_data(long_term_capital_to_fixed_assets_ratio, 'LongTermCapitalToFixedAssetsRatio'),
        ]
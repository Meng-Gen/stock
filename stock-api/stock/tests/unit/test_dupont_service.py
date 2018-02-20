from dupont_service import DupontService
from mock_financial_statement_entry_store import MockFinancialStatementEntryStore

import unittest


class MockMetricNames(object):
    def get(self, good_metric_name):
        return good_metric_name


class DupontServiceTest(unittest.TestCase):
    def test_roe(self):
        service = DupontService()
        service.store = MockFinancialStatementEntryStore()
        service.metric_names = MockMetricNames()
        service.roe('2330')

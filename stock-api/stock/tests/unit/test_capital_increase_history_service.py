from capital_increase_history_service import CapitalIncreaseHistoryService
from mocks import MockFinancialStatementEntryStore

import unittest


class CapitalIncreaseHistoryServiceTest(unittest.TestCase):
    def test_get(self):
        service = CapitalIncreaseHistoryService()
        service.store = MockFinancialStatementEntryStore()
        service.get('2317')

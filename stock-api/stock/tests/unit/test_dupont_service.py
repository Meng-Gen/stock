from dupont_service import DupontService
from mocks import MockFinancialStatementEntryStore

import unittest


class DupontServiceTest(unittest.TestCase):
    def test_roe(self):
        service = DupontService()
        service.store = MockFinancialStatementEntryStore()
        service.roe('2330')

from dupont_service import DupontService
from mocks import MockFinancialStatementEntryStore

import unittest


class DupontServiceTest(unittest.TestCase):
    def test_get(self):
        service = DupontService()
        service.store = MockFinancialStatementEntryStore()
        expected = {
            'DuPont': [
                {
                    'date_frame': u'Yearly',
                    'data': [],
                },
            ]
        }
        self.assertEqual(service.get('2317'), expected)
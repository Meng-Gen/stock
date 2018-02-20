from capital_increase_history_service import CapitalIncreaseHistoryService
from mocks import MockFinancialStatementEntryStore

from datetime import datetime

import unittest


class CapitalIncreaseHistoryServiceTest(unittest.TestCase):
    def test_get(self):
        service = CapitalIncreaseHistoryService()
        service.store = MockFinancialStatementEntryStore()
        expected = [
            {
                'name': 'CapitalIncreaseHistoryService (Yearly)',
                'data': [
                    {
                        'name': 'CapitalIncreaseByCash',
                        'data': {
                            'date': [
                                datetime(2005, 12, 31),
                                datetime(2006, 12, 31),
                                datetime(2007, 12, 31)
                            ],
                            'value': [26.44, 27.01, 27.01],
                        }
                    },
                    {
                        'name': 'CapitalIncreaseByEarnings',
                        'data': {
                            'date': [
                                datetime(2005, 12, 31),
                                datetime(2006, 12, 31),
                                datetime(2007, 12, 31)
                            ],
                            'value': [346.52, 435.51, 547.78],
                        }
                    },
                    {
                        'name': 'CapitalIncreaseBySurplus',
                        'data': {
                            'date': [
                                datetime(2005, 12, 31),
                                datetime(2006, 12, 31),
                                datetime(2007, 12, 31)
                            ],
                            'value': [36.01, 53.83, 53.83],
                        }
                    }
                ]
            }
        ]
        self.assertEqual( service.get('2317'), expected)
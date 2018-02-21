from dupont_service import DupontService
from mocks import MockFinancialStatementEntryStore

from datetime import datetime

import unittest


class DupontServiceTest(unittest.TestCase):
    def test_get(self):
        service = DupontService()
        service.store = MockFinancialStatementEntryStore()
        actual = service.get('2317')
        expected = {
            'DuPont': [
                {
                    'date_frame': u'Yearly',
                    'data': [
                        {
                            'name': 'ReturnOnEquity',
                            'date': [
                                datetime(2014, 12, 31),
                                datetime(2015, 12, 31),
                                datetime(2016, 12, 31),
                                datetime(2017, 12, 31)
                            ],
                            'value': [
                                0.13454361176304513,
                                0.14689095912703148,
                                0.13796224557693534,
                                0.07423633002006001
                            ]
                        },
                        {
                            'name': 'ReturnOnAssets',
                            'date': [
                                datetime(2014, 12, 31),
                                datetime(2015, 12, 31),
                                datetime(2016, 12, 31),
                                datetime(2017, 12, 31)
                            ],
                            'value': [
                                0.057290479709711864,
                                0.062909094868964,
                                0.06344855340006267,
                                0.03524979321325024
                            ]
                        },
                        {
                            'name': 'ReturnOnSales',
                            'date': [
                                datetime(2014, 12, 31),
                                datetime(2015, 12, 31),
                                datetime(2016, 12, 31),
                                datetime(2017, 12, 31)
                            ],
                            'value': [
                                0.03144471671225386,
                                0.03351095658195873,
                                0.034724999214221196,
                                0.0214326416131447
                            ]
                        },
                        {
                            'name': 'AssetTurnover',
                            'date': [
                                datetime(2014, 12, 31),
                                datetime(2015, 12, 31),
                                datetime(2016, 12, 31),
                                datetime(2017, 12, 31)
                            ],
                            'value': [
                                1.821942943037742,
                                1.8772694451471528,
                                1.8271722054950572,
                                1.6446779566188166
                            ]
                        },
                        {
                            'name': 'EquityMultiplier',
                            'date': [
                                datetime(2014, 12, 31),
                                datetime(2015, 12, 31),
                                datetime(2016, 12, 31),
                                datetime(2017, 12, 31)

                            ],
                            'value': [
                                2.3484462417625274,
                                2.334971746660747,
                                2.1743954461347745,
                                2.1060075323265983
                            ]
                        }
                    ]
                },
                {
                    'date_frame': u'Quarterly',
                    'data': [
                        {
                            'name': 'ReturnOnEquity',
                            'date': [
                                datetime(2017, 3, 31),
                                datetime(2017, 6, 30),
                                datetime(2017, 9, 30)
                            ],
                            'value': [
                                0.09871356690508279,
                                0.05152555836407475,
                                0.06871375297117534
                            ]
                        },
                        {
                            'name': 'ReturnOnAssets',
                            'date': [
                                datetime(2017, 3, 31),
                                datetime(2017, 6, 30),
                                datetime(2017, 9, 30)
                            ],
                            'value': [
                                0.05009042413162392,
                                0.02491732638540936,
                                0.030136585857374564
                            ]
                        },
                        {
                            'name': 'ReturnOnSales',
                            'date': [
                                datetime(2017, 3, 31),
                                datetime(2017, 6, 30),
                                datetime(2017, 9, 30)
                            ],
                            'name': 'ReturnOnSales',
                            'value': [
                                0.1198181825640689,
                                0.06469560239892803,
                                0.07290813167583039
                            ]
                        },
                        {
                            'name': 'AssetTurnover',
                            'date': [
                                datetime(2017, 3, 31),
                                datetime(2017, 6, 30),
                                datetime(2017, 9, 30)
                            ],
                            'value': [
                                1.6722144522544293,
                                1.540588569328924,
                                1.6534005282905955
                            ]
                        },
                        {
                            'name': 'EquityMultiplier',
                            'date': [
                                datetime(2017, 3, 31),
                                datetime(2017, 6, 30),
                                datetime(2017, 9, 30)
                            ],
                            'value': [
                                1.9707073480889392,
                                2.067860635089893,
                                2.2800775541188507
                            ]
                        }
                    ]
                }
            ]
        }
        self.assertEqual(actual, expected)
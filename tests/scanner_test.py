
__author__ = 'kchu'

import unittest
from mock import *
from src import scanner
import zbar


class ScannerTestCase(unittest.TestCase):
    def setUp(self):
        self.image_path = 'some/test/path'

    def test_scan_returns_an_array(self):
        self.scanner = scanner.Scanner(self.image_path)
        self.assertTrue(isinstance(self.scanner.scan(), list))

    def test_scan_one_code(self):
        location_list = [[100, 100], [100, 200], [200, 200], [200, 100]]
        qr_codes = [{'data': 'test', 'location': location_list}]

        symbols = [Mock()]
        symbols[0].data = 'test'
        symbols[0].location = location_list

        mock_image = Mock()
        mock_image.__iter__ = Mock(return_value=iter(symbols))
        with patch('zbar.Image', return_value=mock_image) as MockImage:
            self.scanner = scanner.Scanner(self.image_path)
            self.assertItemsEqual(self.scanner.scan(), qr_codes)

    def test_scan_multiple_codes(self):
        location_lists = [
            [[100, 100], [100, 200], [200, 200], [200, 100]],
            [[100, 100], [100, 200], [200, 200], [200, 100]],
        ]
        qr_codes = [
            {'data': 'first', 'location': location_lists[0]},
            {'data': 'second', 'location': location_lists[1]},
        ]

        symbols = [Mock(), Mock()]
        symbols[0].data = qr_codes[0]['data']
        symbols[0].location = location_lists[0]
        symbols[1].data = qr_codes[1]['data']
        symbols[1].location = location_lists[1]

        mock_image = Mock()
        mock_image.__iter__ = Mock(return_value=iter(symbols))
        with patch('zbar.Image', return_value=mock_image) as MockImage:
            self.scanner = scanner.Scanner(self.image_path)
            self.assertItemsEqual(self.scanner.scan(), qr_codes)


if __name__ == '__main__':
    unittest.main()

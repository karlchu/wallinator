
__author__ = 'kchu'

import unittest
from mock import *
from src import scanner
import zbar
from PIL import Image

IMAGE_PATH = 'some/test/path'

class ScannerTestCase(unittest.TestCase):

    def setUp(self):
        self.image_open_patcher = patch.object(Image, 'open')
        open_method = self.image_open_patcher.start()
        open_method(IMAGE_PATH).convert('L').tostring.return_value = 'test data'
        open_method(IMAGE_PATH).convert('L').size = [10, 20]
        self.addCleanup(self.image_open_patcher.stop)

        self.zbar_image_patcher = patch('zbar.Image')
        self.zbar_image_patcher.start()
        self.addCleanup(self.zbar_image_patcher.stop)

    def test_scan_returns_an_array(self):
        self.scanner = scanner.Scanner(IMAGE_PATH)
        self.assertTrue(isinstance(self.scanner.scan(), list))

    def test_scan_one_code(self):
        location_list = [[100, 100], [100, 200], [200, 200], [200, 100]]
        qr_codes = [{'data': 'test', 'location': location_list}]

        symbols = [Mock()]
        symbols[0].data = 'test'
        symbols[0].location = location_list

        mock_zbar_image = Mock()
        mock_zbar_image.__iter__ = Mock(return_value=iter(symbols))
        with patch('zbar.Image', return_value=mock_zbar_image):
            self.scanner = scanner.Scanner(IMAGE_PATH)
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
        with patch('zbar.Image', return_value=mock_image):
            self.scanner = scanner.Scanner(IMAGE_PATH)
            self.assertItemsEqual(self.scanner.scan(), qr_codes)

    def test_scan_should_configure_zbar_scanner_to_scan_qr_codes(self):
        mock_zbar_scanner = Mock()
        with patch('zbar.ImageScanner', return_value=mock_zbar_scanner):
            self.scanner = scanner.Scanner(IMAGE_PATH)
            self.scanner.scan()
            calls = [
                call(0, zbar.Config.ENABLE, 0),
                call(zbar.Symbol.QRCODE, zbar.Config.ENABLE, 1),
            ]
            mock_zbar_scanner.set_config.assert_has_calls(calls)

    def test_scan_should_scan_image_on_given_path(self):
        with patch('zbar.Image') as ZbarImage:
            self.scanner = scanner.Scanner(IMAGE_PATH)
            self.scanner.scan()
            ZbarImage.assert_called_once_with(10, 20, 'Y800', 'test data')

if __name__ == '__main__':
    unittest.main()


__author__ = 'kchu'

import unittest
import mock
from mock import MagicMock
from src import scanner
from PIL import Image


class ScannerTestCase(unittest.TestCase):
    def setUp(self):
        self.image_path = 'some/test/path'
        self.scanner = scanner.Scanner(self.image_path)

    def test_scan_returns_an_array(self):
        self.assertTrue(isinstance(self.scanner.scan(), list))

    # def test_scan_

if __name__ == '__main__':
    unittest.main()

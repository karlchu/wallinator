from PIL import Image
import zbar

__author__ = 'kchu'


class Scanner(object):
    def __init__(self, image_path):
        self.image_path = image_path

    def scan(self):
        # self.image = self.__open_image(self.image_path)
        # self.scanner = self.__create_image_scanner()
        zbar_img = zbar.Image(100, 100, 'Y800', 'test data')

        result = []
        for symbol in zbar_img:
            result.append({
                'data': symbol.data,
                'location': symbol.location,
                })
        return result

    # def __open_image(self, image_path):
    #     return Image.open(image_path).convert('L')
    #
    # def __create_image_scanner(self):
    #     scanner = zbar.ImageScanner()
    #     scanner.set_config(0, zbar.Config.ENABLE, 0)
    #     scanner.set_config(zbar.Symbol.QRCODE, zbar.Config.ENABLE, 1)
    #     return scanner

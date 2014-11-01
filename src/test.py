import Image
import zbar

image_path = '../data/IMG_5240.JPG'

scanner = zbar.ImageScanner()
scanner.set_config(0, zbar.Config.ENABLE, 0)
scanner.set_config(zbar.Symbol.QRCODE, zbar.Config.ENABLE, 1)

image = Image.open(image_path).convert('L')
# scale = 1.7
# doubled_size = (int(image.size[0] * scale), int(image.size[1] * scale))
# image = image.resize(doubled_size, Image.ANTIALIAS)

zbar_img = zbar.Image(image.size[0], image.size[1], 'Y800', image.tostring())

print scanner.scan(zbar_img)

for symbol in zbar_img:
    print "{0}:{1} - {2}".format(symbol.type, symbol.data, symbol.location)

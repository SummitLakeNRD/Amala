from PIL import Image, ExifTags

class exif:
    def __init__(self, imageDir):
        self.exifList = []

    def dataGrab(self, frame):
        img = Image.open(frame)
        return img._getexif()
         
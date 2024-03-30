from exiftool import ExifToolHelper
import math
import utm 

class exif:
    def __init__(self):
        self.exifDict = {}

    def dataGrab(self, frame):
        with ExifToolHelper() as et:
            metadata = et.get_metadata(frame)[0]

        self.exifDict = {'imageFile': metadata['SourceFile'],
                         'dateTime': metadata['EXIF:DateTimeOriginal'],
                         'northing': metadata['Composite:GPSLatitude'],
                         'easting': metadata['Composite:GPSLongitude'],
                         'imageWidth': int(metadata['EXIF:ExifImageWidth']),
                         'imageHeight': int(metadata['EXIF:ExifImageHeight']),
                         'flightHeight_m': float(metadata['XMP:RelativeAltitude'])}
        
        return self.exifDict

class spatialProcess:
    def __init__(self):
        self.hfov = 84

    def frameDims(self, exifData):
        frameWidth_m = 2 * math.tan(0.5 * self.hfov * math.pi / 180) * exifData['flightHeight_m']
        pixelSize_cmP = round(frameWidth_m / exifData['imageWidth'], 4)
        return pixelSize_cmP

    def utmConvert(self, exifData):
        exifData.update()
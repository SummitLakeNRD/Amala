from exiftool import ExifToolHelper
import math
from utm import from_latlon

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
        self.utmCoords = []
        self.center = []

    def frameDims(self, exifData):
        self.frameWidth_m = round(2 * math.tan(0.5 * self.hfov * math.pi / 180) 
                             * exifData['flightHeight_m'], 2)
        pixelSize_cmP = round(self.frameWidth_m / exifData['imageWidth'], 5)
        self.frameHeight_m = round(pixelSize_cmP * exifData['imageHeight'], 2)
        return self.frameWidth_m, self.frameHeight_m

    def utmConvert(self, exifData):
        utmCoords = from_latlon(exifData['northing'], exifData['easting'])
        exifData.update({'northing': utmCoords[1]})
        exifData.update({'easting': utmCoords[0]})
        return exifData  
    
    def pointUtmConvert(self, exifData, boxes):
        yoloCoords = [[(i[2] + i[0]) / 2 / exifData['imageWidth'], 
                       (i[3] + i[1]) / 2 / exifData['imageHeight'],
                       (i[2] - i[0]) / exifData['imageWidth'],
                       (i[3] - i[1]) / exifData['imageHeight']] for i in boxes]
        zeroCoord = [exifData['easting'] - (self.frameWidth_m / 2), # easting increases moving right in space and (0,0) is top left in image data
                     exifData['northing'] + (self.frameHeight_m / 2)] # northing increases up in space and (0,0) is top left in image data
        birdLocation = [[zeroCoord[0] + (j[0] * self.frameWidth_m), 
                 zeroCoord[1] - (j[1] * self.frameHeight_m)] for j in yoloCoords]
        return birdLocation
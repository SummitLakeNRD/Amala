from exiftool import ExifToolHelper
import math
from utm import from_latlon

class exif:
    def __init__(self):
        self.exifDict = {}

    def dataGrab(self, frame):
        # Extract exif data from the images using exiftool package
        # Note: I was only able to see all of the data using this tool,
        # using other exif viewer options I couldn't see some relevant data
        with ExifToolHelper() as et:
            metadata = et.get_metadata(frame)[0]
        self.exifDict = {'imageFile': metadata['SourceFile'],
                         'dateTime': metadata['EXIF:DateTimeOriginal'],
                         'imageNorthing': metadata['Composite:GPSLatitude'],
                         'imageEasting': metadata['Composite:GPSLongitude'],
                         'imageBearing': float(metadata['XMP:FlightYawDegree']),
                         'imageWidth': int(metadata['EXIF:ExifImageWidth']),
                         'imageHeight': int(metadata['EXIF:ExifImageHeight']),
                         'flightHeight_m': float(metadata['XMP:RelativeAltitude'])}
        return self.exifDict
    
def rotateCoord(imageEasting, imageNorthing, birdEasting, birdNorthing, bearing):
    # Function to rotation the location of the bird to its true cartesianal point
    # based on the orientation of the drone
    return [-(round(math.cos(math.radians(bearing)), 2)) * (birdEasting - imageEasting) + 
            (round(math.sin(math.radians(bearing)), 2)) * (birdNorthing - imageNorthing) + imageEasting,
            -(round(math.sin(math.radians(bearing)), 2)) * (birdEasting - imageEasting) - 
            (round(math.cos(math.radians(bearing)), 2)) * (birdNorthing - imageNorthing) + imageNorthing]

class spatialProcess:
    def __init__(self):
        self.hfov = 84
        self.degrees = self.hfov * 0.5 * math.pi / 180

    def frameDims(self, exifData):
        # Extract dimensions of image 
        self.frameWidth_m = round(2 * math.tan(self.degrees) 
                             * exifData['flightHeight_m'], 2)
        pixelSize_cmP = round(self.frameWidth_m / exifData['imageWidth'], 5)
        self.frameHeight_m = round(pixelSize_cmP * exifData['imageHeight'], 2)

    def utmConvert(self, exifData):
        # Extract image location and convert to UTM zone 11 (NAD83)
        utmCoords = from_latlon(exifData['imageNorthing'], exifData['imageEasting'])
        exifData.update({'imageNorthing': utmCoords[1]})
        exifData.update({'imageEasting': utmCoords[0]})
        exifData.update({'utmZone': utmCoords[2]})
        return exifData
    
    def pointUtmConvert(self, exifData, boxes):
        # Convert relative position of waterbird to georeferenced points in UTM points
        yoloCoords = [[(i[2] + i[0]) / 2 / exifData['imageWidth'], 
                       (i[3] + i[1]) / 2 / exifData['imageHeight'],
                       (i[2] - i[0]) / exifData['imageWidth'],
                       (i[3] - i[1]) / exifData['imageHeight']] for i in boxes]
                     # easting increases moving right in space and (0,0) is top left in image data
        zeroCoord = [exifData['imageEasting'] - (self.frameWidth_m / 2), 
                     # northing increases up in space and (0,0) is top left in image data
                     exifData['imageNorthing'] + (self.frameHeight_m / 2)] 
        birdCoordsUTM = [[zeroCoord[0] + (j[0] * self.frameWidth_m), 
                   zeroCoord[1] - (j[1] * self.frameHeight_m)] for j in yoloCoords]
        # Applying rotation function to incorporate the compass bearing the drone is facing
        birdCoordsUTM = [rotateCoord(exifData['imageEasting'], exifData['imageNorthing'], 
                                     k[0], k[1], exifData['imageBearing']) for k in birdCoordsUTM]
        return birdCoordsUTM, yoloCoords


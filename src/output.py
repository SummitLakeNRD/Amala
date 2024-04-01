import json
import cv2
import csv
from datetime import datetime

class textOut:
    def __init__(self):
        self.json = {}
        self.dateFormat = "%Y:%m:%d %H:%M:%S"

    def output(self, exifData, classes, confidence, counter,
               birdCoordinates, yoloCoordinates):
        for w, x, y, z in zip(birdCoordinates, yoloCoordinates, 
                              classes, confidence):
            dateString = datetime.strptime(exifData['dateTime'], self.dateFormat)
            self.json = {'dateTime': dateString.strftime('%Y-%m-%d %H:%M:%S'),
                         'birdID': counter,
                         'class': y, 
                         'confidence': round(z, 3),
                         'species': "",
                         'birdNorthing': round(w[1], 2),
                         'birdEasting': round(w[0], 2),
                         'flightHeight_m': exifData['flightHeight_m'],
                         'pixelWidth': exifData['imageWidth'],
                         'pixelHeight': exifData['imageHeight'],
                         'center_x': x[0],
                         'center_y': x[1],
                         'box_width': x[2],
                         'box_height': x[3],
                         'filename': exifData['imageFile']}
            print(self.json)
            counter += 1
        return counter

class imageOut:
    def __init__(self):
        return 0

    def output(self, frame):
        return 0
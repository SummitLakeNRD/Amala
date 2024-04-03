import json
import cv2
import csv
import os
from datetime import datetime
from math import ceil
from PIL import Image
import numpy as np

class textOut:
    def __init__(self):
        self.json = {}
        self.dateFormat = "%Y:%m:%d %H:%M:%S"
        self.outputDir = os.path.join(os.getcwd(), "output")
        os.makedirs(self.outputDir, exist_ok=True)

    def output(self, exifData, classes, confidence, counter,
               birdCoordinates, yoloCoordinates):
        image_ids = []
        for w, x, y, z in zip(birdCoordinates, yoloCoordinates, 
                              classes, confidence):
            dateString = datetime.strptime(exifData['dateTime'], self.dateFormat)
            fileName = "duckData_" + str(counter) + ".json"
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
            image_ids.append(str(counter))
            counter += 1
            with open(os.path.join(self.outputDir, fileName), "w") as f:
                json.dump(self.json, f)
        return counter, image_ids

class imageOut:
    def __init__(self):
        self.font = cv2.FONT_HERSHEY_SIMPLEX
        self.thickness = 1
        self.fontColor = (255, 255, 255)
        self.fontSize = 1
        self.outputDir = os.path.join(os.getcwd(), "output")

    def output(self, frame, bbox, image_ids, image_counter):
        if len(bbox) == 0:
            return 0 
        else:
            imageName = "duckImage_" + str(image_counter) + ".png"
            centers = [(ceil((i[2] + i[0]) / 2),
                        ceil((i[3] + i[1]) / 2)) for i in bbox]
            frame = np.array(cv2.imread(frame))
            for a, b in zip(image_ids, centers):
                image = cv2.putText(frame, a, b, self.font, self.fontSize, 
                                    self.fontColor, self.thickness)
            cv2.imwrite(os.path.join(self.outputDir, imageName), image)
            image_counter += 1
            return image_counter
            
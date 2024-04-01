import os
from argparse import ArgumentParser
from src.imageProcessing import objectDetection
from src.spatialProcessing import exif, spatialProcess
from src.output import textOut
from datetime import datetime

parser = ArgumentParser()
parser.add_argument('imageDir', type=str, help='path/to/image/dir')
parser.add_argument('confThresh', type=float, help='Confidence threshold value (0-1) for ')
parser.add_argument('model', type=str, help='path/to/ai/file (ends with .pt)')
parser.add_argument('outputDir', type=str, help='path/to/output/directory')
args = parser.parse_args()


# Load classes and initialize main loop
od = objectDetection(args.model, args.confThresh)
exif = exif()
spatial = spatialProcess()
text = textOut()
counter = 0

###MAIN LOOP###
# Select image folder and loop through images performing inference
for image in os.listdir(args.imageDir):
    imageFile = os.path.join(args.imageDir, image)
    classes, confidence, boxes = od.inference(imageFile)

    # Pull exif data from images, specifically need the following:
    rawExifData = exif.dataGrab(imageFile)

    # Generate (x,y) utm location of bird from relative image position and image GPS location
    spatial.frameDims(rawExifData)
    rawExifData = spatial.utmConvert(rawExifData) 
    birdCoordsUTM, yoloCoords = spatial.pointUtmConvert(rawExifData, boxes) # returned in [easting, northing] format

    # Generate .json file for each image
    counter = text.output(rawExifData, classes, confidence, 
                          counter, birdCoordsUTM, yoloCoords)

    # Generate label image for assisted data entry
    counter += 1

###Exit main loop###

# Generate .csv from json files generated in main loop


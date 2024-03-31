import os
from argparse import ArgumentParser
from src.imageProcessing import objectDetection
from src.spatialProcessing import exif, spatialProcess

parser = ArgumentParser()
parser.add_argument('imageDir', type=str, help='path/to/image/dir')
parser.add_argument('confThresh', type=float, help='Confidence threshold value (0-1) for ')
parser.add_argument('model', type=str, help='path/to/ai/file (ends with .pt)')
args = parser.parse_args()


# Grab computer specs and load neural network
od = objectDetection(args.model, args.confThresh)
e = exif()
spatial = spatialProcess()

###MAIN LOOP###
# Select image folder and loop through images performing inference
for image in os.listdir(args.imageDir):
    imageFile = os.path.join(args.imageDir, image)
    classes, confidence, boxes = od.inference(imageFile)

    # Pull exif data from images, specifically need the following:
    rawExifData = e.dataGrab(imageFile)

    # Regenerate (x,y) image coordinates to create real UTM values for bird locations
    spatial.frameDims(rawExifData)
    rawExifData = spatial.utmConvert(rawExifData) 
    birdCoordsUTM = spatial.pointUtmConvert(rawExifData, boxes)

    # Apply bbox center location to new UTM (x,y) values

    # Generate .json file for each image

    # Generate label image for assisted data entry

###Exit main loop###

# Generate .csv from json files generated in main loop


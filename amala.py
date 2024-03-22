import os
from argparse import ArgumentParser
from src.imageProcessing import objectDetection
from src.spatialProcessing import exif

parser = ArgumentParser()
parser.add_argument('imageDir', type=str, help='path/to/image/dir')
parser.add_argument('confThresh', type=float, help='Confidence threshold value (0-1) for ')
parser.add_argument('model', type=str, help='path/to/ai/file (ends with .pt)')
args = parser.parse_args()


# Grab computer specs and load neural network
od = objectDetection(args.model, args.confThresh)
od.load()

e = exif(args.imageDir)

###MAIN LOOP###
# Select image folder and loop through images performing inference
for image in os.listdir(args.imageDir):
    imageFile = os.path.join(args.imageDir, image)
    classes, confidence, boxes = od.inference(imageFile)

# Pull exif data from images, specifically need the following:
    # GPS location
    # flight height
    # Image resolution/pixels per image (if avail?)
    # Date/time of image
    test = e.dataGrab(imageFile)
    print(imageFile)
    print(test)



# Regenerate (x,y) image coordinates to create real UTM values

# Apply bbox center location to new UTM (x,y) values

# Generate .json file for each image

# Generate label image for assisted data entry

###Exit main loop###

# Generate .csv from json files generated in main loop


import os
from argparse import ArgumentParser
from src.imageProcessing import objectDetection
from src.spatialProcessing import exif, spatialProcess
from src.output import textOut, imageOut, createExcel

parser = ArgumentParser()
parser.add_argument('imageDir', type=str, help='path/to/image/dir')
parser.add_argument('confThresh', type=float, help='Confidence threshold value (0-1) for duck detection')
parser.add_argument('model', type=str, help='path/to/ai/file (ends with .pt)')
args = parser.parse_args()



# Load classes and initialize main loop
od = objectDetection(args.model, args.confThresh)
exif = exif()
spatial = spatialProcess()
text = textOut()
images = imageOut()
excel = createExcel()

def main():
    # Select image folder and loop through images performing inference
    for image in os.listdir(args.imageDir):
        imageFile = os.path.abspath(os.path.join(args.imageDir, image))
        classes, confidence, boxes = od.inference(imageFile)

        # Pull exif data from images
        rawExifData = exif.dataGrab(imageFile)

        # Generate (x,y) utm location of bird from relative image position and image GPS location
        spatial.frameDims(rawExifData)
        rawExifData = spatial.utmConvert(rawExifData) 
        birdCoordsUTM, yoloCoords = spatial.pointUtmConvert(rawExifData, boxes) # returned in [easting, northing] format

        # Generate .json file for each image
        image_ids = text.output(rawExifData, classes, confidence, 
                                birdCoordsUTM, yoloCoords)

        # Generate label image for assisted data entry
        images.output(imageFile, boxes, image_ids)

    ###Exit main loop###
    # Generate .xlsx in 'output' folder from the json files generated in main loop
    excel.output(rawExifData)


if __name__ == '__main__':
    main()
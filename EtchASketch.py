#!/usr/bin/env python3

from PIL import Image
import glob, os, sys
OUTPUT_RES = (100, 100)


#takes in file path of image folder with .jpg extensions and returns newest file
def latestImage (filepath):

#defines variables for time stamp and file name
    latestfile= ""
    latestfiletime= 0.0

#iterates through all files returning file with greatest time stamp
    for infile in glob.glob(filepath):
        t= os.path.getmtime(infile)
        if (t >= latestfiletime):
            latestfiletime= t
            latestfile= infile
        
    return (latestfile)

def cropInput (inputSize, outputSize):

    inputW = inputSize [0] *1.0
    inputH = inputSize [1] *1.0

    outputW = outputSize [0] *1.0
    outputH = outputSize [1] *1.0

    inputRatio = (inputW)/(inputH)
    outputRatio = (outputW)/(outputH)

    while (inputRatio < outputRatio):
        inputH = inputH -1
        inputRatio = (inputW)/(inputH)
    while (inputRatio > outputRatio):
        inputW = inputW -1
        inputRatio = (inputW)/(inputH)

    return ((inputW, inputH))


def scaleRes (inputImage, croppedSize, outputSize)

    croppedW = croppedSize [0] *1.0
    croppedH = croppedSize [1] *1.0

    outputW = outputSize [0] *1.0
    outputH = outputSize [1] *1.0

    scaleRatio = outputH/croppedH

    im2ret = Image.new(mode = inputImage.mode, size = outputSize
#prints parameters from input
print (sys.argv)

#opens up latest image and transforms it
with Image.open(latestImage (sys.argv[1]),"r") as im:
    cropOutput = cropInput(im.size, OUTPUT_RES)
    print (cropOutput)
    print (im.format, im.mode, im.size, im.width, im.height)
# im.rotate(360-45).show()



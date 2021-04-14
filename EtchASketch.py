#!/usr/bin/env python3

from PIL import Image
import glob, os, sys
OUTPUT_RES = (10, 14)
debug = 1
TRESHOLD = 220

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
    if ( debug == 1):
        print (latestfile)
    return (latestfile)

#returns cropped image size to match aspect ratio of output res
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

#process input image to scaled up image
def scaleImg (inputImage, croppedSize, outputSize):

    croppedW = croppedSize [0] *1.0
    croppedH = croppedSize [1] *1.0

    outputW = outputSize [0] *1.0
    outputH = outputSize [1] *1.0

    scaleRatio = outputH/croppedH

    im2ret = Image.new(mode = inputImage.mode, size = outputSize)

    inputPixels = inputImage.load ()
    outputPixels = im2ret.load ()

    for x in range (int (croppedW)):
        for y in range (int (croppedH)):
            outputLowerX = x* scaleRatio
            outputLowerY = y* scaleRatio

            outputHighX = outputLowerX + scaleRatio
            outputHighY = outputLowerY + scaleRatio

            for oX in range (int (outputLowerX), int (outputHighX)):
                for oY in range (int (outputLowerY), int (outputHighY)):
                    outputPixels [oX, oY] = inputPixels [x,y]
    return (im2ret)
#return whether pixel is black or white
def isBlack (r,g,b):
    if (r+g+b >= TRESHOLD):
        return (False)
    else:
        return (True)
        
#input scaled imaged output new black and white version
def bwImgConvert (inputImg):

#created new image for output
    bwImage = Image.new(mode = inputImg.mode, size = inputImg.size)
    
    inputPixels = inputImg.load ()
    outputPixels = bwImage.load ()

    for x in range (inputImg.width):
        for y in range (inputImg.height):
            r,g,b = inputPixels[x,y]
            black = isBlack (r,g,b)
            if (black == True):
                outputPixels[x,y] = (0,0,0)
            else: 
                outputPixels[x,y] = (255,255,255)                           
            if (debug == 2):
                print (r,g,b)
    return (bwImage)
                
#-----MAIN PROGRAM START------

#prints parameters from input
if ( debug == 1):
    print (sys.argv)

#opens up latest image and transforms it
with Image.open(latestImage (sys.argv[1]),"r") as im:
    cropOutput = cropInput(im.size, OUTPUT_RES)
    if ( debug == 1):
        print (cropOutput)
        print (im.format, im.mode, im.size, im.width, im.height)

    outputImage = scaleImg (im, cropOutput, OUTPUT_RES)
    im.show()
    outputImage.show()
    bwImage = bwImgConvert (outputImage)
    bwImage.show()



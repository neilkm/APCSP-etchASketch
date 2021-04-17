#!/usr/bin/env python3
#imported Python package Pillow for loading images
from PIL import Image
#imported Python package glob for getting a file from a filepath
#imported Python package os for getting timestamp of file
#imported Python package sys for getting input parameters for getting the filepath from input
import glob, os, sys
OUTPUT_RES = (10, 10)
debug = 1
TRESHOLD = 220

#FUNCTION: latestImage
#INPUT: file path of image folder with .jpg extensions
#OUTPUT: returns newest file
#DESCRIPTION: Iterates through each file in a filepath and finds the
#             file with the largest timestamp value and returns it.
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

#FUNCTION: cropInput
#INPUT: input size of selected image and output size of final image
#OUTPUT: returns cropped image size to match aspect ratio of output resolution
#DESCRIPTION: looks at the aspect ratio of the output image and determines
#             whether the input image aspect ratio is greater or larger than it
#             . If input aspect ratio is larger then it subtracts pixels from
#             the width until the ratio is equal or smaller. If input aspect
#             ratio is smaller then it subtracts pixels from the hegiht until
#             the ratio is equal or smaller.
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

#FUNCTION: scaleImg
#INPUT: takes in the input image, size of the cropped image, size of the output
#       image 
#OUTPUT: returns scaled image
#DESCRIPTION: loads the collection of input image pixels and creates a new 
#             output image. Finds the scale ratio of the cropped image to the
#             output image. Multiplies the coordinates of each pixel in the
#             input image by the scale ratio to get the new image coordinates.
#             Duplicates the input image pixel to the new scaled image according
#             to the scale ratio. Averages out the color of overlapping pixels
#             when scaling to a lower resolution.
def scaleImg (inputImage, croppedSize, outputSize):

    croppedW = croppedSize [0] *1.0
    croppedH = croppedSize [1] *1.0

    outputW = outputSize [0] *1.0
    outputH = outputSize [1] *1.0

    scaleRatio = outputH/croppedH

    im2ret = Image.new(mode = inputImage.mode, size = outputSize)
    outputPixelStatus = {}

    for x in range ( int(outputW)):
        for y in range ( int(outputH)):
            outputPixelStatus [(x, y)] = 1

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
                        Ri,Gi,Bi, = inputPixels [x,y]
                        Ro,Go,Bo, = outputPixels [oX,oY]
                        avg =  outputPixelStatus [(oX, oY)]
                        Rf = int ((Ro*(avg - 1) + Ri)/avg)
                        Gf = int ((Go*(avg - 1) + Gi)/avg)
                        Bf = int ((Bo*(avg - 1) + Bi)/avg)
                        outputPixels [oX,oY] = (Rf, Gf, Bf)
                        outputPixelStatus [(oX, oY)] = outputPixelStatus [(oX,oY)] + 1
    return (im2ret)
#FUNCTION: isBlack
#INPUT: rgb values of a pixel
#OUTPUT: false if white, true if black
#DESCRIPTION: returns whether pixel is black or white by adding up the r, g,
#             and b values by determining whether the sum is below or above a
#             predetermined THRESHOLD value.
def isBlack (r,g,b):
    if (r+g+b >= TRESHOLD):
        return (False)
    else:
        return (True)
        
#FUNCTION: bwImgConvert
#INPUT: input the scaled image
#OUTPUT: the black and white version
#DESCRIPTION: loads a new image with the output size. iterates through each
#             pixel and runs it through 'isBlack' function. If isBlack returns
#             true then the output pixel will be black else white.
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
#takes input from the screen and stores it in a variable
filepath = input("Input file location: ")

#opens up latest image and transforms it
with Image.open(latestImage (filepath),"r") as im:
    cropOutput = cropInput(im.size, OUTPUT_RES)
    if ( debug == 1):
        print (cropOutput)
        print (im.format, im.mode, im.size, im.width, im.height)

    outputImage = scaleImg (im, cropOutput, OUTPUT_RES)
    im.show()
    outputImage.show()
    bwImage = bwImgConvert (outputImage)
    bwImage.show()



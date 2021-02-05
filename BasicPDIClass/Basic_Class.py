# -*- coding: utf-8 -*-
"""
Created on Fri Aug 03 21:57:24 2018

@author: Rodrigo
"""

import cv2
import numpy as np

##Index Database:
class Basic_PDI_Functions():
    #Morfologia
    #Media entre duas images
    #And
    """
    ThresholdBinarize just need an image, a threshold and optionally a value different than 255 to set
    to return an binarized image with your threshold
    """
    def ThresholdBinarize(self,img,thr,value = 255):
        if(value > 255) or (value < 0):
            value = 255
            print ("Set a value with value is between 0 and 255")
        ret,output = cv2.threshold(img, thr , value,cv2.THRESH_BINARY)
        return output
    """ 
        Otsu just need an image and optionally a value different than 255 to set
        to return an otsu binarized image
    """
    def Otsu(self,img,value = 255):
        if(value > 255) or (value < 0):
            value = 255
            print ("Set a value with value is between 0 and 255")
        ret, output = cv2.threshold(img,0, value ,cv2.THRESH_BINARY+ cv2.THRESH_OTSU)
        return output
    """
        GaussianOtsu takes an image and optionally a value different than 255 to set
        it applies a blur before the Otsu binarization
        to return a binarized image
    """
    def GaussianOtsu(self,img,value = 255):
        if(value > 255) or (value < 0):
            value = 255
            print ("Set a value with value is between 0 and 255")
        blur = cv2.GaussianBlur(img,(5,5),0)
        return self.Otsu(blur,value)
    """
        Average takes two different images
        to return the average between them
    """
    def Average(self,img1,img2):
        return (img1 + img2) / 2
    
    """
    
    """
    def HorizontalSplit(self,img):
        height = img.shape[0]
        width = img.shape[1]
        width1 = (width / 2).astype(int)
        if(width1 * 2 == width):
            width2 = width1
        elif(width1 * 2 > width):
            width2 = width1 -1
        else:
            width2 = width1 + 1
        return 0

    def SelectChannel(self, img, channel):
        blue,green,red = cv2.split(img)
        if((channel == "Red") or (channel == "red") or (channel == "R") or (channel == "RED") or (channel == "r")):
            return red
        elif((channel == "Green") or (channel == "green") or (channel == "G") or (channel == "GREEN") or (channel == "g")):
            return green
        elif((channel == "Blue") or (channel == "blue") or (channel == "B") or (channel == "BLUE") or (channel == "b")):
            return blue

    def Dimension(self, array):
        height = array.shape[0]
        width= array.shape[1]
        channels = array.shape[2]
        return [height, width, channels]
    
    def Create(self, height, width, channel = 0):
        if channel == 0:
            return np.zeros((height,width))
        return cv2.merge((np.zeros((height,width)),np.zeros((height,width)),np.zeros((height,width))))

    def CreateAs(self, image):
        height, width, channels = self.Dimension(image)
        return self.Create(height, width, channels)

    def Filter(self, image, mask):
        return cv2.filter2D(image, cv2.CV_64F, mask)
    
    def FilterRGB(self, RGB, mask,R = 1, G = 1, B = 1):
        blue, green, red = cv2.split(RGB)
        default_mask = np.array([[0,0,0], [0,1,0], [0,0,0]])
        if B == 1:
            blue = self.Filter(blue, mask)
        else:
            blue = self.Filter(blue, default_mask)
        if G == 1:
            green = self.Filter(green, mask)
        else:
            green = self.Filter(green, default_mask)
        if R == 1:
            red = self.Filter(red, mask)
        else:
            red = self.Filter(red, default_mask)
        return cv2.merge((blue,green,red))
"""
    Fontes:
        https://docs.opencv.org/3.4.0/d7/d4d/tutorial_py_thresholding.html
"""
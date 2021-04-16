# -*- coding: utf-8 -*-
"""
    Rodrigo Schardong
    Space Filters
"""

import cv2
import numpy as np
from math import sqrt

class Filter_Functions():
    
    def Sobel_Gx(self,image):
        gx = np.zeros((self.height,self.width))
        mask = np.array([[-1,0,1],[-2,0,2],[-1,0,1]])
        gx = cv2.filter2D(image,cv2.CV_64F,mask)
        #cv2.imwrite("Sobel_Gx.png",gx)
        return gx
    
    def Sobel_Gy(self,image):
        gy = np.zeros((self.height,self.width))
        mask = np.array([[1,2,1],[0,0,0],[-1,-2,-1]])
        gy = cv2.filter2D(image,cv2.CV_64F,mask)
        #cv2.imwrite("Sobel_Gy.png",gy)
        return gy
    
    def Sobel_Sqrt(self,gx,gy):
        output = np.zeros((self.height,self.width))
        for x in range (0,self.width):
            for y in range(0,self.height):
                gx[y,x] = gx[y,x] * gx[y,x]
                gy[y,x] = gy[y,x] * gy[y,x]
                output[y,x] = gx[y,x] + gy[y,x]
                output[y,x] = sqrt(output[y,x])
                if(output[y,x] > 255):
                    output[y,x] = 255
                elif(output[y,x] < 0):
                    output[y,x] = 0
        return output.astype(int)

    def Sobel(self,image):
        self.height = image.shape[0]
        self.width = image.shape[1]
        gx = self.Sobel_Gx(image)
        gy = self.Sobel_Gy(image)
        return self.Sobel_Sqrt(gx,gy)
    
    def Sobel_RGB(self,image):
        blue,green,red = cv2.split(image)
        blue = self.Sobel(blue)
        green = self.Sobel(green)
        red = self.Sobel(red)
        return cv2.merge((blue,green,red))
    
    def Even_Convolve(self, image, mask, y, x):
        pixel = 0
        for mY in range(self.mHeight):
            for mX in range(self.mWidth):
                pixel += image[y + mY - (int)( self.mHeight / 2) - 1, x + mX - (int)(self.mWidth / 2) - 1] * mask[mY, mX]
        return pixel
    
    def Even_Convolution(self, image, mask):
        #Lost Colluns and Lines
        highCut = (int)(self.mHeight / 2) - 1
        lowCut = (int)(self.mHeight / 2)
        leftCut = (int)(self.mWidth / 2) - 1
        rightCut = (int)(self.mWidth / 2)
        
        #Output Image Dimension
        outHeight = self.height - lowCut - highCut
        outWidth = self.width - rightCut - leftCut
        output = np.zeros((outHeight, outWidth ))
        
        for y in range (highCut, self.height - lowCut):
            for x in range (leftCut, self.width - rightCut):
                output[y - highCut, x - leftCut] = (int) (self.Even_Convolve(image, mask, y, x))
        return output
                
    def Odd_Convolve(self, image, mask, y, x):
        pixel = 0
        for mY in range(self.mHeight):
            for mX in range(self.mWidth):
                pixel += image[y + mY - (int)( self.mHeight / 2), x + mX - (int)(self.mWidth / 2)] * mask[mY, mX]
        return pixel
    
    def Odd_Convolution(self, image, mask):
        #Lost Colluns and Lines
        highCut = (int)(self.mHeight / 2)
        lowCut = (int)(self.mHeight / 2)
        leftCut = (int)(self.mWidth / 2)
        rightCut = (int)(self.mWidth / 2)
        
        #Output Image Dimension
        outHeight = self.height - lowCut - highCut
        outWidth = self.width - rightCut - leftCut
        output = np.zeros((outHeight, outWidth ))
        
        for y in range (highCut, self.height - lowCut):
            for x in range (leftCut, self.width - rightCut):
                output[y - highCut, x - leftCut] = (int) (self.Odd_Convolve(image, mask, y, x))
        return output
    
    def Generic_Convolution(self, image, mask, manual = False):
        if(manual == False):
            return cv2.filter2D(image,cv2.CV_64F,mask)
            
        else:
            #Getting Image chracteristics
            self.height = image.shape[0]
            self.width = image.shape[1]
            #Getting Mask chracteristics
            self.mHeight = mask.shape[0]
            self.mWidth = mask.shape[1]
            
            #Check if mask is a square array
            if(self.mHeight == self.mWidth):
                if((self.mHeight % 2) == 0):
                    #Even array
                    return self.Even_Convolution(image, mask)
                else:
                    return self.Odd_Convolution(image, mask)
                
    def Blur(self, image, manual = False):
        mask = np.ones((3,3)) / 9
        return self.Generic_Convolution(image, mask, manual)
    
    def Laplacian(self, image, manual = False):
        mask = np.array([[-1,-1,-1], [-1,8,-1], [-1,-1,-1]])
        return self.Generic_Convolution(image, mask, manual)
    
    def Generic_Discrete_Wavelet_Transform(self, image, level, lowMask, highMask, manual = False):
        for l in range (level - 1):
            image = self.Generic_Convolution(image, lowMask, manual)
        highPass = self.Generic_Convolution(image, highMask, manual)
        lowPass = self.Generic_Convolution(image, lowMask, manual)
        
        return lowPass, highPass
    
    def Show_High_Pass_Borders(self, image, filtered):
        if(image.shape[0] < filtered.shape[0]):
            self.height = image.shape[0]
            self.width = image.shape[1]
        else:
            self.height = filtered.shape[0]
            self.width = filtered.shape[1]
        for y in range (self.height):
            for x in range (self.width):
                image[y,x] += filtered[y,x]
                if(image[y,x] > 255):
                    image[y,x] = 255
        return image
                
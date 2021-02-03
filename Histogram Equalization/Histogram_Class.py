# -*- coding: utf-8 -*-
"""
Created on Sun Jun 17 22:03:44 2018

@author: Rodrigo
"""

import cv2
import numpy as np

"""
    The Main functions will be signed with ######### before them
"""

class Histogram_Functions():
    #IDEIAS
    #Criar/adaptar as funções para inserir uma outra imagem binaria para indicar onde deve ser histogramado
    """
        Histogram_Assembler takes an array with 256 spaces a thereshold number that was genererated by the function Histogram_Creator
        it creates an histogram image
        to return this image
    """
    def Histogram_Assembler(self,array,maximum): 
        histogram = np.zeros((maximum + 1, 256))
        for x in range (0,256):
            for y in range (maximum,0,-1):
                if array[x] > 0:
                    histogram[y,x] = 255
                    array[x] -= 1
                else:
                    y = 0
        return histogram
    """
        Histogram_Array_Creator takes a grey image,
        count how many pixels for each value between 0 and 255 and save in one array
        to return this array
    """
    def Histogram_Array_Creator(self,img): 
        height = img.shape[0]
        width = img.shape[1]  
        counter = np.zeros((256))
        for x in range (0,width):
            for y in range (0,height):
                counter[img[y,x]] += 1
        return counter
    """
        Histogram_Creator takes a grey image and an array with 256 spaces
        it creates values to send to the function Histogram_Assemler for receive an Histogram Image
        it return the histogram image
    """
    def Histogram_Creator(self,img,counter): #This function is to start to assemble the histogram image
        maximum = 0
        for x in range (0,256):
            if counter[x] > maximum:
                maximum = counter[x]
        #here will be just to ajust the dimensions to create the histogram image
        ajuster = maximum / 256
        counter = np.round(counter / (ajuster * 2)).astype(int)
        maximum = np.round(maximum / (ajuster * 2)).astype(int)
        return self.Histogram_Assembler(counter,maximum)
    """
        ProbabilityMassFunction takes an array with 256 spaces and the sum of all numbers in this array
        it creates a new array where each space is equal to the entered array divided by the sum
        the function returns the new array that is de Probability Mass
    """
    def ProbabilityMassFunction(self,array,total): #This function is to store in a new array the chance to find a pixel with a value "x" in the image
        pmf = np.zeros((256)).astype(float)
        for x in range (0,256):
            pmf[x] = (array[x])/total
        return pmf
    """
        CumulativeDistributionFunction takes an array with 256 spaces that I recomend be a probability mass array
        to return a cumulative distribution array
    """
    def CumulativeDistributionFunction(self,pmf): #This function is to store in a new array the chance to find a pixel with a value lower than "x" in the image
        cdf = np.zeros((256)).astype(float)
        cdf[0] = pmf[0]
        for x in range (1,256):
            cdf[x] = cdf[x - 1] + pmf[x]
        return cdf
    """
        Equalied_Image_Assembler takes an image and one array that I recomend be a Cumulative disctribution array
        to create an Histogramed image
        and return this Histogramed image
    """
    def Equalized_Image_Assembler(self,img,array): #This function is to create the final image with the normalized array
        height = img.shape[0] # The height of the image array
        width = img.shape[1] # The width of the image array
        equalized = np.zeros((height,width))
        for x in range (0,width):
            for y in range(0,height):
                equalized[y,x] = array[img[y,x]]
        return equalized
    ###########################
    def Histogram(self,img):
        counter = self.Histogram_Array_Creator(img)
        histogram = self.Histogram_Creator(img,counter)
        return (255 - histogram)
    """
        Histogram_Equalization get a grey image and the image name,
        it does an Histogram in the image,
        and return an histogramed image
    """
    ###########################
    def Histogram_Equalization(self,img,name = "image"):
        height = img.shape[0] # The height of the image array
        width = img.shape[1]  # The width of the image array
        counter = self.Histogram_Array_Creator(img)
        histogram = self.Histogram_Creator(img,counter)
    
        pmf = self.ProbabilityMassFunction(counter,height*width)
            
        cdf = self.CumulativeDistributionFunction(pmf)
        
        normalized = np.round(cdf * 255).astype(int)
        
        equalized = self.Equalized_Image_Assembler(img,normalized)
        
        cv2.imwrite(name + "_shape.png",img)
        histogram_neg = 255 - histogram
        cv2.imwrite(name + "_histogram.png",histogram_neg)
        cv2.imwrite(name + "_shape_equalized.png",equalized)
        return equalized
    
    """
        RGB_Equalization get a RGB image,
        it does an Histogram in each channel,
        and return an histogramed RGB image
    """
    ###########################
    def RGB_Equalization(self,img,r = 1, g = 1, b = 1): #Verificar quando um dos valores é FALSO pq ta DANDO ERRO
        blue,green,red = cv2.split(img)
        if b == 1:
            blue_eq = self.Histogram_Equalization(blue,"blue")
        else:
            blue_eq = blue.astype(float)
        if g == 1:
            green_eq = self.Histogram_Equalization(green,"green")
        else:
            green_eq = green.astype(float)
        if r == 1:
            red_eq = self.Histogram_Equalization(red,"red") 
        else:
            red_eq = red.astype(float)
        img = cv2.merge((blue_eq,green_eq,red_eq))
        return img

    """
        CumulativeDistributionBinarization
    """
    def CumulativeDistributionBinarization(self,cdf,threshold):
        for x in range (0,256):
            if cdf[x] >= threshold:
                return x
    
    """
        Histogram_Binarization gets a grey image and an threshold
        It does a binarization acording to the threshold and the Cumulative Distribution
        and return a Histrogram Binarizated image
    """
    ###########################
    def Histogram_Binarization(self,img,threshold = 0.5):
        height = img.shape[0] # The height of the image array
        width = img.shape[1]  # The width of the image array
        counter = self.Histogram_Array_Creator(img)
        pmf = self.ProbabilityMassFunction(counter,height*width)
        cdf = self.CumulativeDistributionFunction(pmf)
        if threshold < 1 and threshold > 0:
            binaryThreshold = self.CumulativeDistributionBinarization(cdf,threshold)
        else:
            print ("Try another value between 0 and 1")
            return img
        ret,output = cv2.threshold(img,binaryThreshold,255,cv2.THRESH_BINARY)
        return output
            
        
        
    
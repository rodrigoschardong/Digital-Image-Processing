"""
    Rodrigo Schardong
    Dithering
"""

import cv2
import numpy as np

#     https://medium.com/100-days-of-algorithms/day-96-floyd-steinberg-7c5b25ee0a65
#     https://research.cs.wisc.edu/graphics/Courses/559-s2004/docs/floyd-steinberg.pdf

class Floyd_Steinberg_Dithering_Functions():
    
    def binarization(self, img, threshold = -1):
        if(threshold >= 0):
            height = img.shape[0] # The height of the image array
            width = img.shape[1] # The width of the image array
            out = np.zeros((height,width))
            
            for y in range (height):
                for x in range (width):
                    if(img[y,x] > threshold):
                        out[y,x] = 255
                    else:
                        out[y,x] = 0
        else:
            ret, out = cv2.threshold(img,0, 255 ,cv2.THRESH_BINARY+ cv2.THRESH_OTSU)
        return out
    
    def pixelBinarization(self, pixel, threshold):
        if(pixel < threshold):
            pixel = 0
        else:
            pixel = 255
        return pixel
    
    def Floyd_Steinberg(self, image, threshold):
        height = image.shape[0]
        width = image.shape[1]
        #out = np.zeros((height,width), dtype = float)
        out = image.astype(float)
        
        #mask = np.array([[0, 0, 0,], [0, 0, 7], [3, 5, 1]], dtype = float) / 16
        
        
        for y in range (0, height- 1):
            for x in range(1, width - 1):
                oldPixel = out[y,x]
                out[y,x] = self.pixelBinarization(oldPixel, threshold)
                error = oldPixel - out[y,x]
                
                out[y    , x + 1] += error * 7/16 
                out[y + 1, x - 1] += error * 3/16 
                out[y + 1, x    ] += error * 5/16 
                out[y + 1, x + 1] += error * 1/16 
                
        return out   

import cv2
import numpy as np

class Frequency_Filters_Functions():
    
    def SetValueOnCenter(self, array, value, percent, form = "square"):
        if(percent > 100 or percent < 0):
            raise Exception('Put a percent value between 0 and 100')
        else:
            percent = np.sqrt(percent) / 10
            
            height = array.shape[0]
            width = array.shape[1]
            
            centerY = (height -1) / 2
            centerX = (width -1) / 2
            
            highY = height - centerY - (height * percent /2)
            lowY = centerY + (height * percent /2)
            if((highY % 1) != 0):
                #highY -= 1
                lowY += 1
            highX = width - centerX - (height * percent /2)
            lowX = centerX + (width * percent /2)
            if((highX % 1) != 0):
                #highX -= 1
                lowX += 1
                
            if(form == "square"):
                array[int(highY) : int(lowY), int(highX) : int(lowX)] = value
            if(form == "circle"):
                if(width == height):
                    array = cv2.circle(array, (int(centerX), int(centerY)), int(height * percent /2), value, -1 )
                else:
                    array = cv2.ellipse(array, (int(centerX), int(centerY)),(int((lowX - highX)*0.8), int((lowY - highY)*0.8)),
                           0, 0, 360, value, -1 )
            return array
    
    def FourierTransform(self, image):
        height = image.shape[0]
        width = image.shape[1]

        realPart = np.zeros((height, width))
        imaginaryPart= np.zeros((height, width))
        
        #Loops to create all output image pixels
        for outY in range (height):
            for outX in range (width):
                
                #Loop to create a single output pixel
                for y in range (height):
                    for x in range (width):
                        summation = ((outY * y) / height) + ((outX * x) / width) 
                        angle = (-2) * np.pi * summation
                        realPart[outY, outX] += image[y,x] * np.cos(angle)
                        imaginaryPart[outY, outX] += image[y,x] * np.sin(angle)
                        
                realPart[outY, outX] = realPart[outY, outX] / (width * height)
                imaginaryPart[outY, outX] = imaginaryPart[outY, outX] / (width * height)
        return realPart, imaginaryPart
    
    def InverseFourierTransform(self, realPart, imaginaryPart):
        if(np.shape(realPart) == np.shape(imaginaryPart)):
            height = realPart.shape[0]
            width = realPart.shape[1]
            output = np.zeros((height, width))
            
            #Loops to create all output image pixels
            for outY in range (height):
                for outX in range (width):
                    
                    #Loop to create a single output pixel
                    for y in range (height):
                        for x in range (width):
                            summation = ((outY * y) / height) + ((outX * x) / width) 
                            angle = 2 * np.pi * summation
                            output[outY, outX] += realPart[y,x] * np.cos(angle)
                            output[outY, outX] -= imaginaryPart[y,x] * np.sin(angle)
                            
                    output[outY, outX] = output[outY, outX] / (width * height)
            return output
        else:
            print("Vish")
            return -1
        
    def FrequencyFilter(self, image, threshold, filterType = "LowPass"):
        realImg, imaginaryImg = self.FourierTransform(image)

        threshold = threshold ** 2
        height = realImg.shape[0]
        width = realImg.shape[1]

        for y in range (height):
            for x in range (width):
                freq = (x ** 2) + (y ** 2)
                if((filterType == "LowPass") and (freq > threshold)):
                    realImg[y,x] = 0
                    imaginaryImg[y,x] = 0
                elif((filterType == "HighPass") and (freq < threshold)):
                    realImg[y,x] = 0
                    imaginaryImg[y,x] = 0

        return self.InverseFourierTransform(realImg, imaginaryImg)

    def BandPassFilter(self, image, thresholdLow, thresholdHigh):
        if(thresholdLow >= thresholdHigh):
            print("ERROR: thresholdLow is >= thresholdHigh")
            return image
        realImg, imaginaryImg = self.FourierTransform(image)

        thresholdLow = thresholdLow ** 2
        thresholdHigh = thresholdHigh ** 2

        height = realImg.shape[0]
        width = realImg.shape[1]

        for y in range (height):
            for x in range (width):
                freq = (x ** 2) + (y ** 2)
                if((freq < thresholdLow) and (freq > thresholdHigh)):
                    realImg[y,x] = 0
                    imaginaryImg[y,x] = 0
        return self.InverseFourierTransform(realImg, imaginaryImg)

    def BandRejectFilter(self, image, thresholdLow, thresholdHigh):
        if(thresholdLow >= thresholdHigh):
            print("ERROR: thresholdLow is >= thresholdHigh")
            return image
        realImg, imaginaryImg = self.FourierTransform(image)

        thresholdLow = thresholdLow ** 2
        thresholdHigh = thresholdHigh ** 2
        height = realImg.shape[0]
        width = realImg.shape[1]

        for y in range (height):
            for x in range (width):
                freq = (x ** 2) + (y ** 2)
                if((freq > thresholdLow) and (freq < thresholdHigh)):
                    realImg[y,x] = 0
                    imaginaryImg[y,x] = 0
        return self.InverseFourierTransform(realImg, imaginaryImg)

    def ButterworthFilter(self, image, threshold, order = 1):
        realImg, imaginaryImg = self.FourierTransform(image)

        height = realImg.shape[0]
        width = realImg.shape[1]

        for y in range (height):
            for x in range (width):
                freq = np.sqrt((x ** 2) + (y ** 2))
                filt = 1 / (1 + (freq / threshold) ** (2 * order))
                realImg[y,x] = realImg[y,x] * filt
                imaginaryImg[y,x] = imaginaryImg[y,x] * filt
        
        return self.InverseFourierTransform(realImg, imaginaryImg)
        
        
        
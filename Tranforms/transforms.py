import cv2
import numpy as np
import math
import sys

class Transforms_Functions():
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

    def CreateHadamarArraySection(self, order, array):
        if((order / 2) == 1):
            array[1,1] = -1
            return array
        else:
            array[0 : int(order /2), 0 : int(order /2)] = self.CreateHadamarArraySection(int(order / 2), array[0 : int(order /2), 0 : int(order /2)])
            array[0 : int(order /2), int(order /2) : order] = self.CreateHadamarArraySection(int(order / 2), array[0 : int(order /2), int(order /2) : order])
            array[int(order /2) : order, 0 : int(order /2)] = self.CreateHadamarArraySection(int(order / 2), array[int(order /2) : order, 0 : int(order /2)])
            array[int(order /2) : order, int(order /2) : order] = -self.CreateHadamarArraySection(int(order / 2), array[int(order /2) : order, int(order /2) : order])
            return array
    def CreateHadamarArray(self, order):
        array = np.ones((order, order))
        return self.CreateHadamarArraySection(order, array)

    def HadamarTransform(self, image):
        height = image.shape[0]
        width = image.shape[1]

        if(height >= width):
            smaller = width
        else:
            smaller = height
        
        order = int(math.log2(smaller))
        output = np.zeros((smaller, smaller))
        widthDif = width - (2 ** order)
        heightDif = height - (2 ** order)
        
        hadamarArray = self.CreateHadamarArray(2 ** order)
        #print(hadamarArray.shape)
        output = np.matmul(hadamarArray, image[0 : height - heightDif, 0 : width - widthDif])
        output = np.matmul(output, hadamarArray)
        return (output / (2 ** (order * 2)))

    def InverseHadamarTransform(self, image):
        return self.HadamarTransform(image)

    def OrderHadamarArray(self, array):
        lengh = array.shape[0]
        lineChanges = np.zeros(lengh, dtype = int)
        output = np.zeros((lengh, lengh))

        #Counting
        for y in range(lengh):
            for x in range (lengh):
                if(x == 0):
                    signal = array[y,x]
                elif(signal != array[y,x]):
                    signal = array[y,x]
                    lineChanges[y] += 1
        ##Ordering
        lineAuxiliar = np.zeros((1, lengh))
        for y in range (lengh):
            output[lineChanges[y], :] = array[y, :]
        return output

    def CreateWalshArray(self, order):
        hadamarArray = self.CreateHadamarArray(order)
        walshArray = self.OrderHadamarArray(hadamarArray)
        return walshArray

    
    def WalshTransform(self, image):
        height = image.shape[0]
        width = image.shape[1]

        if(height >= width):
            smaller = width
        else:
            smaller = height
        
        order = int(math.log2(smaller))
        output = np.zeros((smaller, smaller))
        widthDif = width - (2 ** order)
        heightDif = height - (2 ** order)
        
        walshArray = self.CreateWalshArray(2 ** order)
        output = np.matmul(walshArray, image[0 : height - heightDif, 0 : width - widthDif])
        output = np.matmul(output, walshArray)
        return (output / (2 ** (order * 2)))

    def InverseWalshTransform(self, image):
        height = image.shape[0]
        width = image.shape[1]

        if(height >= width):
            smaller = width
        else:
            smaller = height
        
        order = int(math.log2(smaller))
        output = np.zeros((smaller, smaller))
        widthDif = width - (2 ** order)
        heightDif = height - (2 ** order)
        
        walshArray = self.CreateWalshArray(2 ** order)
        walshArray = np.transpose(walshArray)
        output = np.matmul(walshArray, image[0 : height - heightDif, 0 : width - widthDif])
        output = np.matmul(output, walshArray)
        return (output / (2 ** (order * 2)))

    def CreateHaarArray(self, order):
        N = order 
        array = np.ones((N, N))
        z = np.arange(0, 1, (1 / N))
        k = np.arange(0, N)
        p = np.zeros(N, dtype = int)
        q = np.zeros(N, dtype = int)

        for i in range(1, N):
            while(((2 ** p[i]) + q[i] - 1) != k[i]):
                if(p[i] == 0):
                    if(q[i] == 0):
                        q[i] += 1
                    else:
                        p[i] = 1
                else:
                    if(q[i] <= (2 ** p[i]) -1):
                        q[i] += 1
                    else:
                        q[i] = 1
                        p[i] += 1

        for y in range (1,N):
            for x in range (N):
                if((((q[y] - 1)/ (2**p[y])) <= z[x]) and (z[x] < ((q[y] - 0.5)/(2 ** p[y])))):
                    array[y,x] = 2 ** (p[y] / 2)
                elif((((q[y] - 0.5)/ (2**p[y])) <= z[x]) and (z[x] < ((q[y]/(2 ** p[y]))))):
                    array[y,x] = -2 ** (p[y] / 2)
                else:
                    array[y,x] = 0
        return array / (np.sqrt(N))

    def HaarTransform(self, image):
        height = image.shape[0]
        width = image.shape[1]

        if(height >= width):
            smaller = width
        else:
            smaller = height
        
        order = int(math.log2(smaller))
        output = np.zeros((smaller, smaller))
        widthDif = width - (2 ** order)
        heightDif = height - (2 ** order)

        HaarArray = self.CreateHaarArray(2 ** order)
        output = np.matmul(HaarArray, image[0 : height - heightDif, 0 : width - widthDif])
        output = np.matmul(output, HaarArray)
        return (output / (2 ** (order * 2)))

    def InverseHaarTransform(self, image):
        height = image.shape[0]
        width = image.shape[1]

        if(height >= width):
            smaller = width
        else:
            smaller = height
        
        order = int(math.log2(smaller))
        output = np.zeros((smaller, smaller))
        widthDif = width - (2 ** order)
        heightDif = height - (2 ** order)

        HaarArray = self.CreateHaarArray(2 ** order)
        #HaarArray = np.transpose(HaarArray)
        HaarArray = HaarArray.T
        output = np.matmul(HaarArray, image[0 : height - heightDif, 0 : width - widthDif])
        output = np.matmul(output, HaarArray)
        return (output / (2 ** (order * 2)))

"""
    @author: Rodrigo Schardong
"""

import numpy as np
from matplotlib import pyplot as plt

class Hough_Functions():
    """
        Inputs: image in a array
                threshold for pixels

        output: Number of pixels bigger than threshold
    """
    def CountPixels(self, image, threshold = 255):
        height = image.shape[0]
        width = image.shape[1]
        
        numPixels = 0
        
        for y in range(height):
            for x in range(width):
                if(image[y,x] >= threshold):
                    numPixels += 1
        return numPixels

    """
        Inputs: image in a array
                threshold for pixels
        
        output: Coordinates of pixels bigger than threshold
    """
    def GetPixels(self, image, threshold = 255):
        numPixels = self.CountPixels(image, threshold)
        pixels = np.zeros((numPixels, 2), dtype = int)

        height = image.shape[0]
        width = image.shape[1]
        i = 0
        for y in range (height):
            for x in range (width):
                if(i >= numPixels):
                    return pixels
                elif(image[y , x] >= threshold):
                    pixels[i, 0] = int(y)
                    pixels[i, 1] = int(x)
                    i += 1
        return pixels

    """
        Inputs: Pixels Coordinates
                Angles in Rad

        Output:
                Ro(angles) for each pixel
    """
    def GetRos(self, pixels, angles):
        numPixels = pixels.shape[0]
        numAngles = angles.shape[0]

        ro = np.zeros((numPixels, numAngles), dtype = float)

        for p in range (numPixels):
            for a in range (numAngles):
                ro[p,a] = pixels[p,1] * np.cos(angles[a]) + pixels[p, 0] * np.sin(angles[a])
        return ro

    """
        Inputs: image in a array
                threshold for pixels 

        Plot:   Sinusoids for each pixel filtered
    """
    def PlotHoughSins(self, image, threshold = 255):
        pixels = self.GetPixels(image, threshold)

        angleDegrees = np.arange(-180, 181, 1)
        angleRad = angleDegrees * np.pi / 180
        ro = self.GetRos(pixels, angleRad)

        #plot
        f,a = plt.subplots(ncols = 2, figsize = (20,5))
        a[0].imshow(image, cmap='gray')
        a[0].set_title('Image')
        a[1].set_title('Sinusoid')

        for p in range (pixels.shape[0]):
            a[1].plot(angleDegrees, ro[p, :])
        
        plt.show()  

    """
        Inputs: ros in a array
                deviation for ros 

        Output: Number of crossed sinusoids in p(theta)
    """
    def CountHoughSins(self, ro, deviation = 0.1):
        sins = ro.shape[0]
        angles = ro.shape[1]

        numHoughSins = np.zeros((sins, angles), dtype = int)
        dif = 0.0
        for s in range (sins - 1):
            for a in range (angles):
                for S in range (s +  1, sins):
                    dif = ro[s,a] - ro[S,a]
                    if(dif > -deviation and dif < deviation):
                        numHoughSins[s, a] += 1
                        numHoughSins[S, a] += 1
        return numHoughSins

    """
        output: Filtered Pixels Ids
    """
    def FilterSinusoids(self, ro, threshold, deviation = 0.1):
        numHoughSins = self.CountHoughSins(ro, deviation)
        #Filter
        filtered = [0]
        index = 0
        for s in range (ro.shape[0]):
            for a in range (ro.shape[1]):
                if(numHoughSins[s, a] >= threshold):
                    if(index == 0):
                        filtered[index] = s
                        index += 1
                    else:
                        filtered.append(s)
                        index += 1
        #Erase same sinusoid
        pixels = [-1]
        j = 0
        for i in range (index):
            if(filtered[i] != pixels[j]):
                pixels.append(filtered[i])
                j += 1
        pixels.remove(-1)
        index = j
        #Transform List to an array
        output = np.zeros(j, dtype = int)
        for i in range(j):
            output[i] = pixels[i]
        return output

    def HoughLineFilter(self, image, linesThreshold, pixelThreshold = 255, deviation = 0.1):
        pixels = self.GetPixels(image, pixelThreshold)

        angleDegrees = np.arange(-180, 181, 1)
        angleRad = angleDegrees * np.pi / 180
        ro = self.GetRos(pixels, angleRad)
        filteredPixels = self.FilterSinusoids(ro, linesThreshold, deviation)

        output = np.zeros(image.shape)
        for s in range(filteredPixels.shape[0]):
            output[pixels[filteredPixels[s],0], pixels[filteredPixels[s], 1]] = 255
        return output

    def CreateLine(self, image, ro, theta):
        height = image.shape[0]
        width = image.shape[1]
        for x in range(width):
            try:
                y = int((ro - (x * np.cos(theta))) / np.sin(theta))
                if(y < 0):
                    y = 0
                image[y, x] = 255
            except:
                y = height - 1
                image[y, x] = 255
        for y in range(height):
            try: 
                x = int((ro - (y * np.sin(theta))) / np.cos(theta))
                if(x < 0):
                    x = 0
                image[y, x] = 255
            except:
                x = width - 1
                image[y, x] = 255
        return image

    def HoughLinesTransform(self, image, linesThreshold, pixelThreshold = 255, deviation = 0.1):
        pixels = self.GetPixels(image, pixelThreshold)
        angleDegrees = np.arange(-180, 181, 1)
        angleRad = angleDegrees * np.pi / 180
        ro = self.GetRos(pixels, angleRad)
        numHoughSins = self.CountHoughSins(ro, deviation)

        output = np.zeros(image.shape)
        for s in range (ro.shape[0]):
            for a in range (ro.shape[1]):
                if(numHoughSins[s, a] >= linesThreshold):
                    output = self.CreateLine(output, ro[s,a], angleRad[a])

        return output

    def CountHoughCircles(self, centers, deviation = 0.5):
        centersCount = [] # y = [0], x = [1], count = [2]
        for c in centers[:]:
            count = 0
            for cc in centers[:]:
                dif = c[0] - cc[0]
                if(dif > -deviation and dif < deviation):
                    dif = c[1] - cc[1]
                    if(dif > -deviation and dif < deviation):
                        count += 1
            centersCount.append([c[0], c[1], count])
        return centersCount

    def FilterCircleCenters(self, centersCount, threshold):
        filteredCenters = []
        for c in centersCount[:]:
            if(c[2] > threshold):
                filteredCenters.append([c[0], c[1]])
        #Erasing same centers
        #https://www.codespeedy.com/remove-duplicate-elements-from-a-tuple-in-python/
        b=set()
        centers=[element for element in filteredCenters
            if not (tuple(element) in b
                or  b.add(tuple(element)))]
        return centers

    def GetCircles(self, pixels, radius, threshold, deviation = 0.5):
        perimeter = 2 * np.pi * radius
        threshold = int(threshold * perimeter / 100)

        numPixels = pixels.shape[0]

        angleDegrees = np.arange(0, 361, 15)
        angleRad = angleDegrees * np.pi / 180

        #Calculate possible centers
        centers = [] #y = [0] x = [1]
        for p in range (numPixels):
            yi = pixels[p, 0]
            xi = pixels[p, 1]
            for a in range (angleRad.shape[0]):
                xc = (xi - (radius * np.cos(a)))
                yc = (yi + (radius * np.sin(a)))
                centers.append([yc, xc])
        """
        centersFound = []
        skipIndex = []
        for c in range (len(centers)):

            #Check if this index is of a reapeated coordenate
            skipF = False
            for skip in skipIndex[:]:
                if(skip == c):
                    skipF = True
            if(not(skipF)):
                #Count numbers of reapeated coordenate
                count = 0
                for cc in range(c + 1, len(centers)):
                    c1 = centers[c]
                    c2 = centers[cc]
                    dif = c1[0] - c2[0]
                    if(dif > -deviation and dif < deviation):
                        dif = c1[1] - c2[1]
                        if(dif > -deviation and dif < deviation):
                            skipIndex.append(cc)
                            count += 1

                #Adding to the list of centers found
                if(count >= threshold):
                    centersFound.append(centers[c])
        """
        centersCount = self.CountHoughCircles(centers,deviation)
        centersFound = self.FilterCircleCenters(centersCount, threshold)
        return centersFound

    def CreateCircles(self, image, centers):
        height = image.shape[0]
        width = image.shape[1]

        output = np.zeros((height, width))
        angleDegrees = np.arange(0, 361, 15)
        angleRad = angleDegrees * np.pi / 180

        #count = 0
        for c in centers[:]:
            yc = c[0]
            xc = c[1]
            r = c[2]
            for theta in angleRad[:]:
                x = int(xc + (r * np.cos(theta)))
                y = int(yc - (r * np.sin(theta)))
                if(x >= 0 and x < width):
                    if(y >= 0 and y < height):
                        #count += 1
                        output[y,x] = 255
        #print(count)
        return output

    def HoughCirclesTransform(self, image, circlesThreshold, radius, pixelThreshold = 255, deviation = 0.1):
        pixels = self.GetPixels(image, pixelThreshold)

        
        if(image.shape[0] >= image.shape[1]):
            imgRadius = image.shape[0] / 2
        else:
            imgRadius = image.shape[1] / 2
        minRadius = int(imgRadius * radius[0] / 100)
        maxRadius = int(imgRadius * radius[1] / 100)

        circleInfo = [] # y = [0], x = [1], radius = [2]
        for r in range(minRadius, maxRadius):
            listOfCenters = self.GetCircles(pixels, r, circlesThreshold, deviation)
            for centers in listOfCenters[:]:
                circleInfo.append([centers[0], centers[1], r])
    
        """
        circleInfo = [] # y = [0], x = [1], radius = [2]
        listOfCenters = self.GetCircles(pixels, r, circlesThreshold, deviation)
        for centers in listOfCenters[:]:
            circleInfo.append([centers[0], centers[1], r])  
        """
        output = self.CreateCircles(image, circleInfo)
        #Plot
        f,a = plt.subplots(ncols = 2, figsize = (20,5))
        a[0].imshow(image, cmap='gray')
        a[0].set_title('Image')
        a[1].imshow(output, cmap='gray')
        a[1].set_title('Circles')
        plt.show()
        return output

from PIL import Image
import cv2 
import numpy as np
from matplotlib import pyplot as plt 


def DisplayInOut(inImage, outImage, inIsGray = 0, outIsGray = 0):   
    if(inIsGray == 1):
        inImage = cv2.merge((inImage,inImage,inImage))
    else:
        inImage = cv2.cvtColor(inImage, cv2.COLOR_BGR2RGB)
    
    if(outIsGray == 1):
        outImage = cv2.merge((outImage,outImage,outImage))
    else:
        outImage = cv2.cvtColor(outImage, cv2.COLOR_BGR2RGB)
    f,a = plt.subplots(ncols = 2, figsize = (20,5))
    a[0].imshow(inImage.astype(int))
    a[0].set_title("Input")
    a[1].imshow(outImage.astype(int))
    a[1].set_title("Output")
    plt.plot()

def DisplayImg(inImage, inIsGray = 0,):   
    if(inIsGray == 1):
        inImage = cv2.merge((inImage,inImage,inImage))
    else:
        inImage = cv2.cvtColor(inImage, cv2.COLOR_BGR2RGB)
    plt.imshow(inImage.astype(int))
    plt.title("Image")
    plt.plot()

class FaceRecognizer():
    def __init__(self, image):
        self.image = image.copy()
        self.proportion = [1,1]
        self.lastImage = self.image.copy()

    def DisplayImage(self):
        DisplayImg(self.lastImage)


if __name__ == '__main__':
    pass
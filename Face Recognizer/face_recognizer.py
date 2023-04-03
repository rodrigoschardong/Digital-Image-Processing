"""
    python -m pip install --user opencv-contrib-python
"""

from PIL import Image
import cv2 
import numpy as np
from matplotlib import pyplot as plt 
import os
#import imageio.mimread
import urllib.request



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

class ImageBank():
    def __init__(self, paths):
        self.len = len(paths)
        self.imagesPaths = paths
        self.ids = []
        self.subjects = []
        id = 0
        for path in paths:
            subject = os.path.split(path)[1].split('.')[0]
            index = int(subject.replace('subject', ''))
            self.ids.append(index)
            self.subjects.append(subject)
        #print(self.subjects)
        #print(self.ids)

    def GetImages(self):
        images = []
        for path in self.imagesPaths:
            #img = cv2.imread(path, 0)
            img = Image.open(path).convert('L')
            
            images.append(np.array(img, 'uint8'))

        #print(images[0])
        #cv2.imwrite("hey.png", images[0])
        return np.array(images)

class FaceRecognizer():
    def __init__(self, classifierPath):

        self.classifierPath = classifierPath
        self.proportion = [1,1]
        if(not(os.path.exists(classifierPath))):
            os.mkdir(classifierPath)

    def Train(self, trainPaths):
        imgBank = ImageBank(trainPaths)
        ids = np.array(imgBank.ids)
        images = imgBank.GetImages()
        lbph_classifier = cv2.face.LBPHFaceRecognizer_create()
        
        lbph_classifier.train(images, ids)
        lbph_classifier.write(self.classifierPath + 'lbph_classifer.yml')

    def DisplayImage(self):
        DisplayImg(self.lastImage)


def get_images_paths(path):
    paths = [(path+ '/' + f) for f in os.listdir(path)]
    #paths = os.listdir(path)
    #print(paths)
    return paths



if __name__ == '__main__':
    print("Face Recognizer init")
    trainPath = "./images/train"
    testPath = "./images/test"
    classifierPath = "./classifiers"

    faceRec = FaceRecognizer(classifierPath)

    #paths = get_images_paths(trainPath)
    faceRec.Train(get_images_paths(trainPath))
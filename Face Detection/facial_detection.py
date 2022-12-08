import cv2
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

class FaceDetection():
    def __init__(self, imagePath, cascadePath):
        self.image = cv2.imread(imagePath)
        self.faceDetector = cv2.CascadeClassifier(cascadePath)
        self.lastImage = self.image.copy()

    def DisplayImage(self):
        DisplayImg(self.lastImage)

    def ResizeImage(self, height, width):
        self.resizedImage = cv2.resize(self.image, (width, height))
        self.last = self.resizedImage.copy()
    
    def FaceDetect(self):
        self.detections = self.faceDetector.detectMultiScale(cv2.cvtColor(self.last, cv2.COLOR_BGR2GRAY))
        self.imageWithFacesDetected = self.last.copy()
        for x, y, w, h in self.detections:
            #print(x, y, w, h)
            cv2.rectangle(self.imageWithFacesDetected, (x, y), (x + w, y + h), (0,255,0), 2)
        self.lastImage = self.imageWithFacesDetected.copy()

if __name__ == '__main__':
    image = cv2.imread("./test.jpg")
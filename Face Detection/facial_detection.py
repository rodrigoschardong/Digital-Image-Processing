import cv2
import dlib
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
    def __init__(self, imagePath):
        self.image = cv2.imread(imagePath)
        self.proportion = [1,1]
        self.lastImage = self.image.copy()

    def DisplayImage(self):
        DisplayImg(self.lastImage)

    def ResizeImage(self, height, width):
        shape = self.image.shape
        
        self.proportion = [shape[0] / height, shape[1] / width]
        resizedImage = cv2.resize(self.image, (width, height))
        self.lastImage = resizedImage.copy()
        #print(self.last.shape)
    
    def FaceDetectHaarscade(self, cascadePath, scaleFactor = 1.1, minNeighbors = 1, minSize = 50, maxSize = 700):     
        faceDetector = cv2.CascadeClassifier(cascadePath)
        detections = faceDetector.detectMultiScale(cv2.cvtColor(self.lastImage, cv2.COLOR_BGR2GRAY), scaleFactor = scaleFactor, minNeighbors = minNeighbors, minSize = (minSize, minSize), maxSize = (maxSize, maxSize))
        imageWithFacesDetected = self.lastImage.copy()
        for x, y, w, h in detections:
            #print(x, y, w, h)
            cv2.rectangle(imageWithFacesDetected, (x, y), (x + w, y + h), (0,255,0), 2)
        self.lastImage = imageWithFacesDetected.copy()

    def FaceDetectHOG(self, scale = 1):
        detector = dlib.get_frontal_face_detector()
        detected = detector(self.lastImage, scale)
        imageWithFacesDetected = self.lastImage.copy()
        for face in detected:
             cv2.rectangle(imageWithFacesDetected, (face.left(), face.top()), (face.right(), face.bottom()), (0,255,0), 2)
        self.lastImage = imageWithFacesDetected.copy()

    def FaceDetectCNN(self, weightPath, scale, confidence):
        detector = dlib.cnn_face_detection_model_v1(weightPath)
        detected = detector(self.lastImage, scale)
        imageWithFacesDetected = self.lastImage.copy()
        for face in detected:
            if(face.confidence > confidence):
                cv2.rectangle(imageWithFacesDetected, (face.rect.left(), face.rect.top()), (face.rect.right(), face.rect.bottom()), (0,255,0), 2)
        self.lastImage = imageWithFacesDetected.copy()

if __name__ == '__main__':
    image = cv2.imread("./images/test.jpg")
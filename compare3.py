#Sources:
'''
The threshold functions and the readImage functions have been adapted from Vasu Agrawal's lecture on Image Processing using OpenCV

'''


import ImageChops
import math, operator
from PIL import Image
import cv2
from cv2 import cv
import numpy as np
import os

def resizeImage(path,(pixelRows,pixelCols)=(50,50)):    
    return cv2.resize(path,(pixelRows,pixelCols))

def rmsdiff(im1, im2):
    "Calculate the root-mean-square difference between two images"

    h = ImageChops.difference(im1, im2).histogram()

    # calculate rms
    return math.sqrt(reduce(operator.add,
        map(lambda h, i: h*(i**2), h, range(256))
    ) / (float(im1.size[0]) * im1.size[1]))

def thresholdImage(image):
    image=cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    threshed = cv2.adaptiveThreshold(image,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C,cv2.THRESH_BINARY,15,5)
    #(threshVal,threshed)=cv2.threshold(image,100,255,cv2.THRESH_BINARY)
    return threshed


def numpy_to_PIL(original_image):
    return Image.fromarray(original_image.astype(np.uint8))

def checkStandardDeviation(letterSum,notInclude):
    mean=0
    veryDiff=True    
    for key in letterSum:
        if key!=notInclude and abs(letterSum[key]-letterSum[notInclude])<=10:
            veryDiff=False
    for key in letterSum:
        if key!=notInclude:
            mean+=letterSum[key]
    mean/=(len(letterSum)-1)
    diffsq=0
    for key in letterSum:
        if key!=notInclude:
            diffsq+=(letterSum[key]-mean)**2
    diffsq=(diffsq/len(letterSum))**0.5        
    return diffsq,abs(letterSum[notInclude]-mean),veryDiff

def compareA(letter):
    letterSum=dict()
    
    for imageFile in os.listdir("letterset"):
        im1=thresholdImage(resizeImage(letter))
        im2=thresholdImage(resizeImage(cv2.imread("letterset"+os.sep+imageFile)))
        im1=numpy_to_PIL(im1)
        im2=numpy_to_PIL(im2)
        curSum=rmsdiff(im2,im1)
        curLetter=imageFile[0]
        if curLetter in letterSum:
            letterSum[curLetter]+=curSum
        else:
            letterSum[curLetter]=curSum
        
    minValue=None
    bestLetter=None
    for key in letterSum:
        letterSum[key]/=5
        if letterSum[key]<minValue or minValue==None:
            minValue=letterSum[key]
            bestLetter=key
        
    sd,diff,isVeryDiff=checkStandardDeviation(letterSum,bestLetter)
    print bestLetter,letterSum,(sd,diff)
    if bestLetter:#VeryDiff :#and diff>=15:
        print "goes in"
        return bestLetter
    else:
        return ""
    print letterSum
        

def removeExtraBoundingBoxes(rectList):
    newList=[]
    print "in here"
    for x,y,w,h in rectList:
        if (w*h>100 and w*h<80000):
            newList.append((x,y,w,h))
    seenList=[newList[0]]
    j=0
    print "start"
    for i in range(1,len(newList)):
        print (newList[i],seenList)
        x1,y1,w1,h1=newList[i]
        x,y,w,h=seenList[len(seenList)-1]
        if((x<=x1 and x1<=(x+w) and y<=y1 and y1<=(y+h))):
            j+=1
            print ("not appending")
        else:
            seenList.append((x1,y1,w1,h1))
            print "appending"
        
    print "outta here",j    
    return seenList
                
def findBoundingBoxes():
    image=(resizeImage(cv2.imread("B3.jpg"),(300,300)))
    thresh=thresholdImage(image)
    contours, hierarchy = cv2.findContours(thresh,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
    contours.pop(0)
    i=0
    resultString=""
    rectList=[]
    for cnt in contours:                          
             x,y,w,h = cv2.boundingRect(cnt)
             rectList.append((x,y,w,h))
    
    rectList=sorted(rectList,key=lambda x:(x[0],x[1]))#organised by order  
    rectList=removeExtraBoundingBoxes(rectList)

    for rect in rectList:
             x,y,w,h=rect         
             cv2.rectangle(image,(x,y),(x+w,y+h),(0,255,0),2)
             letter = image[y:y+h,x:x+w]
             cv2.imshow(str(i),resizeImage(thresholdImage(letter)))
             


             
             print (i,w*h)
             i+=1
             result=compareA(letter)
             resultString+=result

    print resultString
    cv2.drawContours(thresh,contours,-1,(0,0,255),3)
    cv2.imshow("image2",image)
                 
        
findBoundingBoxes()
print "Done!"    
    
cv2.waitKey()
cv2.destroyAllWindows()



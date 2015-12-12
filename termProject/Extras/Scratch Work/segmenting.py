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

def resizeImage(path,(pixelRows,pixelCols)=(300,300)):    
    return cv2.resize(path,(pixelRows,pixelCols))


def thresholdImage(image):
    image=cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    threshed = cv2.adaptiveThreshold(image,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C,cv2.THRESH_BINARY,15,5)
    #(threshVal,threshed)=cv2.threshold(image,100,255,cv2.THRESH_BINARY)
    return threshed


def numpy_to_PIL(original_image):
    return Image.fromarray(original_image.astype(np.uint8))


def removeExtraBoundingBoxes(rectList):
    newList=[]
    print "in here"
    for x,y,w,h in rectList:
        if (w*h>100 and w*h<=80000):
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
def checkLetter(ratioList):
    letterRatios={"A":[0.0784,0.0913777777778,0.163555555556,0.165688888889,0.175288888889,0.165866666667,
                       0.134755555556,0.0784,0.1568,0.200533333333,0.102222222222,0.0784,0.0784,0.0785777777778,0.155555555556,0.170488888889],
                  "C":[0.0864,0.153422222222,0.164088888889,0.159111111111,0.127822222222,0.0784,0.0784,0.151644444444,0.125688888889,0.0784,
                       0.0784,0.148088888889,0.0976,0.0784,0.0784,0.145244444444]
                  }
    diffCounts={ letter:0 for letter in letterRatios}
    for letter in letterRatios:
        for i in range(len(ratioList)):
            if not((letterRatios[letter][i]>=0.1 and ratioList[i]>=0.1) or (letterRatios[letter][i]<0.1 and ratioList[i]<0.1)):
                if letter in diffCounts:
                    diffCounts[letter]+=1
                else:
                    diffCounts[letter]=1
    minCount=None
    bestMatch=None
    for letter in diffCounts:
        curCount=diffCounts[letter]
        if minCount==None or minCount>=curCount:
            bestMatch=letter
            minCount=curCount

    print diffCounts
    return bestMatch
        
                
            
        
def segmentImage(imarray):
    height=imarray.shape[0]
    width=imarray.shape[1]
    totalSegPixels=height*width/16.0
    k=0
    ratioList=[]
    print (height*width)
    for i in range(4):
        for j in range(4):
            x=i*width/4
            y=j*height/4
            newH=height/4
            newW=width/4
            cv2.rectangle(imarray,(x,y),(x+newW,y+newH),(0,255,0),2)
            segment=imarray[y:y+newH,x:x+newW]
            cv2.imshow("segment"+str(k),segment)
            blackPixels=int(totalSegPixels)-int(cv2.countNonZero(segment))
            ratio=blackPixels*1.0/totalSegPixels*1.0
            print (cv2.countNonZero(segment))
            print (str(k)+" has "+str(ratio))
            ratioList.append(ratio)
            k+=1

    letter=checkLetter(ratioList)
    print letter
    print "All segments done" 
def findBoundingBoxes():
    height=300
    width=300
    image=(resizeImage(cv2.imread("test1.jpg"),(width,height)))
    thresh=thresholdImage(image)
    contours, hierarchy = cv2.findContours(thresh,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)

    i=0
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
             cv2.waitKey()
             print letter
             letter=resizeImage(thresholdImage(letter))             
             segmentImage(letter)
             

    cv2.drawContours(thresh,contours,-1,(0,0,255),3)
    cv2.imshow("image2",image)
                 
        
findBoundingBoxes()
print "Done!"    
    
cv2.waitKey()
cv2.destroyAllWindows()

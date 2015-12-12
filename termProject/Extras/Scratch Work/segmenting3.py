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


def removeExtraBoundingBoxes(rectList):
    newList=[]
    
    for x,y,w,h in rectList:
        if (w*h>100 and w*h<=80000 and w<290 and h<290):
            newList.append((x,y,w,h))
    
    seenList=[newList[0]]
    j=0
    
    for i in range(1,len(newList)):
        print (newList[i],seenList)
        x1,y1,w1,h1=newList[i]
        x,y,w,h=seenList[len(seenList)-1]
        if((x<=x1 and x1<=(x+w) and y<=y1 and y1<=(y+h))):
            j+=1
            
        else:
            seenList.append((x1,y1,w1,h1))
            
        
        
    return seenList

def resolveTies(bestMatch,ratioList,compareValues):
    
    valuesToCheck={letter:0 for letter in bestMatch}
    for i in range(len(ratioList)):
        for checkLetter in bestMatch:
            valuesToCheck[checkLetter]+=abs(ratioList[i]-compareValues[checkLetter][i])
    minCount=None
    matched=None
    for letter in valuesToCheck:
        curCount=valuesToCheck[letter]
        if minCount==None or minCount>=curCount:
            matched=letter
            minCount=curCount
    return matched
            
            
        
        
    
def checkLetter(ratioList):
    #this dats has been used by getting the average of the non-zero pixel percentages of atleast 5 test images per letter in order to obtain an "ideal letter"
    
    letterRatios={"A":[0.0784,0.0913777777778,0.163555555556,0.165688888889,0.175288888889,0.165866666667,
                       0.134755555556,0.0784,0.1568,0.200533333333,0.102222222222,0.0784,0.0784,0.0785777777778,0.155555555556,0.170488888889],
                  "B":[0.194844444444,0.207466666667,0.201777777778,0.234666666667,0.142044444444,0.173511111111,0.0784,0.145777777778,0.169244444444,
                       0.2544,0.0784,0.151288888889,0.1328,0.114488888889,0.213511111111,0.178488888889],
                  "C":[0.0864,0.153422222222,0.164088888889,0.159111111111,0.127822222222,0.0784,0.0784,0.151644444444,0.125688888889,0.0784,
                       0.0784,0.148088888889,0.0976,0.0784,0.0784,0.145244444444],
                  "D":[0.245866666667,0.210844444444,0.203733333333,0.219377777778,0.139022222222,0.0784,0.0785777777778,0.160888888889,0.161422222222,
                       0.0784,0.0812444444444,0.171022222222,0.148444444444,0.219377777778,0.224,0.0784],
                  "E":[0.211022222222,0.1696,0.201244444444,0.204266666667,0.143466666667,0.0784,0.120177777778,0.145422222222,0.143466666667,
                       0.0784,0.115911111111,0.146666666667,0.118577777778,0.0784,0.088,0.147911111111],
                  "F":[0.225955555556,0.228622222222,0.180444444444,0.1856,0.130488888889,0.136355555556,0.0784,0.0784,0.1296,0.1392,0.0784,0.0784,0.127644444444,
                       0.135466666667,0.0784,0.0784],
                  "G": [0.1024,0.1568,0.152,0.112533333333,0.139377777778,0.0784,0.0784,0.126222222222,0.131555555556,0.0784,0.0784,
                        0.118933333333,0.125333333333,0.0867555555556,0.224711111111,0.190755555556],
                  "H":[0.168177777778,0.218488888889,0.158577777778,0.181688888889,0.0912,0.118577777778, 0.0784,0.0954666666667,0.0912,
                       0.0826666666667,0.0961777777778,0.0961777777778,0.171377777778,0.155377777778,0.193066666667,0.168533333333],
                  "I":[0.136355555556,0.105066666667,0.108977777778,0.147022222222,0.187555555556,0.131911111111,0.102577777778,0.130311111111,0.133155555556,
                       0.0784,0.0784,0.130488888889,0.130844444444,0.106488888889,0.111466666667,0.1408],
                  "J":[0.106311111111,0.0912,0.0935111111111,0.149333333333,0.134222222222,0.0784,0.0784,0.1264,0.193066666667,0.1488,0.133866666667,0.133333333333,
                       0.121777777778,0.0784,0.0784,0.0784],
                  "K":[0.1824,0.233066666667,0.1664,0.176888888889,0.0912,0.138133333333,0.146666666667,0.0784,0.149511111111,0.0794666666667,0.144177777778,0.0785777777778,
                       0.129955555556,0.0784,0.0784,0.153066666667],
                  "L":[0.16,0.178133333333,0.169422222222,0.178488888889,0.0912,0.0784,0.0784,0.125333333333,0.0912,0.0784,0.0784,0.134222222222,0.0908444444444,
                       0.0784,0.0784,0.138311111111],
                  "M":[0.228977777778,0.147733333333,0.152533333333,0.142755555556,0.0915555555556,0.155377777778,0.0954666666667,0.0784,0.0912,0.144177777778,
                       0.0993777777778,0.0784,0.206577777778,0.143111111111,0.1408,0.149155555556],
                  "N":[0.191822222222,0.153422222222,0.156088888889,0.146488888889,0.0784,0.148266666667,0.103644444444,0.0784,0.0784,0.0784,0.1296,
                       0.113066666667,0.164444444444,0.159466666667,0.161244444444,0.193422222222],
                  "O":[0.109688888889,0.154666666667,0.138666666667,0.153422222222,0.1408,0.0784,0.0784,0.1312,0.137955555556,0.0784,0.0784,0.129955555556,
                       0.145244444444,0.128177777778,0.1392,0.0981333333333],
                  "P":[0.226488888889,0.229333333333,0.236977777778,0.193422222222,0.125688888889,0.0784,0.129244444444,0.0856888888889,0.142577777778,
                       0.0979555555556,0.112355555556,0.0784,0.182577777778,0.2128,0.0784,0.0784],
                  "Q":[0.135111111111,0.134755555556,0.139377777778,0.0912,0.175466666667,0.118933333333,0.0784,0.104888888889,0.137422222222,0.0942222222222,
                       0.139911111111,0.115911111111,0.106311111111,0.119466666667,0.1296,0.144533333333],
                  "R":[0.193777777778,0.210311111111,0.185244444444,0.181866666667,0.122133333333,0.141333333333,0.124977777778,0.0784,0.141866666667,0.122488888889,
                       0.114488888889,0.0954666666667,0.0784,0.0784,0.0784,0.1344],
                  "S":[0.129955555556,0.167111111111,0.0901333333333,0.136177777778,0.131022222222,0.121066666667,0.0848,0.133333333333,0.127111111111,
                       0.0952888888889,0.0979555555556,0.119288888889,0.129066666667,0.0784,0.166044444444,0.1312],
                  "T":[0.164622222222,0.0912,0.0912,0.0908444444444,0.154311111111,0.0784,0.0784,0.0784,0.217244444444,0.172622222222,0.171377777778,
                       0.117866666667,0.145244444444,0.0784,0.0784,0.0951111111111],
                  "U":[0.171555555556,0.164444444444,0.151822222222,0.119644444444,0.0784,0.0784,0.0784,0.1344,0.0784,0.0784,0.0784,0.1376,0.127466666667,
                       0.137066666667,0.143288888889,0.141511111111],
                  "V":[0.163377777778,0.158577777778,0.122844444444,0.0784,0.0912,0.0784,0.0990222222222,0.195555555556,0.0912,0.0862222222222,0.145244444444,
                       0.0999111111111,0.141866666667,0.115022222222,0.0784,0.0784],
                  "W":[0.130666666667,0.131911111111,0.126755555556,0.150933333333,0.0784,0.131377777778,0.121422222222,0.0896,0.0784,0.0871111111111,
                       0.132266666667,0.128533333333,0.122844444444,0.121244444444,0.122133333333,0.096],
                  "X":[0.127288888889,0.0784,0.0787555555556,0.198222222222,0.115022222222,0.133155555556,0.197866666667,0.0784,0.0808888888889,0.212266666667,
                       0.139911111111,0.0784,0.173333333333,0.0784,0.105244444444,0.141333333333],
                  "Y":[0.208888888889,0.100444444444,0.102933333333,0.154666666667,0.108977777778,0.1552,0.1584,0.1312,0.0922666666667,
                       0.202844444444,0.0878222222222,0.124622222222,0.171555555556,0.0904888888889,0.0906666666667,0.119822222222],
                  "Z":[0.0869333333333,0.0876444444444,0.113244444444,0.234311111111,0.141511111111,0.115733333333,0.127288888889,0.141155555556,
                       0.181511111111,0.121066666667,0.0784,0.135111111111,0.115022222222,0.0823111111111,0.0894222222222,0.149866666667]                 
                  
                  }
    
    diffCounts={ letter:0 for letter in letterRatios}
    for letter in letterRatios:
        for i in range(len(ratioList)):
            if not((letterRatios[letter][i]>=0.1 and ratioList[i]>=0.1) or (letterRatios[letter][i]<0.1 and ratioList[i]<0.1)):
                if letter in diffCounts:
                    diffCounts[letter]+=1
                else:
                    diffCounts[letter]=1
            if ratioList[i]>=0.5:
                diffCounts=dict()
                break
            
    minCount=None
    bestMatch=[""]
    for letter in diffCounts:
        curCount=diffCounts[letter]
        if minCount==None or minCount>curCount:
            bestMatch=[letter]
            minCount=curCount
        elif minCount==curCount:
            bestMatch.append(letter)
    if len(bestMatch)==1:
        bestMatch=bestMatch[0]
    else:
        valToBeCompared=dict()
        for tie in bestMatch:
            valToBeCompared[tie]=letterRatios[tie]            
        bestMatch=resolveTies(bestMatch,ratioList,valToBeCompared)

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
            
##            try :
##                cv2.rectangle(imarray,(x+20,y+20),(x+newW-20,y+newH-20),(0,255,0),2)
##                segment=imarray[y+20:y+newH-20,x+20:x+newW-20]
##                segment=resizeImage(segment,(300/4,300/4))
##                cv2.imshow("segment"+str(k),segment)
##                totalSegPixels=(segment.shape[0]*segment.shape[1])
##                print "adding 10 pixel"
##            except:
            
            if True:
                cv2.rectangle(imarray,(x,y),(x+newW,y+newH),(0,255,0),2)
                segment=imarray[y:y+newH,x:x+newW]
                cv2.imshow("segment"+str(k),segment)
                print "Nope"
                
            
            blackPixels=abs(int(totalSegPixels)-int(cv2.countNonZero(segment)))
            ratio=blackPixels*1.0/totalSegPixels*1.0
            print (cv2.countNonZero(segment))
            print (str(k)+" has "+str(ratio))
            ratioList.append(ratio)
            k+=1

    letter=checkLetter(ratioList)
    print letter
    print "All segments done"
    return letter

def findBoundingBoxes(imagePath):
    height=300
    width=300
    image=(resizeImage(cv2.imread(imagePath),(width,height)))
    thresh=thresholdImage(image)
    contours, hierarchy = cv2.findContours(thresh,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)

    i=0
    rectList=[]
    
    for cnt in contours:                          
             x,y,w,h = cv2.boundingRect(cnt)
             rectList.append((x,y,w,h))
    
    rectList=sorted(rectList,key=lambda x:(x[0],x[1]))#organised by order
    
    rectList=removeExtraBoundingBoxes(rectList)
    result=""
    
    for rect in rectList:
             x,y,w,h=rect         
             cv2.rectangle(image,(x,y),(x+w,y+h),(0,255,0),2)
             letter = image[y:y+h,x:x+w]
             cv2.imshow(str(i),resizeImage(thresholdImage(letter)))
             cv2.waitKey()
             print letter
             letter=resizeImage(thresholdImage(letter))             
             addToString=segmentImage(letter)
             result+=addToString
             

    cv2.drawContours(thresh,contours,-1,(0,0,255),3)
    cv2.imshow("image2",image)
                 
    print result
    return result

#findBoundingBoxes("test1.jpg")
print "Done!"    
    
cv2.waitKey()
cv2.destroyAllWindows()

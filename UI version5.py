'''
SOURCES:
1. Taking a Photo: http://stackoverflow.com/questions/19448644/save-image-when-pressing-a-key-python-opencv
2. Using the pytesser and pyttsx modules have been adapted from the official documentaton for these modules
and also the following stackoverflow posts:
http://stackoverflow.com/questions/32499491/python-text-to-speech-using-pyttsx
3. the Animation framework is from the 112 Course Notes
'''

from Tkinter import *
root=""
#Image Libraries
import cv
import cv2
import Image
#Numbers
import numpy as np
#Speech to text Library
import pyttsx
#Image to text module
from pytesser import*
from segmenting3 import *
#this is a personal python file, mke sure it is in the same folder as this file
#Modules for system
import sys

def getInputImage(data):
    
    timeCount=200
    cv.NamedWindow("Input Image", cv.CV_WINDOW_AUTOSIZE)
    camera_index = 0
    capture = cv.CaptureFromCAM(camera_index)   

    def repeat():
     frame = cv.QueryFrame(capture)
     cv.ShowImage("Input Image", frame)
     c = cv.WaitKey(25)
     
     if (c == 32): #32 checks for ascii space
      data.picNum+=1
      cv.SaveImage("input"+str(data.picNum)+".jpg",frame)
      data.mode.takeImage=False #initialisng start values for next use
      data.mode.count=70
      cv2.destroyAllWindows()
    
      
    while data.mode.takeImage==True:
        timeCount+=1
        if timeCount>=200:
            timeCount=0
             #instructions for using camera
            sayText("press space to take a picture")
        repeat()

        
def detectPrintedText(imagePath):
#the imagePath is the image name
#it must be stored in the same folder as the .py file  
    image = Image.open(imagePath)
    text= image_to_string(image)
    return text

def sayText(text):
##    engine = pyttsx.init()
##    engine.setProperty('rate', 150)
##    engine.say("lala")
##    engine.runAndWait()
    try:        
        engine = pyttsx.init()
        engine.setProperty('rate', 150)
        engine.say(text)
        engine.runAndWait()
    except:
        engine = pyttsx.init()
        engine.setProperty('rate', 150)
        engine.say("The image contains garbage text. Please upload another image.")
        engine.runAndWait()

def saveAs(data):
    import sys, time, string, win32com.client, stat, os

    class CWordAutomate:
        """Encapsulates a winword com connection"""
        def __init__( self ):
            """construct: create OLE connection to winword"""
            self.m_obWord         = win32com.client.Dispatch( "Word.Application" )
            self.m_obDoc          = self.m_obWord.Documents.Add( ) # create new doc
            self.m_obWord.Visible = 1
            self.m_Sel            = self.m_obWord.Selection # get a selection

        def WriteLine( self, sTxt, sFont, lSize, bBold=0 ):
            """Write a line to winword"""
            self.m_Sel.Font.Name = sFont
            self.m_Sel.Font.Bold = bBold
            self.m_Sel.Font.Size = lSize
            self.m_Sel.TypeText( Text=sTxt + "\n"  )

        def Save(self, sFilename):
            self.m_obDoc.SaveAs(sFilename)

        def Quit(self):
            self.m_obWord.Quit()


    def file_test(file):
        """
        Tests user supplied file to see if it exists and contains data.
        If the input file does not exist or is empty, return a warning code
        """

        if (0 == os.path.isfile(file) or (0 == os.stat(file)[stat.ST_SIZE])):
            return 1
        else:
            return 0


    if __name__ == "__main__":

	
	#sFileName  = sys.argv[1]
	#obFile     = file( sFileName, 'r+' )
        sContent   = str(data.detectedText)
	#obFile.read()
	#obFile.close()
        lstContent = sContent.splitlines()
	
	# 
	# Write contents of source file to user supplied file name
	#
        obWord = CWordAutomate()
	
        for sLine in lstContent:
            obWord.WriteLine( sLine, "Swell Braille", 14  )
	
        sLastMsg = time.strftime( "document generated on %c", time.localtime()  )
        obWord.WriteLine( sLastMsg, "Times New Roman", 14, 0 )
	
        obWord.Save("output"+str(data.picNum)+".docx")
        obWord.Quit()
    sayText("the text has been saved in the Documents folder as output"+str(data.picNum)+" dot doc x.")

def convertTextToSpeakable(text):
    speakable=""
    for char in text:
        if ord(char)<128: #removes all non ASCII characters
            speakable+=char
    return speakable

def leaveApplication():
    global root
    root.destroy()
    sys.exit()
    raise SystemExit

def rgbString(red, green, blue):
    return "#%02x%02x%02x" % (red, green, blue)

class theme1(object): #defines custom colors for UI
    def __init__(self):
        self.option1=rgbString(153,255,51)
        self.option2=rgbString(255,0,127)
        self.option3=rgbString(51,51,255)
theme=theme1()

class Mode(object):
    #base class that other classes are modelled on
    def __init__(self):
        pass
    def drawMode(self,canvas,data):
        pass
    def keyPressed(self,event,data):
        pass
    def mousePressed(self,event,data):
        pass
    def modeTimerFired(self,data):
        pass
    
class startMode(Mode): #the camera mode

    def __init__(self):
        self.label="start"
        self.takeImage=True
        self.count=60

    def drawMode(self,canvas,data):
        canvas.create_rectangle(0,0,data.width,data.height,fill=theme.option1)
        canvas.create_text(data.width//2,data.height//2,text="Press SPACE to switch on the webcam.", font="16")
        
    def keyPressed(self,event,data):
        if event.keysym=="space":
            getInputImage(data)
            self.takeImage=True #needs to be reset because out of loop
            self.count=60 #reinitialising
            data.mode=gettype

    def modeTimerFired(self,data):
        self.count+=1
        if self.count>=70:
            self.count=0
            sayText("press space to switch on the webcam")
        #saying initial message to start camera.

class getInputTypeMode(Mode):
    
    def __init__(self):
        
        self.timeCount=90
        
    def drawMode(self,canvas,data):
        canvas.create_rectangle(0,0,data.width,data.height,fill=theme.option1)
        message='''Press the LEFT ARROW Key for Printed Text. \n \nPress the RIGHT ARROW Key for Handwritten Text'''
        canvas.create_text(data.width//2,data.height//4,text=message, font="14")
        
    def modeTimerFired(self,data):
        self.timeCount+=1 #incrementing timer to repeat instructions
        if self.timeCount>=100:
            self.timeCount=0
            sayText("""Press the left arrow key to process Printed Text.
                    press the right arrow key to process handwritten text.""")            
            
    def keyPressed(self,event,data):
        self.timerFired=90 # reintialising time count to repeat instructions 
        if event.keysym=='Left':
            data.mode=printed
            sayText("Processing Printed Text")
        elif event.keysym=='Right':
            sayText("processing handwritten text")
            data.mode=handwritten
            
class TranslatePrinted(Mode):
    
        
    def drawMode(self,canvas,data):
        canvas.create_rectangle(0,0,data.width,data.height,fill=theme.option1)        
        canvas.create_text(data.width//2,data.height//2,text="Translating Printed Text", font="16")
        
    def modeTimerFired(self,data):
        sayText("Obtaining Text from Image")
        self.translate(data)
        
    def emptyStringError(self):
        #speak instructions to click another image on keyPressed
        sayText("The image does not contain text. Please upload another image. Switching to camera mode.")

    def translate(self,data):
        firstPath="C:\\Users\\Naviya\\Desktop\\112 Term Project Stuff\\" #+last picture taken
        data.detectedText=detectPrintedText(firstPath+"input"+str(data.picNum)+".jpg")
        if data.detectedText==None or data.detectedText.isspace():
            self.emptyStringError()
            data.mode=start
        else:
            #change to output mode type
            data.detectedText=convertTextToSpeakable(data.detectedText)
            print data.detectedText
            data.mode=getoutputtype

class TranslateHandwritten(Mode):
    
        
    def drawMode(self,canvas,data):
        canvas.create_rectangle(0,0,data.width,data.height,fill=theme.option2)        
        canvas.create_text(data.width//2,data.height//2,text="Translating Handwritten Text", font="16")
        
    def modeTimerFired(self,data):
        sayText("Obtaining Text from Image")
        self.translate(data)
        
    def emptyStringError(self):
        #speak instructions to click another image on keyPressed
        sayText("The image does not contain text. Please upload another image. Switching to camera mode.")

    def translate(self,data):
        firstPath="C:\\Users\\Naviya\\Desktop\\112 Term Project Stuff\\" #+last picture taken
        data.detectedText=findBoundingBoxes(firstPath+"input"+str(data.picNum)+".jpg")
        if data.detectedText==None or data.detectedText.isspace():
            self.emptyStringError()
            data.mode=start
        else:
            #change to output mode type
            data.detectedText=convertTextToSpeakable(data.detectedText)
            print data.detectedText
            data.mode=getoutputtype


class chooseOutput(Mode):
    
    def __init__(self):
        self.count=90
        
    def drawMode(self,canvas,data):
        message="Press the LEFT ARROW key to say the text out loud. \n\nPress the RIGHT ARROW key to save the text as Braille."
        canvas.create_rectangle(0,0,data.width,data.height,fill=theme.option2)
        canvas.create_text(data.width//2,data.height//4,text=message,font='16')
        
    def keyPressed(self,event,data):
        self.count=90
        if event.keysym=="Left":
            print "Speak Screen"
            sayText("the obtained text is"+data.detectedText)
            data.mode=audio
        elif event.keysym=="Right":
            #speak confirmation message
            #start processing
            #change mode
            print "Braille"
            saveAs(data)
            print "Saved"
            data.mode=audio
        
    def modeTimerFired(self,data):
        self.count+=1
        if self.count>=100:
            self.count=0
            sayText("Press the LEFT ARROW key to say the text out loud. Press the RIGHT ARROW key to save the text as Braille.")

class Audio(Mode):
    def __init__(self):
        self.count=90

    def drawMode(self,canvas,data):
        message="Press the LEFT ARROW key to repeat the audio.\n\nPress the RIGHT ARROW key to save the text as Braille. \n\nPress the DOWN ARROW key to quit application."
        canvas.create_rectangle(0,0,data.width,data.height,fill="green")
        canvas.create_text(data.width//2,data.height//4,text=message,font="16")
        
    def modeTimerFired(self,data):
        message="Press the LEFT ARROW key to repeat the audio. Press the RIGHT ARROW key to save the text as Braille. Press the DOWN ARROW key to quit application."
        self.count+=1
        if self.count>=100:
            self.count=0
            sayText(message)
            
    def keyPressed(self,event,data):
        self.count=90 #reinitialising instruction counter
        if event.keysym=="Left":
            sayText(str(data.detectedText))
            data.mode=audio
            
        elif event.keysym=="Right":
            sayText("Saving the text.")
            saveAs(data)
            data.mode=audio
            
        elif event.keysym=="Down":
            data.mode=lastmenu
            #third menu-take another picture or quit 
        
class lastMenu(Mode):
    
    def __init__(self):
        self.count=90
        
    def drawMode(self,canvas,data):
        
        message="Press the LEFT ARROW key to Quit Application.\n\nPress the RIGHT ARROW key to take another image."        
        canvas.create_rectangle(0,0,data.width,data.height,fill=theme.option1)
        canvas.create_text(data.width//2,data.height//4,text=message,font="16")
        
    def modeTimerFired(self,data):
        message="Are you sure you wish to quit the application? Press the LEFT ARROW key to Quit Application. Press the RIGHT ARROW key to take another image."
        self.count+=1
        if self.count>=100:
            self.count=0
            sayText(message)

    def keyPressed(self,event,data):
        self.count=90 #reinit to speak instructions
        if event.keysym=="Left":
            sayText("Quitting Application.")
            leaveApplication()
        elif event.keysym=="Right":
            data.mode=start

class Blank(Mode):
    def __init__(self):
        self.label="blank"
        self.count=0
    def drawMode(self,canvas,data):
        canvas.create_text(data.width//2,data.height//2,text="Under construction")
    def modeTimerFired(self,data):
        #do nothing
        print "inBlankTImerFired"
        self.count+=1      
        
            
        
start=startMode()
gettype=getInputTypeMode()
printed=TranslatePrinted()
blank=Blank()
getoutputtype=chooseOutput()
audio=Audio()
lastmenu=lastMenu()
handwritten=TranslateHandwritten()

####################################
# Central Control
####################################

def init(data):
    data.mode=start
    data.picNum=0
    data.detectedText=""


def mousePressed(event, data):
    data.mode.mousePressed(event,data)
    
def keyPressed(event, data):
    if event.keysym=="r":
        data.mode=start
    data.mode.keyPressed(event,data)
    

def timerFired(data):
    data.mode.modeTimerFired(data)
        

def redrawAll(canvas, data):
    data.mode.drawMode(canvas,data)
        


####################################
# use the run function as-is
####################################

def run(width=300, height=300):
    def redrawAllWrapper(canvas, data):
        canvas.delete(ALL)
        redrawAll(canvas, data)
        canvas.update()    

    def mousePressedWrapper(event, canvas, data):
        mousePressed(event, data)
        redrawAllWrapper(canvas, data)

    def keyPressedWrapper(event, canvas, data):
        keyPressed(event, data)
        redrawAllWrapper(canvas, data)

    def timerFiredWrapper(canvas, data):
        timerFired(data)
        redrawAllWrapper(canvas, data)
        # pause, then call timerFired again
        canvas.after(data.timerDelay, timerFiredWrapper, canvas, data)
    # Set up data and call init
    class Struct(object): pass
    data = Struct()
    data.width = width
    data.height = height
    data.timerDelay = 100 # milliseconds
    init(data)
    # create the root and the canvas
    global root
    root = Tk()
    canvas = Canvas(root, width=data.width, height=data.height)
    canvas.pack()
    # set up events
    root.bind("<Button-1>", lambda event:
                            mousePressedWrapper(event, canvas, data))
    root.bind("<Key>", lambda event:
                            keyPressedWrapper(event, canvas, data))
    timerFiredWrapper(canvas, data)
    # and launch the app
    root.mainloop()  # blocks until window is closed
    print("bye!")

run(500,500)

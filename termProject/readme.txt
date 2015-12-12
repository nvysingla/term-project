This project aims to allow visually impaired individuals better access to printed and handwritten text. 
The program takes in an image that could contain English language characters using a webcam and then allows a user to process it either as printed text or as handwritten text. Both modes obtain a string of characters from the image and allow the user to either use the computer’s speakers to say the text out loud or save the text as Braille in a Word Document. 

To run it: 
Once the below mentioned modules have been installed, proceed to next step.
Make sure that segmenting2.py and UIversion5.py are in the same directory. Then, run the file UIversion5.py as a normal python file.


Module Installation:

Open CV and numpy installation:
	Refer to Vasu Agrawal's installation guide: https://docs.google.com/document/d/1j4wBKNKR4KoW4ZLrkwu0PCoypC_mJvRJUfx2JKLHREU/edit

Pyttsx and Pywin:

	Pywin/Win32 has a GUI Installer, so simply install the newest file from the link below and follow the instructions on screen.
	http://sourceforge.net/projects/pywin32/files/pywin32/
	
	Using a terminal, cd into the folder containing pip (C:/Python27/Lib/site-packages) and then follow the commands from the official documentation below:
	http://pyttsx.readthedocs.org/en/latest/install.html

Pytesser:
	Downloaded from: https://pypi.python.org/pypi/PyTesser/ or https://code.google.com/p/pytesser/downloads/detail?name=pytesser_v0.0.1.zip
	Install the module the same way as done for pyttsx. except use sudo pip install pytesser

PIL:
	Downloaded from :http://www.pythonware.com/products/pil/	
	Install the module the same way as done for pyttsx. except use sudo pip install <name of the pil file that you downloaded>
	
	
Tkinter/Sys: Inbuilt
	
import sys
import os
import glob

import numpy as np
from PIL import Image

from PyQt5.QtWidgets import QListWidget, QPushButton, QLabel, QListWidgetItem, QRadioButton, QWidget, QFileDialog, QLineEdit, QApplication
from PyQt5.QtGui import QPixmap, QIntValidator, QFont, QGuiApplication
#from PyQt5.QtCore import 

from PyPIV_FFT import PyPIV_FFT

import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

#main GUI file
#run this one to run PyPIV program


#this is the main class which everything runs from
#contains the QApplication to exectue
#also creates the main window of the program
class PIV_GUI():
    def __init__(self):
        #all of this is just laying out the window
        app = QApplication([])
        window = QWidget()
        window.setGeometry(30,100,1000,750)
        
        #create a font
        self.font = QFont('SansSerif',13)
        
        #declare variables
        self.imagearray = np.zeros((2,2,2))
        
        #creates button connected to file selection routine
        self.fileSelection = QPushButton(window)
        self.fileSelection.setText('Choose Images')
        self.fileSelection.clicked.connect(self.fileWindow)
        self.fileSelection.setFont(self.font)
        
        #checking masks files
        self.mask = checkBox('Masks option', window)
        self.mask.mover(500,220)
        
        #straddling Boolean
        self.straddle = checkBox('Straddling', window)
        self.straddle.mover(400,220)
        
        #laying out numberical input objects
        self.windowSize = inputBox('Window Size',window)
        self.windowSize.move(400,25)
        self.windowSize.title.move(400,10)
        self.windowSize.setFont(self.font)
        
        self.stepSize = inputBox('Step Size',window)
        self.stepSize.move(400,75)
        self.stepSize.title.move(400,60)
        self.stepSize.setFont(self.font)
        
        self.numImage = inputBox('Number of Image Pairs',window)
        self.numImage.move(400,125)
        self.numImage.title.move(400,110)
        self.numImage.setFont(self.font)
        
        self.imageStep = inputBox('Image Step',window)
        self.imageStep.move(400,175)
        self.imageStep.title.move(400,160)
        self.imageStep.setFont(self.font)
        
        #run buttons
        self.Xcorr = QPushButton(window)
        self.Xcorr.setText('PIV XCorr')
        self.Xcorr.move(20,440)
        self.Xcorr.clicked.connect(self.Xcorr_run)
        self.Xcorr.setFont(self.font)
        
        self.CNN = QPushButton(window)
        self.CNN.setText('PIV CNN')
        self.CNN.move(120,440)
        self.CNN.clicked.connect(self.CNN_run)
        self.CNN.setFont(self.font)
        
        
        window.show()
        app.exec_()
        
        
        
    #creates window to run cross correlation from
    def Xcorr_run(self):
        self.Xcorr_window = QWidget()
        self.Xcorr_window.setGeometry(200,200,500,500)
        
        #directory selection button
        self.outdir = QPushButton('Choose Output Directory',self.Xcorr_window)
        self.outdir.move(0,0)
        self.outdir.setFont(self.font)
        self.outdir.clicked.connect(self.direcSelection)
        
        #button to initiate FFT
        self.fftbutton = QPushButton('Run FFT',self.Xcorr_window)
        self.fftbutton.move(0,40)
        self.fftbutton.setFont(self.font)
        self.fftbutton.clicked.connect(self.FFT_analysis)
        
        #brings up window
        self.Xcorr_window.show()
        
    def direcSelection(self):
        self.outdirec = QFileDialog.getExistingDirectory()
        
        
        
        
        
        
#calls the FFT function with objects from the main window
    def FFT_analysis(self):
        self.Xcorr_window.close()
        self.progresswindow = QWidget()
        self.progresswindow.setGeometry(300,300,200,200)
        
         #Labels to show progress 
        self.imageloading = QLabel(self.progresswindow)
        self.imageloading.move(0,0)
        self.imageloading.setText('Analyzing Sets')
        self.imageloading.setFont(self.font)
        self.analysisprogress = QLabel(self.progresswindow)
        self.analysisprogress.move(0,20)
        self.analysisprogress.setText('                        ')
        self.analysisprogress.setFont(self.font)
        self.progresswindow.show()
        
        imshape = np.shape(self.imagearray)
        
        progressstr = '%d / ' + '%d' % imshape[2]
        self.analysisprogress.setText(progressstr % 0)
        
        
        for i in range(imshape[2]-1):
            #update progress display
            self.analysisprogress.setText(progressstr % i)
            #necessary for updating the GUI while processes are running
            QGuiApplication.processEvents()
            
            head = 'image %d and %d x,y,u,v' % (i,(i+1))
            
            #funstion that computes the velocities through simple FFT
            x,y,u,v = PyPIV_FFT(self.imagearray[:,:,i], self.imagearray[:,:,i+1], self.windowSize.value, self.stepSize.value)
            
            #creating output file
            filename = self.outdirec + '/PIV_%04d.txt' % i
            #shaping data for output file
            dims = np.shape(x)
            out = np.reshape(np.transpose([np.reshape(x,(1,dims[0]*dims[1])), np.reshape(y,(1,dims[0]*dims[1])), np.reshape(u,(1,dims[0]*dims[1])), np.reshape(v,(1,dims[0]*dims[1]))]),(dims[0]*dims[1],4))
            np.savetxt(filename,out,fmt='%03.5f',delimiter='   ',header=head)
        
#            self.figwin = QWidget()
#            self.figwin.close()
#            #complicated matplotlib to pyqt stuff
#            fig,ax = plt.subplots(figsize=(30, 20))
#            ax.quiver(u,v,headwidth=2,headlength=3)
#            plt.savefig('out.png')
#        
#            self.figwin.setGeometry(500,300,1100,800)
#            pic = QLabel(self.figwin)
#            graph = QPixmap('out.png')
#            pic.setPixmap(graph.scaledToWidth(1000))
#            self.figwin.show()
        
        self.progresswindow.close()
        
        
    def CNN_run(self):
        print('Running PIV Neural Net Analysis\n')

        
    #function creates and lays out a new window for choosing images
    def fileWindow(self):
       
        
        #create new window
        self.selectionWindow = QWidget()
        self.selectionWindow.setGeometry(200,200,500,500)
        
        
        
        #button to select first image
        self.firstImage = QPushButton('Choose First Image',self.selectionWindow)
        self.firstImage.move(0,0)
        self.firstImage.setFont(self.font)
        self.firstImage.clicked.connect(self.imageSelection)
        
        #button to load images into program
        self.loadimages = QPushButton('Load Images',self.selectionWindow)
        self.loadimages.move(150,450)
        self.loadimages.setFont(self.font)
        self.loadimages.clicked.connect(self.load)
        
        #textbox for directory
        self.directorylabel = QLabel(self.selectionWindow)
        self.directorylabel.move(0,50)
        self.directorylabel.setText('Directory')
        self.directorylabel.setFont(self.font)
        self.directory = QLineEdit(self.selectionWindow)
        self.directory.move(0,70)
        
        
        #textbox for file basename
        self.basenamelabel = QLabel(self.selectionWindow)
        self.basenamelabel.move(0,100)
        self.basenamelabel.setText('Image Base Name')
        self.basenamelabel.setFont(self.font)
        self.basename = QLineEdit(self.selectionWindow)
        self.basename.move(0,120)
        
        #textbox for filetype
        self.filetypelabel = QLabel(self.selectionWindow)
        self.filetypelabel.move(0,150)
        self.filetypelabel.setText('File Type')
        self.filetypelabel.setFont(self.font)
        self.filetype = QLineEdit(self.selectionWindow)
        self.filetype.move(0,170)
        
        #textbox for number of digits
        self.numdigitslabel = QLabel(self.selectionWindow)
        self.numdigitslabel.move(0,200)
        self.numdigitslabel.setText('Number of Digits')
        self.numdigitslabel.setFont(self.font)
        self.numdigits = QLineEdit(self.selectionWindow)
        self.numdigits.move(0,220)
        
        #textbox for first image
        self.firstimagelabel = QLabel(self.selectionWindow)
        self.firstimagelabel.move(0,250)
        self.firstimagelabel.setText('First Image')
        self.firstimagelabel.setFont(self.font)
        self.firstimage = QLineEdit(self.selectionWindow)
        self.firstimage.move(0,270)
        
        #textbox for number of images
        self.numimageslabel = QLabel(self.selectionWindow)
        self.numimageslabel.move(0,300)
        self.numimageslabel.setText('Number of Images')
        self.numimageslabel.setFont(self.font)
        self.numimages = QLineEdit(self.selectionWindow)
        self.numimages.move(0,320)
        
        #brings up window
        self.selectionWindow.show()
        
    def imageSelection(self):
        #funcion to extract and seperate information about files
        #autofills fields in the selection window
        
        #get name of a file from GUI file selection
        file = QFileDialog.getOpenFileName()
        file = file[0]
        
        #extracting the extension of the album
        ftype = file[(file.find('.')):len(file)]
        self.filetype.setText(ftype)
        
        #extract the directory from the full address
        revfile = file[::-1]
        direc=file[0:(len(file)-revfile.find('/'))]
        self.directory.setText(direc)
        
        #cut file down to just the file name with no directory or extension
        file = file[(len(file)-revfile.find('/')):file.find('.')]
        
        #find the number of digits used to enumerate
        self.numdigits.setText(str(len(file)-file.find('0')))
        
        #filename with enumeration digits removed
        base = file[0:file.find('0')]
        self.basename.setText(base)
        
        #finds all files in the same directory with the same base name
        files = glob.glob(direc + base + '*' + ftype)
        self.numimages.setText(str(len(files)))
        
        #takes digits from the first image file in the list
        firstim = files[0]
        firstim = firstim[(firstim.find('\\')+1):firstim.find('.')]
        firstim = firstim[firstim.find('0'):len(firstim)]
        self.firstimage.setText(firstim)
        
    def load(self):
        
        #create a new window to show progress
        self.selectionWindow.close()
        self.loadwindow = QWidget()
        self.loadwindow.setGeometry(300,300,200,200)
        
         #Labels to show progress 
        self.imageloading = QLabel(self.loadwindow)
        self.imageloading.move(0,0)
        self.imageloading.setText('Loading Images')
        self.imageloading.setFont(self.font)
        self.progress = QLabel(self.loadwindow)
        self.progress.move(0,20)
        self.progress.setText('                        ')
        self.progress.setFont(self.font)
        self.loadwindow.show()
        
        
        
        #create template to call each file individually
        filename = self.directory.text() + self.basename.text() + '%0' + self.numdigits.text() + 'd' + self.filetype.text()
        
        #shape imarray with sample image
        files = glob.glob(self.directory.text() + self.basename.text() + '*' + self.filetype.text())
        dim = np.shape(np.array(Image.open(files[0])))
        self.imagearray = np.zeros((dim[0], dim[1], int(self.numimages.text())))
        
        #set up a string to show progress
        progressstr = '%d / ' + '%d' % int(self.numimages.text())
        self.progress.setText(progressstr % 0)
        
        #load images in loop
        for i in range(int(self.numimages.text())):
            
            #update progress display
            self.progress.setText(progressstr % i)
            #necessary for updating the GUI while processes are running
            QGuiApplication.processEvents()
            
            #actually fills the global imarray with images converted to arrays
            self.imagearray[:,:,i] = np.array(Image.open(filename % i))
        
        self.loadwindow.close()
        
        
        
        
#Numerical Input Lines
class inputBox(QLineEdit):
    def __init__(self,title,window):
        super(inputBox,self).__init__(window)
        self.title = QLabel(window)
        self.title.setText(title)
        self.setValidator(QIntValidator())
        self.textChanged.connect(self.change)
        self.value = 0
        
    def change(self,num):
        self.value = int(num)
        
        
#Boolean input
class checkBox(QRadioButton):
    def __init__(self,title,window):
        super(checkBox,self).__init__(window)
        self.title = QLabel(window)
        self.title.setText(title)
        self.value = False
        self.toggled.connect(self.change)
        
    def change(self, value):
        self.value = value
        
    def mover(self,x,y):
        self.move(x,(y+15))
        self.title.move(x,y)
        

if __name__ == '__main__':
    PIV_GUI()

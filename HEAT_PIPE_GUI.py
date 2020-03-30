import sys
import os
import glob

import numpy as np
from PIL import Image

from PyQt5.QtWidgets import QListWidget, QPushButton, QLabel, QListWidgetItem, QRadioButton, QWidget, QFileDialog, QLineEdit, QApplication
from PyQt5.QtGui import QPixmap, QIntValidator, QFont, QGuiApplication
#from PyQt5.QtCore import 

#from PyPIV_FFT import PyPIV_FFT

import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

#main GUI file
#run this one to run PyPIV program


#this is the main class which everything runs from
#contains the QApplication to exectue
#also creates the main window of the program
class HEAT_PIPE_GUI():
    def __init__(self):
        #all of this is just laying out the window
        app = QApplication([])
        window = QWidget()
        window.setGeometry(100,100,1700,750)
        
        #create a font
        self.font = QFont('SansSerif',13)
        
        #declare variables
        self.imagearray = np.zeros((2,2,2))
        
        #creates button connected to file selection routine
        self.fileSelection = QPushButton(window)
        self.fileSelection.setText('Choose Images')
        self.fileSelection.move(100,20)
        self.fileSelection.clicked.connect(self.fileWindow)
        self.fileSelection.setFont(self.font)
        
        #Steady Operation Option
        self.steadyOp = checkBox('Steady Operation', window)
        self.steadyOp.mover(400,20)
        
        #Transient Operation Option
        self.transOp = checkBox('Transient Operation', window)
        self.transOp.mover(600,20)

        # heat pipe params
        self.pipeOD = inputBox('Heat Pipe Outer Diameter (mm)',window)
        self.pipeOD.move(100,125)
        self.pipeOD.title.move(100,110)
        self.pipeOD.setFont(self.font)

        self.pipeID = inputBox('Heat Pipe Inner Diameter (mm)',window)
        self.pipeID.move(100,175)
        self.pipeID.title.move(100,160)
        self.pipeID.setFont(self.font)

        self.vapcoreDia = inputBox('Vapor Core Diameter',window)
        self.vapcoreDia.move(100,225)
        self.vapcoreDia.title.move(100,210)
        self.vapcoreDia.setFont(self.font)

        self.numEvapNode = inputBox('Number of Evaporator Nodes',window)
        self.numEvapNode.move(100,275)
        self.numEvapNode.title.move(100,260)
        self.numEvapNode.setFont(self.font)

        self.numAdiaNode = inputBox('Number of Adiabatic Section Nodes',window)
        self.numAdiaNode.move(100,325)
        self.numAdiaNode.title.move(100,310)
        self.numAdiaNode.setFont(self.font)
        
        self.numCondNode = inputBox('Number of Condensor Nodes',window)
        self.numCondNode.move(100,375)
        self.numCondNode.title.move(100,360)
        self.numCondNode.setFont(self.font)

        self.pipeInclination = inputBox('Heat Pipe Inclination',window)
        self.pipeInclination.move(100,425)
        self.pipeInclination.title.move(100,410)
        self.pipeInclination.setFont(self.font)

         #laying out wick properties
        self.wickThickness = inputBox('Wick Thickness',window)
        self.wickThickness.move(400,125)
        self.wickThickness.title.move(400,110)
        self.wickThickness.setFont(self.font)

        self.wireDia = inputBox('Wire Diameter',window)
        self.wireDia.move(400,175)
        self.wireDia.title.move(400,160)
        self.wireDia.setFont(self.font)
        
        self.wireMeshNum = inputBox('Wire Mesh Number',window)
        self.wireMeshNum.move(400,225)
        self.wireMeshNum.title.move(400,210)
        self.wireMeshNum.setFont(self.font)
        
        self.wickCapilRadi = inputBox('Wick Capillary Radius',window)
        self.wickCapilRadi.move(400,275)
        self.wickCapilRadi.title.move(400,260)
        self.wickCapilRadi.setFont(self.font)
        
        self.wickPorosity = inputBox('Wick Porosity',window)
        self.wickPorosity.move(400,325)
        self.wickPorosity.title.move(400,310)
        self.wickPorosity.setFont(self.font)
        
        self.wickCrimpFact = inputBox('Wick Crimping Factor',window)
        self.wickCrimpFact.move(400,375)
        self.wickCrimpFact.title.move(400,360)
        self.wickCrimpFact.setFont(self.font)

        self.wickPermeability = inputBox('Wick Permeability',window)
        self.wickPermeability.move(400,425)
        self.wickPermeability.title.move(400,410)
        self.wickPermeability.setFont(self.font)
        
         #sodium properties
        self.sodiumLiquidDensity = inputBox('Sodium Liquid Density',window)
        self.sodiumLiquidDensity.move(700,125)
        self.sodiumLiquidDensity.title.move(700,110)
        self.sodiumLiquidDensity.setFont(self.font)
        
        self.sodiumLiquidViscosity = inputBox('Sodium Liquid Viscosity',window)
        self.sodiumLiquidViscosity.move(700,175)
        self.sodiumLiquidViscosity.title.move(700,160)
        self.sodiumLiquidViscosity.setFont(self.font)
        
        self.sodiumSurfTensCoeff = inputBox('Sodium Surface Tension Coefficient',window)
        self.sodiumSurfTensCoeff.move(700,225)
        self.sodiumSurfTensCoeff.title.move(700,210)
        self.sodiumSurfTensCoeff.setFont(self.font)
        
        self.sodiumThermCond = inputBox('Sodium Thermal Conductivity',window)
        self.sodiumThermCond.move(700,275)
        self.sodiumThermCond.title.move(700,260)
        self.sodiumThermCond.setFont(self.font)
        
        self.sodiumLatentHeat = inputBox('Sodium Latent Heat',window)
        self.sodiumLatentHeat.move(700,325)
        self.sodiumLatentHeat.title.move(700,310)
        self.sodiumLatentHeat.setFont(self.font)
        
        self.sodiumVaporDensity = inputBox('Sodium Vapor Density',window)
        self.sodiumVaporDensity.move(700,375)
        self.sodiumVaporDensity.title.move(700,360)
        self.sodiumVaporDensity.setFont(self.font)
        
        self.sodiumVaporViscosity = inputBox('Sodium Vapor Viscosity',window)
        self.sodiumVaporViscosity.move(700,425)
        self.sodiumVaporViscosity.title.move(700,410)
        self.sodiumVaporViscosity.setFont(self.font)


         #conditions
        self.operationTemp = inputBox('Operation Temperature',window)
        self.operationTemp.move(1000,125)
        self.operationTemp.title.move(1000,110)
        self.operationTemp.setFont(self.font)
        
        self.operationPressure = inputBox('Operation Pressure',window)
        self.operationPressure.move(1000,175)
        self.operationPressure.title.move(1000,160)
        self.operationPressure.setFont(self.font)
        
        self.sodiumSurfTensCoeff = inputBox('Sodium Surface Tension Coefficient',window)
        self.sodiumSurfTensCoeff.move(1000,225)
        self.sodiumSurfTensCoeff.title.move(1000,210)
        self.sodiumSurfTensCoeff.setFont(self.font)
        
        self.sodiumThermCond = inputBox('Sodium Thermal Conductivity',window)
        self.sodiumThermCond.move(1000,275)
        self.sodiumThermCond.title.move(1000,260)
        self.sodiumThermCond.setFont(self.font)
        
        self.wireDia = inputBox('Wire Diameter',window)
        self.wireDia.move(1000,325)
        self.wireDia.title.move(1000,310)
        self.wireDia.setFont(self.font)
        
        self.wireMeshNum = inputBox('Wire Mesh Number',window)
        self.wireMeshNum.move(1000,375)
        self.wireMeshNum.title.move(1000,360)
        self.wireMeshNum.setFont(self.font)        
        self.wireMeshNum.insert(' Added')

        #run buttons
        self.SteadyOp = QPushButton(window)
        self.SteadyOp.setText('Steady Operation')
        self.SteadyOp.move(100,640)
        self.SteadyOp.clicked.connect(self.SteadyOp_run)
        self.SteadyOp.setFont(self.font)

        self.Xcorr = QPushButton(window)
        self.Xcorr.setText('PIV XCorr')
        self.Xcorr.move(400,640)
        self.Xcorr.clicked.connect(self.Xcorr_run)
        self.Xcorr.setFont(self.font)
        
        self.CNN = QPushButton(window)
        self.CNN.setText('PIV CNN')
        self.CNN.move(700,640)
        self.CNN.clicked.connect(self.CNN_run)
        self.CNN.setFont(self.font)

        window.show()
        app.exec_()
        
        
        
    #creates window to run cross correlation from
    def SteadyOp_run(self):
        self.SteadyOp_window = QWidget()
        self.SteadyOp_window.setGeometry(200,200,500,500)
        
        #directory selection button
        self.outdir = QPushButton('Choose Output Directory',self.SteadyOp_window)
        self.outdir.move(20,20)
        self.outdir.setFont(self.font)
        self.outdir.clicked.connect(self.direcSelection)
        
        #button to initiate FFT
        self.fftbutton = QPushButton('Run FFT',self.SteadyOp_window)
        self.fftbutton.move(20,60)
        self.fftbutton.setFont(self.font)
        self.fftbutton.clicked.connect(self.FFT_analysis)
        
        self.textbox = QLineEdit(self.SteadyOp_window)
        self.textbox.move(20, 100)
        self.textbox.resize(280,40)
        
        #brings up window
        self.SteadyOp_window.show()
        
        #display results
        l1 = QLabel()
        l2 = QLabel()
        l3 = QLabel()
        l4 = QLabel()
	
        l1.setText("Hello World")
        l4.setText("TutorialsPoint")
        l2.setText("welcome to Python GUI Programming")
        self.textbox.insert(l1.text())
        self.textbox.setFont(self.font)
 
        

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
        
        
    def Xcorr_run(self):
        print('Running PIV Xcorr Analysis\n')
        
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
    HEAT_PIPE_GUI()

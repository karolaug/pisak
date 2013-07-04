#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import Image
import cv2
import numpy as np

from cameo import Cameo

#from PySide import QtCore, QtGui
from PyQt4 import QtCore, QtGui

class TestWidget(QtGui.QWidget):
    def __init__(self, parent=None):
        QtGui.QWidget.__init__(self, parent)
        
        self.scene = QtGui.QGraphicsScene()
        self.view  = QtGui.QGraphicsView(self.scene)

        self.im = np.load('pickle.npy')
        self.im2 = self.im.astype('uint8')

        self.comboBox_cam = QtGui.QComboBox()
        self.comboBox_cam.setObjectName("comboBox_cam")
        cameras = self.lookForCameras()
        for i in cameras:
            self.comboBox_cam.addItem(i)
        
        self.camera_label = QtGui.QLabel()
        self.camera_label.setObjectName("camera_label")
        self.camera_label.setText(QtGui.QApplication.translate("QWidget", "Wybierz kamerę:", None, QtGui.QApplication.UnicodeUTF8))
        
        self.resolution_label = QtGui.QLabel()
        self.resolution_label.setObjectName("resolution_label")
        self.resolution_label.setText(QtGui.QApplication.translate("QWidget", "Wybierz rozdzielczość:", None, QtGui.QApplication.UnicodeUTF8))
                
        self.comboBox_res = QtGui.QComboBox()
        self.comboBox_res.setObjectName("comboBox_res")
        
        self.resolutions_w = [160,320,640,1280]
        self.resolutions_h = [120,240,480,720]
        for i in xrange(len(self.resolutions_w)):
            tmp = str(self.resolutions_w[i]) + " x " + str(self.resolutions_h[i])
            self.comboBox_res.addItem(tmp)
        
        self.view_label = QtGui.QLabel()
        self.view_label.setObjectName("view_label")
        self.view_label.setText(QtGui.QApplication.translate("QWidget", "Podgląd obrazu:", None, QtGui.QApplication.UnicodeUTF8))
        
        self.pushButton = QtGui.QPushButton()
        self.pushButton.setObjectName("button")
        self.pushButton.setText(QtGui.QApplication.translate("QWidget", "Uruchom", None, QtGui.QApplication.UnicodeUTF8))
        
        self.imageDummy(62)
        
        layout = QtGui.QVBoxLayout()
        
        layout.addWidget(self.resolution_label)
        layout.addWidget(self.comboBox_res)
        
        layout.addWidget(self.camera_label)
        layout.addWidget(self.comboBox_cam)
        
        layout.addWidget(self.view_label)
        layout.addWidget(self.view)
        
        layout.addWidget(self.pushButton)
        
        self.setLayout(layout)

        self.comboBox_cam.currentIndexChanged.connect(self.imageChange)
        self.comboBox_res.currentIndexChanged.connect(self.resolutionChange)
        self.pushButton.clicked.connect(self.uruchom)

#######################################################
# FUNKCJA PRZEGRZEBUJĄCA ZBIÓR MOŻLIWYCH KAMER        #
#######################################################
    def lookForCameras(self):
		listOfCameras = ['dummy']
		
		device = 0
		while True:
			cap = cv2.VideoCapture(device)		# to zwraca jakiś "pseudo" błąd dla pierwszego niedostępnego indeksu oraz jakiś inne g*wna nawet jak jest ok - nie umiem ubić tego wypisania
			ret,im = cap.read()
			if ret:
				device += 1
				cameraLabel = 'Camera_' + str(device)
				listOfCameras.append(cameraLabel)
			else:
				break
		return listOfCameras
		
#######################################################
# METODA ZMIENIAJĄCA ROZDZIELCZOŚĆ                    #
#######################################################
    def resolutionChange(self):
		index  = self.comboBox_res.currentIndex()
		self.h = self.resolutions_h[index]
		self.w = self.resolutions_w[index]
		if self.comboBox_cam.currentText() == 'dummy':
			pass
		else:
		    self.imageChange()

#######################################################
# METODA ZMIENIAJĄCA OBRAZ W ZALEŻNOŚCI OD COMBO      #
#######################################################
    def imageChange(self):
        selectedCameraIndex = self.comboBox_cam.currentIndex()
        selectedCameraName  = self.comboBox_cam.currentText()
        self.scene.removeItem(self.pixItem)
    
        if selectedCameraName == 'dummy':
            self.imageDummy(62)
        else:
			self.imageCamera(selectedCameraIndex)
				
#######################################################
# UMIESZCZENIE OBRAZU Z KAMERY                        #
#######################################################
    def imageCamera(self, selectedCameraIndex):		
        cap = cv2.VideoCapture(selectedCameraIndex-1)			# -1, bo numeracja jest od zera, a użytkownik widzi od 1
        cap.set(3,self.w)
        cap.set(4,self.h)
        ret,im = cap.read()
        
        b = im[:,:,0]
        g = im[:,:,1]
        r = im[:,:,2]

        b_c = Image.fromarray(b)
        g_c = Image.fromarray(g)
        r_c = Image.fromarray(r)
        tmp = Image.merge('RGB', (r_c, g_c, b_c))

        tmp.show()

        result  = QtGui.QImage(tmp.tostring() , self.w , self.h , QtGui.QImage.Format_RGB888)
        pixmap = QtGui.QPixmap.fromImage(result)
        self.pixItem = QtGui.QGraphicsPixmapItem(pixmap)
        self.scene.addItem(self.pixItem)
        self.view.fitInView(self.pixItem)
        self.scene.update()
        self.view.show()
            
#######################################################
# UMIESZCZENIE OBRAZU Z PLIKU                         #
#######################################################
    def imageDummy(self, index):
        im2 = self.im2[index] 

        b = im2[:,:,0]
        g = im2[:,:,1]
        r = im2[:,:,2]

        self.comboBox_res.setCurrentIndex(2)

        self.resolutionChange()

        b_c = Image.fromarray(b)
        g_c = Image.fromarray(g)
        r_c = Image.fromarray(r)
        tmp = Image.merge('RGB', (r_c, g_c, b_c))

        result  = QtGui.QImage(tmp.tostring() , self.w , self.h , QtGui.QImage.Format_RGB888)
    
        pixmap = QtGui.QPixmap.fromImage(result)
        self.pixItem = QtGui.QGraphicsPixmapItem(pixmap)
        self.scene.addItem(self.pixItem)
        self.view.fitInView(self.pixItem)
        self.scene.update()
        self.view.show()
#######################################################
# URUCHAMIA EYETRACKER                                #
#######################################################
    def uruchom(self):
        
        selectedCameraIndex = self.comboBox_cam.currentIndex()
        selectedCameraName  = self.comboBox_cam.currentText()
        
        if selectedCameraName == 'dummy':
            index = 'dummy'
        else:
            index = selectedCameraIndex-1

        a = Cameo(self.w , self.h , index)
        
        a.run()
        
        #QtGui.QWidget.destroy()

#######################################################
# TEGO NIE NALEŻY USUWAĆ, BO TO DLA MNIE KAWAŁ WIEDZY #
#######################################################
    #def do_test(self):
        #img = Image.open('image.png')
        #enhancer = ImageEnhance.Brightness(img)
        #for i in range(1, 8):
            #img = enhancer.enhance(i)
            #self.display_image(img)
            #QCoreApplication.processEvents()  # let Qt do his work
            #time.sleep(0.5)

    #def display_image(self, img):
        #self.scene.clear()
        #w, h = img.size
        #self.imgQ = ImageQt.ImageQt(img)  # we need to hold reference to imgQ, or it will crash
        #pixMap = QPixmap.fromImage(self.imgQ)
        #self.scene.addPixmap(pixMap)
        #self.view.fitInView(QRectF(0, 0, w, h), Qt.KeepAspectRatio)
        #self.scene.update()
#######################################################
#######################################################

if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    widget = TestWidget()
    widget.resize(800, 700)
    widget.setWindowTitle("Eyetracker -- settings -- step1")
    widget.show()

    sys.exit(app.exec_())

#!/usr/bin/env python
# -*- coding: utf-8 -*-

#    This file is part of eyetracker-ng.
#
#    eyetracker-ng is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    eyetracker-ng is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with eyetracker-ng. If not, see <http://www.gnu.org/licenses/>.

# authors: Sasza Kijek, Karol Augustin, Tomasz Spustek
# e-mails: saszasasha@gmail.com karol@augustin.pl tomasz@spustek.pl
# University of Warsaw 2013

import cv2
import numpy as np
import sys
from itertools import izip
from PyQt4 import QtCore, QtGui

from ..analysis.detect import pupil, glint
from ..analysis.processing import threshold, imageFlipMirror, mark

from ..camera.display import drawPupil, drawGlint, displayImage
from ..camera.capture import lookForCameras
from ..camera.camera import Camera

from .graphical import Ui_StartingWindow

#################################### URUCHOMIENIE PROGRAMU

class MyForm(QtGui.QMainWindow):
    def __init__(self, parent=None):
        QtGui.QWidget.__init__(self, parent)
        self.ui = Ui_StartingWindow()
        self.ui.setupUi(self)
        
        ############################# INICJALIZACJA PARAMETRÓW        
        self.cameras = lookForCameras()
        for i in self.cameras.iterkeys():
            self.ui.cmb_setCamera.addItem(i)
        
        self.algorithms = ['NESW']
        for algorithm in self.algorithms:
            self.ui.cmb_setAlgorithm.addItem(algorithm)
        
        self.resolutions_w = [160,320,640,1280]
        self.resolutions_h = [120,240,480,720]
        for w, h in izip(self.resolutions_w, self.resolutions_h):
            self.ui.cmb_setResolution.addItem(''.join([str(w), 'x', str(h)]))
            
        self.ui.cmb_setResolution.setCurrentIndex(1)
        self.w = 320
        self.h = 240
        self.selectedCameraName  = self.ui.cmb_setCamera.currentText()
        self.selectedCameraIndex = self.ui.cmb_setCamera.currentIndex()
        #self.index = 0
        #self.im = np.load('pickle.npy').astype('uint8')

        self.camera = Camera(self.cameras['Camera_1'], 
                             {3 : self.w, 4 : self.h})

        self.mirrored = 0
        self.fliped = 0
        self.advanced = 0
        
        self.ui.lbl_pupil1.setText(str(self.ui.hsb_pupil1.value()))
        self.ui.lbl_pupil2.setText(str(self.ui.hsb_pupil2.value()))
        self.ui.lbl_pupil3.setText(str(self.ui.hsb_pupil3.value()))
        self.ui.lbl_glint1.setText(str(self.ui.hsb_glint1.value()))
        self.ui.lbl_glint2.setText(str(self.ui.hsb_glint2.value()))
        self.ui.lbl_glint3.setText(str(self.ui.hsb_glint3.value()))
        
        self.ui.timer.start(100 , self) # będzie odpalał co 100 ms, self odbiera zdarzenia

        ################################### DOWIĄZANIA ZDARZEŃ
        self.ui.cmb_setCamera.currentIndexChanged.connect(self.cameraChange)
        self.ui.cmb_setResolution.currentIndexChanged.connect(self.resolutionChange)
        self.ui.cmb_setAlgorithm.currentIndexChanged.connect(self.algorithmChange)
        #self.ui.btn_start.clicked.connect(self.startEyetracker)
        self.ui.btn_settings.clicked.connect(self.startAdvancedSettings)
        self.ui.chb_flip.stateChanged.connect(self.imageFlip)
        self.ui.chb_mirror.stateChanged.connect(self.imageMirror)
        self.ui.hsb_pupil1.valueChanged[int].connect(self.hsbPupil_1Change)
        self.ui.hsb_pupil2.valueChanged[int].connect(self.hsbPupil_2Change)
        self.ui.hsb_pupil3.valueChanged[int].connect(self.hsbPupil_3Change)
        self.ui.hsb_glint1.valueChanged[int].connect(self.hsbGlint_1Change)
        self.ui.hsb_glint2.valueChanged[int].connect(self.hsbGlint_2Change)
        self.ui.hsb_glint3.valueChanged[int].connect(self.hsbGlint_3Change)

########################################### CYKANIE ZEGARA #
    def timerEvent(self, event):
        
        if self.advanced == 0:      # update małego okienka w podstawowym gui
            im = self.camera.frame()
            im = imageFlipMirror(im, self.mirrored, self.fliped)
            self.displayGuiImage(im)
            
        else:                       # update dwóch okien w ustawieniach zaawansowanych
            im = self.camera.frame()
            im = imageFlipMirror(im, self.mirrored, self.fliped)
            
            pupil = self.pupilDetectionUpdate(gray)
            glint = self.blackAndWhiteUpdate(gray)
            
            displayImage(pupil, 'pupil_detection')
            displayImage(glint, 'glint_detection')

############################## METODA ZMIENIAJĄCA ALGORYTM #
    def algorithmChange(self):
        pass
################################ METODA ZMIENIAJĄCA KAMERĘ #
    def cameraChange(self):
        self.ui.timer.stop()
        if self.selectedCameraName == 'dummy':
            pass
        else:
            self.camera.close()

        self.selectedCameraIndex = self.ui.cmb_setCamera.currentIndex()
        self.selectedCameraName  = self.ui.cmb_setCamera.currentText()
        
        if self.selectedCameraName == 'dummy':
            self.index = 0
        else:
            self.camera = Camera(self.selectedCameraIndex-1, 
                                 {3 : 320, 4 : 240})		# -1, bo numeracja jest od zera, a użytkownik widzi od 1

        self.ui.timer.start(100 , self)

######################### METODA ODBIJAJĄCA OBRAZ GÓRA-DÓŁ #
    def imageMirror(self):
        if self.mirrored == 0:
            self.mirrored = 1
        else:
            self.mirrored = 0

####################### METODA ODBIJAJĄCA OBRAZ LEWO-PRAWO #
    def imageFlip(self):
        if self.fliped == 0:
            self.fliped = 1
        else:
            self.fliped = 0

######################### METODA ZMIENIAJĄCA ROZDZIELCZOŚĆ #
    def resolutionChange(self):
		index  = self.ui.cmb_setResolution.currentIndex()
		self.h = self.resolutions_h[index]
		self.w = self.resolutions_w[index]
        
############################# UMIESZCZENIE OBRAZU Z KAMERY #
    def displayGuiImage(self, im):
        '''
        To do
        '''
        result = QtGui.QImage(im , 320 , 240 , QtGui.QImage.Format_RGB888).rgbSwapped()
        pixmap  = QtGui.QPixmap.fromImage(result)
        pixItem = QtGui.QGraphicsPixmapItem(pixmap)
        self.ui.graphicsScene.addItem(pixItem)
        self.ui.graphicsView.fitInView(pixItem)
        self.ui.graphicsScene.update()
        self.ui.graphicsView.show()
    
### FUNKCJA WŁĄCZAJĄCA/WYŁACZAJĄCA ZAAWANSOWANE USTAWIENIA #
    def startAdvancedSettings(self):
        if self.advanced == 0:
            self.ui.hsb_glint1.setEnabled(True)
            self.ui.hsb_glint2.setEnabled(True)
            self.ui.hsb_glint3.setEnabled(True)
            self.ui.hsb_pupil1.setEnabled(True)
            self.ui.hsb_pupil2.setEnabled(True)
            self.ui.hsb_pupil3.setEnabled(True)
            self.ui.chb_mirror.setEnabled(False)
            self.ui.chb_flip.setEnabled(False)
            self.ui.cmb_setResolution.setEnabled(False)
            self.ui.cmb_setCamera.setEnabled(False)
            self.ui.btn_start.setEnabled(False)
            
            self.advanced = 1
            
            resolutionIndex = self.ui.cmb_setResolution.currentIndex()
            settings = {3 : self.resolutions_w[resolutionIndex], 
                        4 : self.resolutions_h[resolutionIndex]}
            self.camera.set(settings)
            
            cv2.namedWindow('pupil_detection' , flags=cv2.CV_WINDOW_AUTOSIZE)
            cv2.moveWindow('pupil_detection',800,100)
            cv2.namedWindow('glint_detection' , flags=cv2.CV_WINDOW_AUTOSIZE)
            cv2.moveWindow('glint_detection',800,500)
        else:
            self.ui.hsb_glint1.setEnabled(False)
            self.ui.hsb_glint2.setEnabled(False)
            self.ui.hsb_glint3.setEnabled(False)
            self.ui.hsb_pupil1.setEnabled(False)
            self.ui.hsb_pupil2.setEnabled(False)
            self.ui.hsb_pupil3.setEnabled(False)
            self.ui.chb_mirror.setEnabled(True)
            self.ui.chb_flip.setEnabled(True)
            self.ui.cmb_setResolution.setEnabled(True)
            self.ui.cmb_setCamera.setEnabled(True)
            self.ui.btn_start.setEnabled(True)
            self.advanced = 0
            
            cv2.destroyAllWindows()
        
######### OBSŁUGA SUWAKÓW ZMIENIAJĄCYCH PARAMETRY DETEKCJI #
    def hsbPupil_1Change(self, value):
        self.ui.lbl_pupil1.setText(str(value))
    def hsbPupil_2Change(self, value):
        self.ui.lbl_pupil2.setText(str(value))
    def hsbPupil_3Change(self, value):
        self.ui.lbl_pupil3.setText(str(value))
    def hsbGlint_1Change(self, value):
        self.ui.lbl_glint1.setText(str(value))
    def hsbGlint_2Change(self, value):
        self.ui.lbl_glint2.setText(str(value))
    def hsbGlint_3Change(self, value):
        self.ui.lbl_glint3.setText(str(value))
        
############## UPDATE OBRAZU W USTAWIENIACH ZAAWANSOWANYCH #    
    def pupilDetectionUpdate(self, image):
        pupilThresholds = [self.ui.hsb_pupil1.value(), self.ui.hsb_pupil2.value(), self.ui.hsb_pupil3.value()]
        pupil = drawPupil(image, pupilThresholds)
        return pupil
            
    def blackAndWhiteUpdate(self, image):
        glintThresholds = [self.ui.hsb_glint1.value(), self.ui.hsb_glint2.value(), self.ui.hsb_glint3.value()]
        glint = drawGlint(image, glintThresholds)
        return glint

##########################################################

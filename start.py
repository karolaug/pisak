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
from itertools import izip

from camera_lookup import lookForCameras
from analysis.detect import pupil, glint
from PyQt4 import QtCore, QtGui
from eyetrackerStartGui import Ui_StartingWindow

class MyForm(QtGui.QMainWindow):
    def __init__(self, parent=None):
        QtGui.QWidget.__init__(self, parent)
        self.ui = Ui_StartingWindow()
        self.ui.setupUi(self)
        
        ############################# INICJALIZACJA PARAMETRÓW        
        self.cameras = lookForCameras()
        for i in self.cameras.iterkeys():
            self.ui.cmb_setCamera.addItem(i)
        
        self.resolutions_w = [160,320,640,1280]
        self.resolutions_h = [120,240,480,720]
        for w, h in izip(self.resolutions_w, self.resolutions_h):
            self.ui.cmb_setResolution.addItem(''.join([str(w), 'x', str(h)]))
            
        self.ui.cmb_setResolution.setCurrentIndex(1)
        self.w = 320
        self.h = 240
        self.selectedCameraName  = 'dummy'

        self.mirrored = 0
        self.fliped = 0
        self.advanced = 0                                   # flaga odnośnie zaawansowanych ustawień
        
        self.ui.lbl_pupil1.setText( str(self.ui.hsb_pupil1.value() ) )
        self.ui.lbl_pupil2.setText( str(self.ui.hsb_pupil2.value() ) )
        self.ui.lbl_pupil3.setText( str(self.ui.hsb_pupil3.value() ) )
        self.ui.lbl_glint1.setText( str(self.ui.hsb_glint1.value() ) )
        self.ui.lbl_glint2.setText( str(self.ui.hsb_glint2.value() ) )
        self.ui.lbl_glint3.setText( str(self.ui.hsb_glint3.value() ) )
        
        self.timer = QtCore.QBasicTimer() #czy tego się nie da do tego startGui wywalić?
        self.timer.start(100 , self) # będzie odpalał co 100 ms, self odbiera zdarzenia

        ################################### DOWIĄZANIA ZDARZEŃ
        self.ui.cmb_setCamera.currentIndexChanged.connect(self.cameraChange)
        self.ui.cmb_setResolution.currentIndexChanged.connect(self.resolutionChange)
        self.ui.btn_start.clicked.connect(self.startEyetracker)
        self.ui.btn_settings.clicked.connect(self.startAdvancedSettings)
        self.ui.chb_flip.stateChanged.connect(self.imageFlip)
        self.ui.chb_mirror.stateChanged.connect(self.imageMirror)
        self.ui.hsb_pupil1.valueChanged[int].connect(self.hsbPupil_1Change)
        self.ui.hsb_pupil2.valueChanged[int].connect(self.hsbPupil_2Change)
        self.ui.hsb_pupil3.valueChanged[int].connect(self.hsbPupil_3Change)
        self.ui.hsb_glint1.valueChanged[int].connect(self.hsbGlint_1Change)
        self.ui.hsb_glint2.valueChanged[int].connect(self.hsbGlint_2Change)
        self.ui.hsb_glint3.valueChanged[int].connect(self.hsbGlint_3Change)

########################################### CYKANIE ZEGARA
    def timerEvent(self, event):
        
        if self.advanced == 0:      # update małego okienka w podstawowym gui
            self.imageCamera()
        else:                       # update dwóch okien w ustawieniach zaawansowanych
            if self.selectedCameraName == 'dummy':
                pass
            else:
                ret, im = self.cap.read()
                im = self.imageFlipMirror(im)
                gray = cv2.cvtColor(im , cv2.COLOR_BGR2GRAY)
                
                self.pupilDetectionUpdate(im , gray)
                self.blackAndWhiteUpdate(im , gray)

################################ METODA ZMIENIAJĄCA KAMERĘ
    def cameraChange(self):
        self.timer.stop()
        if self.selectedCameraName == 'dummy':
            pass
        else:
            self.cap.release()

        self.selectedCameraIndex = self.ui.cmb_setCamera.currentIndex()
        self.selectedCameraName  = self.ui.cmb_setCamera.currentText()
        
        if self.selectedCameraName == 'dummy':
            pass
        else:
            self.cap = cv2.VideoCapture(self.selectedCameraIndex-1)		# -1, bo numeracja jest od zera, a użytkownik widzi od 1
            self.cap.set(3,320)
            self.cap.set(4,240)

        self.timer.start(100 , self)

######################### METODA ODBIJAJĄCA OBRAZ GÓRA-DÓŁ
    def imageMirror(self):
        if self.mirrored == 0:
            self.mirrored = 1
        else:
            self.mirrored = 0

####################### METODA ODBIJAJĄCA OBRAZ LEWO-PRAWO
    def imageFlip(self):
        if self.fliped == 0:
            self.fliped = 1
        else:
            self.fliped = 0
                                                                        # ODBIJANIE WYMAGA REFAKTORYZACJI - WIEM

######################### METODA ZMIENIAJĄCA ROZDZIELCZOŚĆ
    def resolutionChange(self):
		index  = self.ui.cmb_setResolution.currentIndex()
		self.h = self.resolutions_h[index]
		self.w = self.resolutions_w[index]
        
############################# UMIESZCZENIE OBRAZU Z KAMERY
    def imageCamera(self):
        if self.selectedCameraName == 'dummy':
            im = self.im[self.index]
            im = cv2.resize(im,(320,240))
        else:
            ret, im = self.cap.read()
        
        im = self.imageFlipMirror(im)
        
        result  = QtGui.QImage(im , 320 , 240 , QtGui.QImage.Format_RGB888).rgbSwapped()
        pixmap  = QtGui.QPixmap.fromImage(result)
        pixItem = QtGui.QGraphicsPixmapItem(pixmap)
        self.ui.graphicsScene.addItem(pixItem)
        self.ui.graphicsView.fitInView(pixItem)
        self.ui.graphicsScene.update()
        self.ui.graphicsView.show()

###################### ACTUALLY FLIP AND/OR MIRROR AN IMAGE
    def imageFlipMirror(self , im):
        if self.mirrored == 1 and self.fliped == 0:
            im[:,:,0] = cv2.flip(im[:,:,0], 1)
            im[:,:,1] = cv2.flip(im[:,:,1], 1)
            im[:,:,2] = cv2.flip(im[:,:,2], 1)
        elif self.mirrored == 0 and self.fliped == 1:
            im[:,:,0] = cv2.flip(im[:,:,0], 0)
            im[:,:,1] = cv2.flip(im[:,:,1], 0)
            im[:,:,2] = cv2.flip(im[:,:,2], 0)           
        elif self.mirrored == 1 and self.fliped == 1:
            im[:,:,0] = cv2.flip(im[:,:,0], -1)
            im[:,:,1] = cv2.flip(im[:,:,1], -1)
            im[:,:,2] = cv2.flip(im[:,:,2], -1)   
        return im
        
### FUNKCJA WŁĄCZAJĄCA/WYŁACZAJĄCA ZAAWANSOWANE USTAWIENIA
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
            x = self.cap.set(3,self.resolutions_w[resolutionIndex])
            y = self.cap.set(4,self.resolutions_h[resolutionIndex])
            
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
        
######### OBSŁUGA SUWAKÓW ZMIENIAJĄCYCH PARAMETRY DETEKCJI
    def hsbPupil_1Change(self , value):
        self.ui.lbl_pupil1.setText( str(value) )
    def hsbPupil_2Change(self , value):
        self.ui.lbl_pupil2.setText( str(value) )
    def hsbPupil_3Change(self , value):
        self.ui.lbl_pupil3.setText( str(value) )
    def hsbGlint_1Change(self , value):
        self.ui.lbl_glint1.setText( str(value) )
    def hsbGlint_2Change(self , value):
        self.ui.lbl_glint2.setText( str(value) )
    def hsbGlint_3Change(self , value):
        self.ui.lbl_glint3.setText( str(value) )
        
############## UPDATE OBRAZU W USTAWIENIACH ZAAWANSOWANYCH        
    def pupilDetectionUpdate(self, frame, gray):
        
        pupilThreshold1 = self.ui.hsb_pupil1.value()
        pupilThreshold2 = self.ui.hsb_pupil2.value()
        pupilThreshold3 = self.ui.hsb_pupil3.value()
        
        thresholds = [cv2.THRESH_OTSU , cv2.THRESH_BINARY , cv2.THRESH_TOZERO , ncv2.THRESH_TRUNC]
        
        ret, black1 = cv2.threshold(gray , pupilThreshold3 , pupilThreshold1 , thresholds[pupilThreshold2])
        
        where_pupil = pupil(black1)
        if where_pupil != None:
            black1 = cv2.cvtColor(black1, cv2.COLOR_GRAY2BGR)
            for cor in where_pupil:
                cv2.circle(black1, tuple(cor[:2]), cor[2], (0, 0, 255), 3)
                    
        cv2.imshow('pupil_detection', black1)
            
    def blackAndWhiteUpdate(self, frame, gray):
        
        glintThreshold1 = self.ui.hsb_glint1.value()
        glintThreshold2 = self.ui.hsb_glint2.value()
        glintThreshold3 = self.ui.hsb_glint3.value()
        
        where_glint = glint(gray)
        if where_glint != None:
            gray = cv2.cvtColor(gray, cv2.COLOR_GRAY2BGR)
            for cor in where_glint:
                cv2.circle(gray, tuple(cor), 10, (255, 0, 0), 3)
                
        cv2.imshow('glint_detection', gray)
        
#################################### URUCHOMIENIE PROGRAMU
    def startEyetracker(self):
        #self.im = None      # wywalenie dummy z pamięci
        #self.cap.release()  # zniszczenie strumienia z kamery
        
        # tu trzeba uruchomić program docelowy
        pass
##########################################################

if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    myapp = MyForm()
    myapp.show()
    sys.exit(app.exec_())

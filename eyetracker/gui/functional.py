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
import sys
from itertools import izip
from PyQt4 import QtCore, QtGui

from ..analysis.detect import pupil, glint
from ..analysis.processing import threshold, imageFlipMirror, mark

from ..camera.display import drawPupil, drawGlint, displayImage
from ..camera.capture import lookForCameras
from ..camera.camera import Camera

from .graphical import Ui_StartingWindow

########################################################################

class MyForm(QtGui.QMainWindow):
    def __init__(self, parent=None):
        QtGui.QWidget.__init__(self, parent)
        self.ui = Ui_StartingWindow()
        self.ui.setupUi(self)
        
        ############################# PARAMETERS INITIALIZATION
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

        self.camera = Camera(self.cameras['Camera_1'], {3 : self.w, 4 : self.h})

        self.mirrored = 0
        self.fliped = 0
        
        self.sampling = 30.0
        
        self.ui.lbl_pupil.setText(str(self.ui.hsb_pupil.value()))
        self.ui.lbl_glint.setText(str(self.ui.hsb_glint.value()))
        
        self.ui.timer.start(1000/self.sampling , self)

        ################################### EVENTS BINDINGS
        self.ui.cmb_setCamera.currentIndexChanged.connect(self.cameraChange)
        self.ui.cmb_setResolution.currentIndexChanged.connect(self.resolutionChange)
        self.ui.cmb_setAlgorithm.currentIndexChanged.connect(self.algorithmChange)
        #self.ui.btn_start.clicked.connect(self.startEyetracker)
        #self.ui.btn_settings.clicked.connect(self.startAdvancedSettings)
        self.ui.chb_flip.stateChanged.connect(self.imageFlip)
        self.ui.chb_mirror.stateChanged.connect(self.imageMirror)
        self.ui.hsb_pupil.valueChanged[int].connect(self.hsbPupil_Change)
        self.ui.hsb_glint.valueChanged[int].connect(self.hsbGlint_Change)

########################################### CLOCK TICKS
    def timerEvent(self, event):
        im = self.camera.frame()
        im = imageFlipMirror(im, self.mirrored, self.fliped)
            
        pupil = self.pupilDetectionUpdate(im)
        glint = self.blackAndWhiteUpdate(im)
            
        self.x = displayImage(pupil, 'pupil_detection')
        self.y = displayImage(glint, 'glint_detection')
        
        self.update()
        #painter = QtGui.QPainter(self)
        #painter.drawImage(QtCore.QPoint(0, 0), x)

############################## ALGORITHM CHANGING METHOD
    def algorithmChange(self):
        pass
################################ CAMERA CHANGING METHOD
    def cameraChange(self):
        self.ui.timer.stop()
        self.camera.close()
        self.selectedCameraIndex = self.ui.cmb_setCamera.currentIndex()
        self.camera = Camera(self.selectedCameraIndex-1, {3 : 320, 4 : 240})		# -1, bo numeracja jest od zera, a użytkownik widzi od 1
        self.ui.timer.start(100 , self)

######################### MIRROR METHON
    def imageMirror(self):
        if self.mirrored == 0:
            self.mirrored = 1
        else:
            self.mirrored = 0

####################### FLIP METHOD
    def imageFlip(self):
        if self.fliped == 0:
            self.fliped = 1
        else:
            self.fliped = 0

######################### RESOLUTION CHANGING METHOD
    def resolutionChange(self):
		index  = self.ui.cmb_setResolution.currentIndex()
		self.h = self.resolutions_h[index]
		self.w = self.resolutions_w[index]
        
######### CHANGING PARAMETERS ACCORDING TO SCROLLBARS
    def hsbPupil_Change(self, value):
        self.ui.lbl_pupil.setText(str(value))

    def hsbGlint_Change(self, value):
        self.ui.lbl_glint.setText(str(value))

############## UPDATE OBRAZU W USTAWIENIACH ZAAWANSOWANYCH #    
    def pupilDetectionUpdate(self, image):
        pupilThreshold = self.ui.hsb_pupil.value()
        pupil = drawPupil(image, pupilThreshold)
        return pupil
            
    def blackAndWhiteUpdate(self, image):
        glintThreshold = self.ui.hsb_glint.value()
        glint = drawGlint(image)#, glintThreshold)
        return glint

##########################################################
    def paintEvent(self, e):
        painter = QtGui.QPainter(self)
        
        result_glint  = QtGui.QImage(self.x , 320 , 240 , QtGui.QImage.Format_RGB888)
        result_pupil  = QtGui.QImage(self.y , 320 , 240 , QtGui.QImage.Format_RGB888)#.rgbSwapped()
        
        painter.drawImage(QtCore.QPoint(5, 5), result_pupil)
        painter.drawImage(QtCore.QPoint(5, 250), result_glint)

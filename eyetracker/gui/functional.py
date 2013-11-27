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
from itertools import izip
from PyQt4 import QtCore, QtGui

from ..analysis.processing import threshold, imageFlipMirror

from ..camera.display import drawPupil, drawGlint
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
        self.selectedCamera = str(self.ui.cmb_setCamera.currentText())

        self.camera = Camera(self.cameras[self.selectedCamera], 
                             {3 : self.w, 4 : self.h})

        self.mirrored = 0
        self.flipped = 0
        
        self.sampling = 30.0
        
        self.ui.lbl_pupil.setText(str(self.ui.hsb_pupil.value()))
        self.ui.lbl_glint.setText(str(self.ui.hsb_glint.value()))
        
        self.ui.timer.start(1000/self.sampling, self)

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
        im = imageFlipMirror(im, self.mirrored, self.flipped)
            
        self.pupilDetectionUpdate(im)
        self.glintDetectionUpdate(im)
            
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
        self.selectedCamera = str(self.ui.cmb_setCamera.currentText())
        self.camera = Camera(self.cameras[self.selectedCamera], 
                             {3 : 320, 4 : 240})
        self.ui.timer.start(100, self)

######################### MIRROR METHON
    def imageMirror(self):
        if self.mirrored == 0:
            self.mirrored = 1
        else:
            self.mirrored = 0

####################### FLIP METHOD
    def imageFlip(self):
        if self.flipped == 0:
            self.flipped = 1
        else:
            self.flipped = 0

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
        self.pupil = drawPupil(image, pupilThreshold)
            
    def glintDetectionUpdate(self, image):
        glintThreshold = self.ui.hsb_glint.value()
        self.glint = drawGlint(image)#, glintThreshold

##########################################################
    def paintEvent(self, e):
        painter = QtGui.QPainter(self)
        
        result_glint = QtGui.QImage(self.glint, 320, 240, QtGui.QImage.Format_RGB888)
        result_pupil = QtGui.QImage(self.pupil, 320, 240, QtGui.QImage.Format_RGB888)#.rgbSwapped()
        
        painter.drawImage(QtCore.QPoint(5, 5), result_pupil)
        painter.drawImage(QtCore.QPoint(5, 250), result_glint)

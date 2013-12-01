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

from ..analysis.processing import imageFlipMirror, runningAverage

from ..camera.display import drawPupil, drawGlint
from ..camera.capture import lookForCameras
from ..camera.camera import Camera

from .graphical import Ui_StartingWindow

import os

########################################################################

class MyForm(QtGui.QMainWindow):
    '''
    Class governing the functional part of the default graphical user interface.

    Parameters:
    -----------
    No parameters needed.

    Defines:
    --------
    self.cameras - list containing all camera devices connected to the computer,
    self.algorithms - list of all implemented algorithms for eyetracker programm,
    self.resolutions - list of all possible image resolutions for eyetracer to operate on,
    self.w - selected width of an image to start an eyetracker,
    self.h - selected height of an image to start an eyetracker,
    self.selectedCamera - selected camera name as chosen by the user (default is a name of the first avalaible device),
    self.timer_on - flag showing wether timer is ticking or not,
    
    self.config - dictionary with all configuration variables,
    self.configFileName - path to the configuration file,
    
    self.alpha - control parameter of the running average, it describes
    how fast previous images would be forgotten, 1 - no average,
    0 - never forget anything.
    
    self.ui - class encapsulating graphical part of an interface, as described
    in eyetracker/gui/graphical.py file,
    
    self.camera - class encapsulating a camera device as described in
    eyetracker/camera/camera.py.
    
    Returns:
    --------
    Class does not return anything.
    '''
    
    def __init__(self, parent=None):
        QtGui.QWidget.__init__(self, parent)
        self.ui = Ui_StartingWindow()
        self.ui.setupUi(self)
        
        ############################# PARAMETERS INITIALIZATION
        self.cameras = lookForCameras()
        for i in self.cameras.iterkeys():
            self.ui.cmb_setCamera.addItem(i)
        
        self.algorithms = ['NESW' , 'Raw output']
        for algorithm in self.algorithms:
            self.ui.cmb_setAlgorithm.addItem(algorithm)
        
        self.resolutions_w = [160,320,640,1280]
        self.resolutions_h = [120,240,480,720]
        for w, h in izip(self.resolutions_w, self.resolutions_h):
            self.ui.cmb_setResolution.addItem(''.join([str(w), 'x', str(h)]))
        
        
        self.loadSettings()      # this will create self.config containing all necessary settings
        self.setWidgetsState()   # this will set up state of widgets according to loaded settings

        self.w = 320
        self.h = 240
        
        self.selectedCamera = str(self.ui.cmb_setCamera.currentText())

        try:                                                                                # THIS IS BAD - I WILL WORK ON IT LATER - Tomek.
            self.camera  = Camera(self.cameras['Camera_1'], {3 : self.w, 4 : self.h})
            #self.average = float32(self.camera.frame())
        except KeyError:
            print 'No camera device detected.'
        
        self.ui.timer.start(1000/self.config['Sampling'], self)
        self.timer_on = False # it starts above, but timer_on says if it already ticked at least once.
        

        ################################### EVENTS BINDINGS
        self.ui.cmb_setCamera.currentIndexChanged.connect(self.cameraChange)
        self.ui.cmb_setResolution.currentIndexChanged.connect(self.resolutionChange)
        self.ui.cmb_setAlgorithm.currentIndexChanged.connect(self.algorithmChange)
        self.ui.btn_start.clicked.connect(self.runEyetracker)
        self.ui.btn_clear.clicked.connect(self.clearSettings)
        self.ui.btn_save.clicked.connect(self.saveSettings)
        self.ui.chb_flip.stateChanged.connect(self.imageFlip)
        self.ui.chb_mirror.stateChanged.connect(self.imageMirror)
        self.ui.hsb_pupil.valueChanged[int].connect(self.hsbPupil_Change)
        self.ui.hsb_glint.valueChanged[int].connect(self.hsbGlint_Change)

########################################### CLOCK TICKS
    def timerEvent(self, event):
        '''
        Function controlling the main flow of this gui. It fires periodically
        (sampling rate), grabs frames from a camera, starts image processing
        and displays changes in the gui.
        
        Parameters:
        -----------
        event - standard event handler as described in QT4 documentation.
        
        Returns:
        --------
        Function does not return anything.
        '''
        im = self.camera.frame()
        
        im = runningAverage(im , im , self.config['Alpha'])
        
        im = imageFlipMirror(im, self.config['Mirrored'], self.config['Fliped'])

        self.pupilUpdate(im)
        self.glintUpdate(im)
        
        if self.timer_on == False:
            self.timer_on = True
        
        self.update()

####################### SET DEFAULT CONFIG
    def setDefaultSettings(self):
        '''
        Function sets all gui parameters to its default values.
        
        Parameters:
        -----------
        No parameters needed.
        
        Returns:
        --------
        Function does not return anything.
        '''
        
        self.config['Mirrored']        = 0
        self.config['Fliped']          = 0
        self.config['Alpha']           = 0.1
        self.config['ResolutionIndex'] = 1
        self.config['PupilBar']        = 0
        self.config['GlintBar']        = 0
        self.config['Sampling']        = 30.0
        self.config['AlgorithmIndex']  = 0

##################### SET STATE OF WIDGETS 
    def setWidgetsState(self):
        '''
        Function sets state of gui widgets according to self.config variable.
        
        Parameters:
        -----------
        No parameters needed.
        
        Returns:
        --------
        Function does not return anything.
        '''
        
        warningFlag = False
        
        try:
            self.ui.cmb_setAlgorithm.setCurrentIndex(self.config['AlgorithmIndex'] )
        except KeyError:
            self.config['AlgorithmIndex']  = 0
            self.ui.cmb_setAlgorithm.setCurrentIndex(0)
            print 'No AlgorithmIndex in configuration file present -- loading default value.'
            warningFlag = True
            
        try:
            self.ui.cmb_setResolution.setCurrentIndex(self.config['ResolutionIndex'] )       
        except KeyError:
            self.config['ResolutionIndex']  = 0
            self.ui.cmb_setResolution.setCurrentIndex(0)
            print 'No ResolutionIndex in configuration file present -- loading default value.'
            warningFlag = True
            
        try:
            self.ui.hsb_pupil.setValue(self.config['PupilBar'])
            self.ui.hsb_glint.setValue(self.config['GlintBar'])
        except KeyError:
            self.config['PupilBar'] = 0
            self.config['GlintBar'] = 0
            self.ui.hsb_pupil.setValue(0)
            self.ui.hsb_glint.setValue(0)
            print 'Either GlintBar or PupilBar (or both) not present in configuration file -- loading default values.'
            warningFlag = True
                    
        self.ui.lbl_pupil.setText(str(self.ui.hsb_pupil.value()))
        self.ui.lbl_glint.setText(str(self.ui.hsb_glint.value()))

        try:
            if self.config['Mirrored'] == 1:
                self.ui.chb_mirror.toggle()
            if self.config['Fliped'] == 1:
                self.ui.chb_flip.toggle()
        except KeyError:
            self.config['Mirrored'] == 0
            self.config['Fliped'] == 0
            print 'Either Mirrored or Fliped (or both) not present in configuration file -- loading default values.'
            warningFlag = True
        
        if warningFlag == True:
            print 'Some variables were not present in configuration file. Saving current settings should solve this issue.'

############################# CLEAR CONFIG
    def clearSettings(self):
        '''
        Function clears all parameters saved previously in a config file
        and set gui to a default state.
        
        Parameters:
        -----------
        No parameters needed.
        
        Returns:
        --------
        Function does not return anything.
        '''
        
        self.setDefaultSettings()
        self.saveSettings()
        self.setWidgetsState()

############################## SAVE CONFIG
    def saveSettings(self):
        '''
        Saves parameters of a programm to a specified file on disc.
        
        Parameters:
        -----------
        No parameters needed.
        
        Returns:
        --------
        Function does not return anything.    
        '''
        
        with open(self.configFileName , 'w') as f:
            
            for key in self.config.keys():
                stringToWrite = key + ' ' + str(self.config[key]) + '\n'
                f.write(stringToWrite)
            
            #f.write('Fliped {}\n'.format(self.flipped) ) # this is here for historical reasons - Tomek

############################## LOAD CONFIG
    def loadSettings(self):
        '''
        Loads parameters of a programm from a specified file on disc. If
        file is not present, default parameters would be loaded.
        
        Parameters:
        -----------
        No parameters needed.
        
        Returns:
        --------
        This function does not return anything.
        '''
        
        self.config = {}
        
        self.configFileName = os.path.expanduser("~") + '/.config/eyetracker-ng/configFile.txt'
        
        directory = self.configFileName[0 : self.configFileName.find('configFile')]
        if not os.path.exists(directory):
            os.makedirs(directory)
        
        try:
            with open(self.configFileName , 'r') as configFile:
                for line in configFile:
                    tmp = line.split()
                    try:
                        self.config[str(tmp[0])] = int(tmp[1])
                    except ValueError:
                        self.config[str(tmp[0])] = float(tmp[1])
                    
        except IOError:
            # No config file yet -- using defaults
            self.setDefaultSettings()

############################## ALGORITHM CHANGING METHOD
    def algorithmChange(self):
        '''
        Function changing algorithm for eyetracker.
        
        Parameters:
        -----------
        No parameters needed.
        
        Returns:
        --------
        Function does not return anything.
        '''
        
        ind = self.ui.cmb_setAlgorithm.currentIndex()
        
        self.config['AlgorithmIndex']  = ind
        
################################ CAMERA CHANGING METHOD
    def cameraChange(self):
        '''
        Function changing camera between avalaible devices.
        
        Parameters:
        -----------
        No parameters needed.
        
        Returns:
        --------
        Function does not return anything.            
        '''
        
        self.ui.timer.stop()
        self.camera.close()
        self.selectedCamera = str(self.ui.cmb_setCamera.currentText())
        self.camera = Camera(self.cameras[self.selectedCamera], 
                             {3 : self.w, 4 : self.h})
        self.ui.timer.start(100, self)

######################### MIRROR METHON
    def imageMirror(self):
        '''
        Function sets a variable telling the gui to mirror incomming frames from a camera.
        
        Parameters:
        -----------
        No parameters needed.
        
        Returns:
        --------
        Function does not return anything.          
        '''
        
        if self.config['Mirrored'] == 0:
            self.config['Mirrored'] = 1
        else:
            self.config['Mirrored'] = 0

####################### FLIP METHOD
    def imageFlip(self):
        '''
        Function sets a variable telling the gui to flip incomming frames from a camera.
        
        Parameters:
        -----------
        No parameters needed.
        
        Returns:
        --------
        Function does not return anything.          
        '''        
        
        if self.config['Fliped'] == 0:
            self.config['Fliped'] = 1
        else:
            self.config['Fliped'] = 0

######################### RESOLUTION CHANGING METHOD
    def resolutionChange(self):
        '''
        Function sets a chosen resolution of a camera. It does not change
        an image displayed in the gui, but sets variable for eyetracker programm.
        
        Parameters:
        -----------
        No parameters needed.
        
        Returns:
        --------
        Function does not return anything.          
        '''
        
        ind = self.ui.cmb_setResolution.currentIndex()
        
        self.config['ResolutionIndex']  = ind
        
######### CHANGING PARAMETERS ACCORDING TO SCROLLBARS
    def hsbPupil_Change(self, value):
        '''
        Function sets a text in a gui according to the possition of a slider.
        
        Parameters:
        -----------
        value - value to be displayed in an apriopriate label
        
        Returns:
        --------
        Function does not return anything.          
        '''
        
        self.ui.lbl_pupil.setText(str(value))
        self.config['PupilBar'] = value

    def hsbGlint_Change(self, value):
        '''
        Function sets a text in a gui according to the possition of a slider.
        
        Parameters:
        -----------
        value - value to be displayed in an apriopriate label
        
        Returns:
        --------
        Function does not return anything.          
        '''
        
        self.ui.lbl_glint.setText(str(value))
        self.config['GlintBar'] = value

############## UPDATE OBRAZU
    def pupilUpdate(self, image):
        '''

        Parameters:
        -----------
        image - numpy array depicting an image on which pupil should be find and marked.
        
        Returns:
        --------
        Function does not return anything.          
        '''
        
        pupilThreshold = self.ui.hsb_pupil.value()
        self.pupil = drawPupil(image, pupilThreshold)
            
    def glintUpdate(self, image):
        '''
        
        Parameters:
        -----------
        image - numpy array depicting an image on which glints should be find and marked.
        
        Returns:
        --------
        Function does not return anything.          
        '''
        
        glintThreshold = self.ui.hsb_glint.value()
        self.glint = drawGlint(image)#, glintThreshold

##########################################################
    def paintEvent(self, event):
        '''
        
        Parameters:
        -----------
        event - standard event handler as described in QT4 documentation.
        
        Returns:
        --------
        Function does not return anything.          
        '''
        
        painter = QtGui.QPainter(self)
        
        if self.timer_on:
            result_pupil = QtGui.QImage(self.pupil, self.w, self.h, QtGui.QImage.Format_RGB888)   # I will work on color convention here - Tomek
            result_glint = QtGui.QImage(self.glint, self.w, self.h, QtGui.QImage.Format_RGB888)   # same here
        
            painter.drawImage(QtCore.QPoint(5, 35), result_pupil)
            painter.drawImage(QtCore.QPoint(5, 300), result_glint)

##########################################################
    def runEyetracker(self):
        '''
        Starts eyetracker with parameters picked in gui.
        
        Parameters:
        -----------
        No parameters needed.
        
        Returns:
        --------
        Function does not return anything.
        
        '''
        
        # This is here for informational reasons, I will remove it, when I'm done - Tomek
        #self.h = self.resolutions_h[ind]
        #self.w = self.resolutions_w[ind]
        
        pass

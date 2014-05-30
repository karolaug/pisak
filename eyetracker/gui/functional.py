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


from itertools import izip
from PyQt4 import QtCore, QtGui

import numpy as np

from ..analysis.processing import imageFlipMirror, runningAverage

from ..camera.display import drawPupil, drawGlint
from ..camera.camera import lookForCameras
from ..camera.camera import Camera
from eyetracker.analysis.processing import gray2bgr, bgr2gray, mark, threshold, thresholds
from .graphical import Ui_StartingWindow

import os
#from functools import partial
from scipy.optimize import curve_fit

import subprocess

import pygame,time
from PIL import Image

cRED = pygame.Color(255,0,0)
cBLUE = pygame.Color(0,0,255)
cGREEN = pygame.Color(0, 255, 0)
cYELLOW = pygame.Color(255, 255, 0)
cBLACK = pygame.Color(0,0,0)
cWHITE = pygame.Color(255,255,255)



def f_for_fitting((x,y) , a , b , c , d , e , f):
    return a*x**2 + b*x + c*y**2 + d*y + e*x*y + f



def find_pup(where_glint,where_pupil):
    """It finds right pupil values from glint *where_glint* 
    and pupils positions *where_pupil*"""
    xsr,ysr=np.mean(where_glint,axis=0)
    ls=[]
    try:
        for wsp in where_pupil:
            r=np.sqrt((xsr-wsp[0])**2+(ysr-wsp[1])**2)
            ls.append([r,wsp[0],wsp[1]])
    except TypeError:
        return np.array([np.NaN,np.NaN])
    return np.array(min(ls)[1:])

def eye_calibr_params(points):
    """Returns parameters needed to scale eyetracker cursor.
    *points* is a vector of data points from callibration session"""
    points = np.asarray(points)
    xmax,ymax = np.max(points,axis=0)
    xmean,ymean = np.mean(points,axis=0)
    xmin,ymin = np.min(points,axis=0)
    return xmin, xmax-xmin, ymin, ymax-ymin, xmean, ymean

class MyTextViewer(QtGui.QMainWindow):
    def __init__(self, parent=None):
        QtGui.QWidget.__init__(self, parent)
        self.ui = Ui_MusicPlayerWindow()
        self.ui.setupUi(self)
        
    def closeEvent(self, event):
        event.accept()
        

class MyForm(QtGui.QMainWindow):
    ''' Functional part of GUI interface.

    Class governing the functional part of the default graphical user interface.

    Defines
    -------
    self.cameras : list
        all camera devices connected to the computer,
    self.algorithms : list
        all implemented algorithms for eyetracker programm,
    self.resolutions : list
        all possible image resolutions for eyetracer to operate on,
    self.w : int
        selected width of an image to start an eyetracker,
    self.h : int
        selected height of an image to start an eyetracker,
    self.selectedCamera : string
        selected camera name as chosen by the user (default is a name of the first avalaible device),
    self.timer_on : boolean
        flag showing wether timer is ticking or not,
    self.config : path
        dictionary with all configuration variables,
    self.configFileName : path
        path to the configuration file,
    self.ui : class
        encapsulating graphical part of an interface, as described
        in eyetracker/gui/graphical.py file,
    self.camera : class
        encapsulating a camera device as described in
        eyetracker/camera/camera.py.
    '''

    def __init__(self, parent=None):
        QtGui.QWidget.__init__(self, parent)
        self.ui = Ui_StartingWindow()
        self.ui.setupUi(self)
        self.defaults                    = {}
        self.defaults['Mirrored']        = 0
        self.defaults['Fliped']          = 0
        self.defaults['Alpha']           = 0.8
        self.defaults['ResolutionIndex'] = 1
        self.defaults['PupilBar']        = 0
        self.defaults['NumberOfGlints']  = 2
        self.defaults['NumberOfPupils']  = 1
        self.defaults['Sampling']        = 30.0
        self.defaults['AlgorithmIndex']  = 0
        self.defaults['PupilStackDeph']  = 100.
        self.defaults['DecisionStackDeph'] = 10.


        self.procHandler = subprocess.Popen(['python3' , 'cursor_app.py'] , stdin = subprocess.PIPE)

        self.N_b = 10
        self.buf_pup = np.zeros((self.N_b,2))      
        self.initializeFlags()
        
        
        
        
        self.screen_x_list = []
        self.screen_y_list = []
        
        
        
        #pygame.init()
        
        self.cameras = lookForCameras()
        for i in self.cameras.iterkeys():
            self.ui.cmb_setCamera.addItem(i)
            
        self.algorithms = {}
        self.algorithms['Raw output']   = self.module_raw
        #self.algorithms['Calibration']  = self.module_calibration
        #self.algorithms['Picture viewer']  = self.module_picture
        self.algorithms['After cal']  = self.module_after_cal
        self.algorithms['New Calibr Test'] = self.module_calibration_rectangle
        
        #self.ui.cmb_setAlgorithm.setCurrentIndex(self.config['AlgorithmIndex'] )
        
        print self.algorithms.keys()
        
        for algorithm in self.algorithms.keys():
            print algorithm
            self.ui.cmb_setAlgorithm.addItem(algorithm)
            
        
        self.resolutions = [(160,120),(320,240),(640,480),(1280,720)]
        for w,h in self.resolutions:
            self.ui.cmb_setResolution.addItem(''.join([str(w), 'x', str(h)]))
            
        self.loadSettings()
        self.setWidgetsState()
        
        self.to_calibr_rect = []
        self.w = 640#320
        self.h = 480#240

        self.selectedCamera = str(self.ui.cmb_setCamera.currentText())

        try:
            self.camera  = Camera(self.cameras['Camera_1'], {3 : self.w, 4 : self.h})
        except KeyError:
            print 'No camera device detected.'

        self.glints_stack = np.zeros([6,3])
        self.pupils_stack = np.zeros([6,3])
        #print self.pupils_stack.shape
        
        self.pupilPositionsStack = []
        self.decisionPupilPositionsStack = []

        self.ui.timer.start(1000/self.config['Sampling'], self)
        self.timer_on = False

        self.ui.cmb_setCamera.currentIndexChanged.connect(self.cameraChange)
        self.ui.cmb_setResolution.currentIndexChanged.connect(self.resolutionChange)
        self.ui.cmb_setAlgorithm.currentIndexChanged.connect(self.algorithmChange)
        self.ui.btn_start.clicked.connect(self.startButtonClicked)
        self.ui.btn_clear.clicked.connect(self.clearSettings)
        self.ui.btn_save.clicked.connect(self.saveSettings)
        self.ui.chb_flip.stateChanged.connect(self.imageFlip)
        self.ui.chb_mirror.stateChanged.connect(self.imageMirror)
        self.ui.hsb_pupil.valueChanged[int].connect(self.hsbPupil_Change)
        self.ui.hsb_pupil2.valueChanged[int].connect(self.hsbPupilNumber_Change)
        self.ui.hsb_glint.valueChanged[int].connect(self.hsbGlint_Change)
        self.ui.led_alpha.editingFinished.connect(self.alphaChange)
        self.ui.led_pupilStackDeph.editingFinished.connect(self.pupilStackDephChange)
        self.ui.led_decisionStackDeph.editingFinished.connect(self.decisionStackDephChange)
        
        #for buttonNo in range(1,7):
        #    self.ui.keys[buttonNo].clicked.connect(partial(self.keyButtonClicked, clickedButtonNo = buttonNo))

    def timerEvent(self, event):
        ''' Function controlling the main flow of this gui.

        Function fires periodically (sampling rate),
        grabs frames from a camera, starts image processing
        and displays changes in the gui.

        Parameters
        -----------
        event : object
            standard event handler as described in QT4 documentation.
       '''
        im = self.camera.frame()
        im = imageFlipMirror(im, self.config['Mirrored'], self.config['Fliped'])

        if self.timer_on == False:
            self.im = im
            self.timer_on = True

        #self.im = runningAverage(im, self.im, self.config['Alpha'])
        self.im = im
        self.pupilUpdate(self.im)
        self.glintUpdate(self.im)
        
        try:
            mx,my =  self.mean_pupfinder()
            #mark(self.pupil, np.array([mx,my]),radius=20, color='green')
            mark(self.glint, np.array([mx,my]),radius=20, color='green')
        except TypeError:
            mx,my = [0,0]
        #print mx, my
        
        self.runEyetracker()
        
        self.update()
        
    def initializeFlags(self):
        #self.musicPlayerFlag = 0
        self.startFlag       = 0
        
        #self.textViewerFlag  = 0
        self.pictureViewerFlag  = 0
    
        self.spellerFlag    = 0
        #self.spellerLvl     = 0
        self.spellerCalibrationFlag = 0
        self.afterFlag = 0

    def setDefaultSettings(self):
        ''' Set GUI defaul configuration.

        Function sets all gui parameters to its default values.

        '''
        self.config['Mirrored']        = self.defaults['Mirrored']
        self.config['Fliped']          = self.defaults['Fliped']
        self.config['Alpha']           = self.defaults['Alpha']
        self.config['ResolutionIndex'] = self.defaults['ResolutionIndex']
        self.config['PupilBar']        = self.defaults['PupilBar']
        self.config['NumberOfGlints']  = self.defaults['NumberOfGlints']
        self.config['NumberOfPupils']  = self.defaults['NumberOfPupils']
        self.config['Sampling']        = self.defaults['Sampling']
        self.config['AlgorithmIndex']  = self.defaults['AlgorithmIndex']
        self.config['PupilStackDeph']    = self.defaults['PupilStackDeph']
        self.config['DecisionStackDeph']    = self.defaults['DecisionStackDeph']

    def setWidgetsState(self):
        ''' Set state of gui widgets according to self.config variable.
        '''
        warningFlag = False
        
        try:
            self.ui.cmb_setAlgorithm.setCurrentIndex(self.config['AlgorithmIndex'] )
        except KeyError:
            self.config['AlgorithmIndex']  = self.defaults['AlgorithmIndex']
            self.ui.cmb_setAlgorithm.setCurrentIndex(self.defaults['AlgorithmIndex'])
            print 'No AlgorithmIndex in configuration file present -- loading default value.'
            warningFlag = True
            
        try:
            self.ui.cmb_setResolution.setCurrentIndex(self.config['ResolutionIndex'] )       
        except KeyError:
            self.config['ResolutionIndex']  = self.defaults['ResolutionIndex']
            self.ui.cmb_setResolution.setCurrentIndex(self.defaults['ResolutionIndex'])
            print 'No ResolutionIndex in configuration file present -- loading default value.'
            warningFlag = True
            
        try:
            self.ui.hsb_pupil.setValue(self.config['PupilBar'])
            self.ui.hsb_pupil2.setValue(self.config['NumberOfPupils'])
            self.ui.hsb_glint.setValue(self.config['NumberOfGlints'])
        except KeyError:
            self.config['PupilBar'] = self.defaults['PupilBar']
            self.config['NumberOfGlints'] = self.defaults['NumberOfGlints']
            self.config['NumberOfPupils'] = self.defaults['NumberOfPupils']
            self.ui.hsb_pupil.setValue(self.defaults['PupilBar'])
            self.ui.hsb_glint.setValue(self.defaults['NumberOfGlints'])
            self.ui.hsb_pupil2.setValue(self.defaults['NumberOfPupils'])
            print 'Either NumberOfGlints, NumberOfPupils or PupilBar (or any combination of them) not present in configuration file -- loading default values.'
            warningFlag = True
                    
        self.ui.lbl_pupil.setText(str(self.ui.hsb_pupil.value()))
        self.ui.lbl_pupil2.setText(str(self.ui.hsb_pupil2.value()))
        self.ui.lbl_glint.setText(str(self.ui.hsb_glint.value()))

        try:
            if self.config['Mirrored'] == 1:
                self.ui.chb_mirror.toggle()
            if self.config['Fliped'] == 1:
                self.ui.chb_flip.toggle()
        except KeyError:
            self.config['Mirrored'] == self.defaults['Mirrored']
            self.config['Fliped'] == self.defaults['Fliped']
            
            if self.config['Mirrored'] == 1:
                self.ui.chb_mirror.toggle()
            if self.config['Fliped'] == 1:
                self.ui.chb_flip.toggle()

            print 'Either Mirrored or Fliped (or both) not present in configuration file -- loading default values.'
            warningFlag = True
            
        try:
            self.ui.led_alpha.setText(str(self.config['Alpha']))
        except KeyError:
            self.config['Alpha'] = self.defaults['Alpha']
            self.ui.led_alpha.setText(str(self.config['Alpha']))
            print 'Parameter for alpha smoothing not present in configuration file -- loading default values.'
            warningFlag = True
        
        try:
            self.ui.led_pupilStackDeph.setText(str(self.config['PupilStackDeph']))
        except KeyError:
            self.config['PupilStackDeph'] = self.defaults['PupilStackDeph']
            self.ui.led_pupilStackDeph.setText(str(self.config['PupilStackDeph']))
            print 'PupilStackDeph parameter not present in configuration file -- loading default values.'
            warningFlag = True
            
        try:
            self.ui.led_decisionStackDeph.setText(str(self.config['DecisionStackDeph']))
        except KeyError:
            self.config['DecisionStackDeph'] = self.defaults['DecisionStackDeph']
            self.ui.led_decisionStackDeph.setText(str(self.config['DecisionStackDeph']))
            print 'DecisionStackDeph parameter not present in configuration file -- loading default values.'
            warningFlag = True
            
        if warningFlag == True:
            print 'Some variables were not present in configuration file. Saving current settings should solve this issue.'

    def clearSettings(self):
        ''' Restore GUI default configuration.

        Function clears all parameters saved previously in a config file
        and set gui to a default state.
        '''

        self.setDefaultSettings()
        self.saveSettings()
        self.setWidgetsState()

    def saveSettings(self):
        ''' Save GUI settings.

        Saves GUI parameters specified file.
        '''

        with open(self.configFileName , 'w') as f:

            for key in self.config.keys():
                stringToWrite = key + ' ' + str(self.config[key]) + '\n'
                f.write(stringToWrite)

    def loadSettings(self):
        ''' Load GUI settings from file.

        Loads parameters of a programm from a specified file. If
        file is not present, default parameters would be loaded.
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
            print 'No config file yet -- using defaults'
            self.setDefaultSettings()

    def algorithmChange(self):
        ''' Change eyetracker algorithm.

        Function changing algorithm for eyetracker.
        '''

        ind = self.ui.cmb_setAlgorithm.currentIndex()

        self.config['AlgorithmIndex']  = ind

    def cameraChange(self):
        ''' Change camera between avalaible devices.
        '''

        self.ui.timer.stop()
        self.camera.close()
        self.glints_stack = np.zeros([self.config['Alpha'],3])
        self.pupils_stack = np.zeros([self.config['Alpha'],3])
        self.selectedCamera = str(self.ui.cmb_setCamera.currentText())
        self.camera = Camera(self.cameras[self.selectedCamera], 
                             {3 : self.w, 4 : self.h})
        self.ui.timer.start(1000/self.config['Sampling'], self)

    def imageMirror(self):
        ''' Set a variable telling the gui to mirror incomming frames from a camera.
        '''

        if self.config['Mirrored'] == 0:
            self.config['Mirrored'] = 1
        else:
            self.config['Mirrored'] = 0
            
        #self.glints_stack = np.zeros([self.config['Alpha'],3])
        #self.pupils_stack = np.zeros([self.config['Alpha'],3])

    def imageFlip(self):
        ''' Set a variable telling the gui to flip incomming frames from a camera.
        '''

        if self.config['Fliped'] == 0:
            self.config['Fliped'] = 1
        else:
            self.config['Fliped'] = 0
            
        #self.glints_stack = np.zeros([self.config['Alpha'],3])
        #self.pupils_stack = np.zeros([self.config['Alpha'],3])

    def resolutionChange(self):
        ''' Set a chosen resolution of a camera.

        It does not change an image displayed in the gui,
        but sets variable for eyetracker programm.
        '''

        ind = self.ui.cmb_setResolution.currentIndex()

        self.config['ResolutionIndex']  = ind
        
    def alphaChange(self):
        '''
        Set a chosen alpha parameter for smoothing purposes.
        
        Alpha is a control parameter of the running average. It describes
        how many previous glint and pupil positions should be averaged.
        By arbitrary alpha should not exceed 10 and could not be a negative
        number.
        
        value : string
            value to be assigned to alpha parameter. It would be converted
            to np.float32
        '''
        try:
            alpha = float(self.ui.led_alpha.text())
        except ValueError:
            self.ui.led_alpha.setText( str(self.config['Alpha']) )
            print 'Alpha should be a floating point number!'
            return
        
        if alpha < 0. or alpha > 1.:
            self.ui.led_alpha.setText( str(self.config['Alpha']) )
            print 'Alpha should be between 0.0 and 1.0!'
        else:
            self.config['Alpha'] = alpha
            
        self.glints_stack = np.zeros([self.config['Alpha'],3])
        self.pupils_stack = np.zeros([self.config['Alpha'],3])

    def pupilStackDephChange(self):
        '''
        Set a chosen pupilStackDeph parameter for some purposes.
        
        What is pupilStackDeph --> Sasha
        
        value : string
            value to be assigned to pupilStackDeph parameter. It would be converted
            to np.float32
        '''
        try:
            pupilStackDeph = float(self.ui.led_pupilStackDeph.text())
        except ValueError:
            self.ui.led_pupilStackDeph.setText( str(1) )                          # for now...
            #self.ui.led_pupilStackDeph.setText( str(self.config['Alpha']) )      # in future
            print 'PupilStackDeph should be a floating point number!'
            return
        
        if pupilStackDeph < 10. or pupilStackDeph > 300.:
            self.ui.led_pupilStackDeph.setText( str(100.) )                          # for now...
            #self.ui.led_alpha.setText( str(self.config['Alpha']) )             # in future
            print 'PupilStackDeph should be between 10.0 and 300.0!'
        else:
            #self.config['PupilStackDeph'] = alpha                                # in future
            pass
            
    def decisionStackDephChange(self):
        '''
        Set a chosen decisionStackDeph parameter for some purposes.
        
        What is decisionStackDeph --> Sasha
        
        value : string
            value to be assigned to decisionStackDeph parameter. It would be converted
            to np.float32
        '''
        try:
            decisionStackDeph = float(self.ui.led_decisionStackDeph.text())
        except ValueError:
            self.ui.led_decisionStackDeph.setText( str(1) )                          # for now...
            #self.ui.led_decisionStackDeph.setText( str(self.config['Alpha']) )      # in future
            print 'PupilStackDeph should be a floating point number!'
            return
        
        if decisionStackDeph < 0. or decisionStackDeph > 30.:
            self.ui.led_decisionStackDeph.setText( str(6) )                          # for now...
            #self.ui.led_alpha.setText( str(self.config['Alpha']) )             # in future
            print 'DecisionStackDeph should be between 0.0 and 10.0!'
        else:
            #self.config['DecisionStackDeph'] = alpha                                # in future
            pass

    def hsbPupil_Change(self, value):
        ''' Set a text in a gui according to the possition of a slider.

        Parameters
        -----------
        value : int
            value to be displayed in an apriopriate label
        '''

        self.ui.lbl_pupil.setText(str(value))
        self.config['PupilBar'] = value

    def hsbPupilNumber_Change(self, value):
        ''' Set a text in a gui according to the possition of a slider.

        Parameters
        -----------
        value : int
            value to be displayed in an apriopriate label
        '''

        self.ui.lbl_pupil2.setText(str(value))
        self.config['NumberOfPupils'] = value

    def hsbGlint_Change(self, value):
        ''' Set a text in a gui according to the possition of a slider.

        Parameters
        -----------
        value : int
            value to be displayed in an apriopriate label
        '''

        self.ui.lbl_glint.setText(str(value))
        self.config['NumberOfGlints'] = value

    def pupilUpdate(self, image):
        '''

        Parameters
        -----------
        image : np.array
            image on which pupil should be find and marked.

        '''
        self.pupil , self.where_pupil , self.pupils_stack = drawPupil(image , self.config['PupilBar'] , self.pupils_stack , self.config['NumberOfPupils'])
        

    def glintUpdate(self, image):
        '''

        Parameters
        -----------
        image : np.array
            image on which glints should be find and marked.
        '''
        self.glint , self.where_glint , self.glints_stack = drawGlint(image , self.where_pupil , self.config['NumberOfGlints'] , self.glints_stack)

    def paintEvent(self, event):
        '''

        Parameters
        -----------
        event : object
            standard event handler as described in QT4 documentation.

        '''
        painter = QtGui.QPainter(self)

        if self.timer_on:
            result_pupil = QtGui.QImage(self.pupil, self.w, self.h, QtGui.QImage.Format_RGB888).rgbSwapped()
            result_glint = QtGui.QImage(self.glint, self.w, self.h, QtGui.QImage.Format_RGB888).rgbSwapped()

            painter.drawImage(QtCore.QPoint(40, 40), result_pupil)
            painter.drawImage(QtCore.QPoint(720, 40), result_glint)

#    def closeEvent(self, event):
#        '''
#
#        Parameters
#        -----------
#        event : object
#            standard event handler as described in QT4 documentation.
#
#        '''
        
    def startButtonClicked(self):
        ''' Handles the behavior of the start/stop button, based on parameters picked from gui.
        '''
        
        if self.startFlag == 0:
            self.startFlag = 1
            self.ui.btn_start.setText('Stop')
        else:
            self.startFlag = 0
            #self.pupilPositionsStack = []
            self.ui.btn_start.setText('Start')
            
            
            
    def runEyetracker(self):
        ''' Starts eyetracker with parameters picked from gui.
        '''
        if self.startFlag == 1:
            self.ui.btn_start.setText('Start')
            self.algorithms[ str(self.ui.cmb_setAlgorithm.currentText()) ]()
        else:
            pass

    def mean_pupfinder(self):
        """It averages *N_b* positions of the best finded pupil"""
        fp=find_pup(self.where_glint,self.where_pupil)
        if not np.any(np.isnan(fp)):
            self.buf_pup[:self.N_b-1,:] = self.buf_pup[1:,:]
            self.buf_pup[self.N_b-1,:] = fp
        else:
            fp = None 
        return np.mean(self.buf_pup,axis=0).astype(np.uint)
        #return fp

       
    def module_raw(self):
        #if self.startFlag == 1:
        print 'Pupil coordinates: {}.'.format(self.where_pupil)
        print 'Glint coordinates: {}.'.format(self.where_glint)
        
    def module_picture(self):
        pass
    
    def module_after_cal(self):
        if self.afterFlag == 0 :
            self.resize(0,0)
            scr_x = self.ui.trueScreen.width()
            scr_y = self.ui.trueScreen.height()
            
            pygame.init()
            self.screen = pygame.display.set_mode((scr_x,scr_y))
            self.afterFlag=1

        if self.spellerFlag == 0 and self.startFlag == 1 and self.spellerCalibrationFlag==1 and self.afterFlag==1:
            #print self.position()
            
            data2send = self.position()
            
            ### TO TUTAJ
            self.procHandler.stdin.write(data2send)
            
            
            
            
            
            
#             pygame.init()
#             keys=pygame.key.get_pressed()
#             for event in pygame.event.get():
#                 if event.type == pygame.QUIT:
#                     pygame.quit()
#                     break
#                 if keys[ord('q')]:
#                     pygame.quit()
#                     break
#                 if keys[ord('z')]:
#                     self.screen.fill(cBLACK)
#             mx,my =  self.position()
#             pygame.draw.circle(self.screen, cRED, (mx,my), 3)
#             pygame.display.flip()

    def module_calibration(self):
        if self.spellerFlag == 0 and self.startFlag == 1:
            
            self.calibr_length = 12
            self.resize(0,0)
            
            pygame.init()
            self.screen = pygame.display.set_mode((self.w,self.h),pygame.FULLSCREEN)
            pygame.display.set_caption('calibration')
            self.cal_positions = []
            self.t0 = time.time()
            self.t_arr = time.time()
            
            self.rectangle = [(self.screen, cRED, (0,0,40,self.w)),
                    (self.screen, cRED, (0,0,self.w,40)),
                    (self.screen, cRED, (self.w-40,0,40,self.h)),
                    (self.screen, cRED, (0,self.h-40,self.w,40))]
            self.rl = 0
            self.blacktangle = [(self.screen, cBLACK, (0,0,40,self.w)),
                    (self.screen, cBLACK, (0,0,self.w,40)),
                    (self.screen, cBLACK, (self.w-40,0,40,self.h)),
                    (self.screen, cBLACK, (0,self.h-40,self.w,40))]
            pygame.draw.circle(self.screen, cWHITE, (self.w/2,self.h/2), 10)
            
            self.spellerFlag = 1
        elif self.spellerFlag == 1 and self.spellerCalibrationFlag == 1:
            print 'Calibration time!'
            if len(self.cal_positions)>0:
                self.x0, self.Ax, self.y0, self.By, self.meanx, self.meany = eye_calibr_params(self.cal_positions)
            self.resize(1280,1000)
            self.spellerFlag = 0
            self.startFlag = 0
        
        elif self.spellerFlag == 1 and self.startFlag == 1:
            print 'działam!', self.spellerFlag, self.startFlag
            pygame.init()
            keys=pygame.key.get_pressed()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    break
                if keys[ord('q')]:
                    pygame.quit()
                    break
                if keys[ord('z')]:
                    self.screen.fill(cBLACK)
# 
#             frame = self.cam.frame()
#             frame_gray = bgr2gray(frame)
#             frame_thresh = threshold(frame_gray, self.thresh_v, 
#                                      thresh_type=self.threshold_types[self.thresh_t])
# 
#             self.where_glint = glint(frame_gray,maxCorners=2)
#             self.where_pupil = pupil(frame_thresh)
                    
            mx,my =  self.mean_pupfinder()
            pygame.draw.circle(self.screen, cRED, (int(self.w-mx),my), 1)
            pygame.display.flip()

            if time.time()- self.t0>1:
                self.cal_positions.append((mx,my))
            
            if time.time() - self.t_arr>2:
                if self.rl>0:
                    pygame.draw.rect(*self.blacktangle[self.rl-1])
                elif self.rl==0:
                    pygame.draw.rect(*self.blacktangle[3])
                pygame.draw.rect(*self.rectangle[self.rl])
                self.rl+=1
                self.t_arr = time.time()
                if self.rl>=4:
                    self.rl=0

            if time.time() - self.t0>self.calibr_length:
                self.spellerCalibrationFlag =1
                #print 'aaaaaaaaaa'
                pygame.quit()

    def module_calibration_rectangle(self):
        if self.spellerFlag == 0 and self.startFlag == 1:
            
            self.calibr_length = 18
            self.resize(0,0)

            scr_x = self.ui.trueScreen.width()
            scr_y = self.ui.trueScreen.height()
            
            pygame.init()
            self.screen = pygame.display.set_mode((scr_x,scr_y))
            pygame.display.set_caption('calibration')
            self.cal_positions = []
            self.t0 = time.time()
            self.t_arr = time.time()
            C,D = 350,160#marginesy
            rect_big = 100 # wielkosc prostokata
            
            self.rectangle = []
            self.cal_buffer = []
            for i in range(1,5):
                for j in range(1,5):
                    self.rectangle.append((self.screen, cRED, (i*C,j*D,rect_big,rect_big)))
            self.rl = 0
            
            self.spellerFlag = 1
        elif self.spellerFlag == 1 and self.spellerCalibrationFlag == 1:
            print 'Calibration time!'
            if len(self.cal_positions)>0:
                self.x0, self.Ax, self.y0, self.By, self.meanx, self.meany = eye_calibr_params(self.cal_positions)
            self.resize(1280,1000)
            self.spellerFlag = 0
            self.startFlag = 0
            
            x_true = []
            y_true = []
            x_esti = []
            y_esti = []
            
            for ind in self.to_calibr_rect:
                x_true.append(ind[0][0])
                y_true.append(ind[0][1])
                x_esti.append(ind[1])
                y_esti.append(ind[2])
                
            self.x_true = np.array(x_true)
            self.y_true = np.array(y_true)
            self.x_esti = np.array(x_esti)
            self.y_esti = np.array(y_esti)
            
            #print self.to_calibr_rect
            #print self.x_true
            #print self.y_true
            #print self.x_esti
            #print self.y_esti
            
            # $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$
            # $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$
            # $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$
            
            self.x_opt, x_pcov = curve_fit(f_for_fitting , (self.x_esti , self.y_esti) , x_true)
            self.y_opt, y_pcov = curve_fit(f_for_fitting , (self.x_esti , self.y_esti) , y_true)
            
            #print self.x_opt
            #print self.y_opt
            
            # $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$
            # $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$
            # $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$
            
            #self.config_parameters_x = np.polyfit(np.vstack([self.x_esti,self.y_esti]), np.vstack([self.x_true,self.y_true]), 12)
            #self.config_parameters_y = np.polyfit(np.vstack([self.x_esti,self.y_esti]), self.y_true, 12)
        
        elif self.spellerFlag == 1 and self.startFlag == 1:
            #print 'działam!', self.spellerFlag, self.startFlag
            pygame.init()
            keys=pygame.key.get_pressed()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    break
                if keys[ord('q')]:
                    pygame.quit()
                    break
                if keys[ord('z')]:
                    self.screen.fill(cBLACK)

            mx,my =  self.mean_pupfinder()
            
            #print mx , my
            #pygame.draw.circle(self.screen, cRED, (int(self.w-mx),my), 1)
            

            if time.time()- self.t0>1:
                self.cal_buffer.append((mx,my))
            
            if time.time() - self.t_arr>1:
                
                if self.rl>0:
                    #print np.mean(np.array(self.cal_buffer),axis=0)
                    mn_x, mn_y = np.mean(np.array(self.cal_buffer),axis=0)
                    try:
                        self.to_calibr_rect.append([self.rectangle[self.rl-1][-1],mn_x, mn_y])
                    except IndexError:
                        pass 
                self.screen.fill(cBLACK)
                pygame.draw.rect(*self.rectangle[self.rl])
                self.t_arr = time.time()
                self.rl+=1
                self.cal_buffer = []
                if self.rl>=len(self.rectangle):
                    self.rl = 0
                
            pygame.display.flip()
            if time.time() - self.t0>self.calibr_length:
                self.spellerCalibrationFlag =1
                pygame.quit()

                
    def position(self):
        mx,my =  self.mean_pupfinder()
        
        #print '> x_0 ={}, A_x={}, y_0={}, B_y={}'.format( self.x0,self.Ax,self.y0,self.By )
        
        #meanx = 0.5*(2*self.x0+self.Ax)
        #meany = 0.5*(2*self.y0+self.By)
        #meanx = self.meanx
        #meany = self.meany
        #C = 1.
        #scr_x = self.ui.trueScreen.width()
        #scr_y = self.ui.trueScreen.height()

        #xp, yp = mx - meanx, my - meany
        #zx = (scr_x*C/self.Ax)*xp + scr_x/2.
        #zy = (scr_y*C/self.By)*yp + scr_y/2.
        #print int(zx), int(zy)
        
#        zx = mx * (scr_x / self.Ax)
#        zy = my * (scr_y / self.By)
  #      kx = scr_x*1./self.Ax *mx
 #       ky = scr_y*1./self.By *my
 
        #return int(kx), int(ky)
        
        [a1,b1,c1,d1,e1,f1] = self.x_opt
        [a2,b2,c2,d2,e2,f2] = self.y_opt
        
        screen_x = f_for_fitting((mx,my) , a1,b1,c1,d1,e1,f1)
        screen_y = f_for_fitting((mx,my) , a2,b2,c2,d2,e2,f2)
        
        self.screen_x_list.append(screen_x)
        self.screen_y_list.append(screen_y)
        
        if len(self.screen_x_list) == 5:
            screen_x = np.mean(self.screen_x_list)
            self.screen_x_list.pop(0)
            screen_y = np.mean(self.screen_y_list)
            self.screen_y_list.pop(0)
        
        
        
        result_string = str(screen_x) + ' ' + str(screen_y)
        
        #print result_string
        #return int(screen_x), int(screen_y)
        return result_string
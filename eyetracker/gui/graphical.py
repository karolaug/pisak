## #!/usr/bin/env python
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

from PyQt4 import QtCore, QtGui
import eyetracker

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)


class Ui_StartingWindow(object):
    ''' GUI graphical part for the main window.

    Class governing the graphical part of the default graphical user interface.
    It describes only parameters of used widgets, all operational functions
    are placed in separate class in eyetracker/gui/functional.

    '''

    def setupUi(self, StartingWindow):
        ''' Initialization of all needed widgets.

        '''

        StartingWindow.setObjectName(_fromUtf8("StartingWindow"))
        StartingWindow.setEnabled(True)
        StartingWindow.resize(1280, 640)
        StartingWindow.setMinimumSize(QtCore.QSize(1400, 1000))
        #StartingWindow.setMaximumSize(QtCore.QSize(640, 640))
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(_fromUtf8("pictures/camera.svg")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        StartingWindow.setWindowIcon(icon)
        
        self.trueScreen = QtGui.QDesktopWidget().screenGeometry()
        #print trueScreen.width(), trueScreen.height()

        self.centralwidget = QtGui.QWidget(StartingWindow)
        self.centralwidget.setObjectName(_fromUtf8("centralwidget"))


        self.groupBoxCamera = QtGui.QGroupBox(self.centralwidget)
        self.groupBoxCamera.setGeometry(QtCore.QRect(40, 600, 640, 250))
        self.groupBoxCamera.setObjectName(_fromUtf8("groupBoxCamera"))

        self.groupBoxDetection = QtGui.QGroupBox(self.centralwidget)
        self.groupBoxDetection.setGeometry(QtCore.QRect(720, 600, 640, 250))
        self.groupBoxDetection.setObjectName(_fromUtf8("groupBoxDetection"))

        #self.lbl_title = QtGui.QLabel(self.centralwidget)
        #self.lbl_title.setEnabled(True)
        #self.lbl_title.setGeometry(QtCore.QRect(100, 10, StartingWindow.width(), 16))
        #font = QtGui.QFont()
        #font.setBold(True)
        #font.setItalic(True)
        #font.setWeight(75)
        #self.lbl_title.setFont(font)
        #self.lbl_title.setTextFormat(QtCore.Qt.RichText)
        #self.lbl_title.setObjectName(_fromUtf8("lbl_title"))

        self.btn_start = QtGui.QPushButton(self.centralwidget)
        self.btn_start.setGeometry(QtCore.QRect(1160, 920, 200, 40))
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap(_fromUtf8("pictures/start.svg")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.btn_start.setIcon(icon1)
        self.btn_start.setObjectName(_fromUtf8("btn_start"))





        self.lbl_setCamera = QtGui.QLabel(self.groupBoxCamera)
        self.lbl_setCamera.setGeometry(QtCore.QRect(20, 40, 200, 40))
        self.lbl_setCamera.setObjectName(_fromUtf8("lbl_setCamera"))

        self.lbl_setResolution = QtGui.QLabel(self.groupBoxCamera)
        self.lbl_setResolution.setGeometry(QtCore.QRect(20, 120, 200, 40))
        self.lbl_setResolution.setObjectName(_fromUtf8("lbl_setResolution"))

        self.cmb_setCamera = QtGui.QComboBox(self.groupBoxCamera)
        self.cmb_setCamera.setGeometry(QtCore.QRect(220, 40, 200, 40))
        self.cmb_setCamera.setObjectName(_fromUtf8("cmb_setCamera"))

        self.cmb_setResolution = QtGui.QComboBox(self.groupBoxCamera)
        self.cmb_setResolution.setGeometry(QtCore.QRect(220, 120, 200, 40))
        self.cmb_setResolution.setObjectName(_fromUtf8("cmb_setResolution"))

        self.chb_flip = QtGui.QCheckBox(self.groupBoxCamera)
        self.chb_flip.setGeometry(QtCore.QRect(20, 180, 94, 40))
        self.chb_flip.setObjectName(_fromUtf8("chb_flip"))

        self.chb_mirror = QtGui.QCheckBox(self.groupBoxCamera)
        self.chb_mirror.setGeometry(QtCore.QRect(20, 220, 94, 40))
        self.chb_mirror.setObjectName(_fromUtf8("chb_mirror"))






        self.lbl_pupilDetection = QtGui.QLabel(self.groupBoxDetection)
        self.lbl_pupilDetection.setGeometry(QtCore.QRect(20, 40, 200, 20))
        self.lbl_pupilDetection.setObjectName(_fromUtf8("lbl_pupilDetection"))

        self.hsb_pupil = QtGui.QScrollBar(self.groupBoxDetection)
        self.hsb_pupil.setEnabled(True)
        self.hsb_pupil.setGeometry(QtCore.QRect(300, 40, 160, 20))
        self.hsb_pupil.setMaximum(255)
        self.hsb_pupil.setOrientation(QtCore.Qt.Horizontal)
        self.hsb_pupil.setObjectName(_fromUtf8("hsb_pupil1"))

        self.lbl_pupil = QtGui.QLabel(self.groupBoxDetection)
        self.lbl_pupil.setGeometry(QtCore.QRect(500, 40, 30, 20))
        self.lbl_pupil.setText(_fromUtf8(""))
        self.lbl_pupil.setObjectName(_fromUtf8("lbl_pupil1"))
 
 
 
        self.lbl_pupilNumber = QtGui.QLabel(self.groupBoxDetection)
        self.lbl_pupilNumber.setGeometry(QtCore.QRect(20, 80, 200, 20))
        self.lbl_pupilNumber.setObjectName(_fromUtf8("lbl_pupilNbumber"))
 
        self.hsb_pupil2 = QtGui.QScrollBar(self.groupBoxDetection)
        self.hsb_pupil2.setEnabled(True)
        self.hsb_pupil2.setGeometry(QtCore.QRect(300, 80, 160, 20))
        self.hsb_pupil2.setMaximum(5)
        self.hsb_pupil2.setOrientation(QtCore.Qt.Horizontal)
        self.hsb_pupil2.setObjectName(_fromUtf8("hsb_pupil2"))
 
        self.lbl_pupil2 = QtGui.QLabel(self.groupBoxDetection)
        self.lbl_pupil2.setGeometry(QtCore.QRect(500, 80, 30, 20))
        self.lbl_pupil2.setText(_fromUtf8(""))
        self.lbl_pupil2.setObjectName(_fromUtf8("lbl_pupil2"))
 
 
 
 
        self.lbl_glintDetection = QtGui.QLabel(self.groupBoxDetection)
        self.lbl_glintDetection.setGeometry(QtCore.QRect(20, 120, 200, 20))
        self.lbl_glintDetection.setObjectName(_fromUtf8("lbl_glintDetection"))
 
        self.hsb_glint = QtGui.QScrollBar(self.groupBoxDetection)
        self.hsb_glint.setEnabled(True)
        self.hsb_glint.setGeometry(QtCore.QRect(300, 120, 160, 20))
        self.hsb_glint.setMaximum(5)
        self.hsb_glint.setOrientation(QtCore.Qt.Horizontal)
        self.hsb_glint.setObjectName(_fromUtf8("hsb_glint2"))
 
        self.lbl_glint = QtGui.QLabel(self.groupBoxDetection)
        self.lbl_glint.setGeometry(QtCore.QRect(500, 120, 30, 20))
        self.lbl_glint.setText(_fromUtf8(""))
        self.lbl_glint.setObjectName(_fromUtf8("lbl_glint2"))
 
 
 
 
 
 
 
        self.lbl_alpha = QtGui.QLabel(self.centralwidget)
        self.lbl_alpha.setGeometry(QtCore.QRect(0,0,0,0))#360, 440, 140, 16))
        self.lbl_alpha.setObjectName(_fromUtf8("lbl_alpha"))
          
        self.led_alpha = QtGui.QLineEdit(self.centralwidget)
        self.led_alpha.setGeometry(QtCore.QRect(0,0,0,0))#500, 440, 50, 20))
        self.led_alpha.setObjectName(_fromUtf8("led_alpha"))
          
        self.lbl_pupilStackDeph = QtGui.QLabel(self.centralwidget)
        self.lbl_pupilStackDeph.setGeometry(QtCore.QRect(0,0,0,0))#360, 470, 140, 16))
        self.lbl_pupilStackDeph.setObjectName(_fromUtf8("lbl_pupilStackDeph"))
          
        self.led_pupilStackDeph = QtGui.QLineEdit(self.centralwidget)
        self.led_pupilStackDeph.setGeometry(QtCore.QRect(0,0,0,0))#500, 470, 50, 20))
        self.led_pupilStackDeph.setObjectName(_fromUtf8("led_pupilStackDeph"))
  
        self.lbl_decisionStackDeph = QtGui.QLabel(self.centralwidget)
        self.lbl_decisionStackDeph.setGeometry(QtCore.QRect(0,0,0,0))#360, 500, 140, 16))
        self.lbl_decisionStackDeph.setObjectName(_fromUtf8("lbl_decisionStackDeph"))
          
        self.led_decisionStackDeph = QtGui.QLineEdit(self.centralwidget)
        self.led_decisionStackDeph.setGeometry(QtCore.QRect(0,0,0,0))#500, 500, 50, 20))
        self.led_decisionStackDeph.setObjectName(_fromUtf8("led_decisionStackDeph"))
  
  
 
 
 
 
 
 
 
        self.cmb_setAlgorithm = QtGui.QComboBox(self.centralwidget)
        self.cmb_setAlgorithm.setGeometry(QtCore.QRect(920, 920, 200, 40))
        self.cmb_setAlgorithm.setObjectName(_fromUtf8("cmb_setAlgorithm"))
 
 
 
 

 
        self.btn_clear = QtGui.QPushButton(self.centralwidget)
        self.btn_clear.setGeometry(QtCore.QRect(40, 920, 40, 40))
        icon5 = QtGui.QIcon()
        icon5.addPixmap(QtGui.QPixmap(_fromUtf8("pictures/clear.svg")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.btn_clear.setIcon(icon5)
        self.btn_clear.setIconSize(QtCore.QSize(24, 24))
        self.btn_clear.setObjectName(_fromUtf8("btn_clear"))
        
        
        
        
        
 
        self.btn_save = QtGui.QPushButton(self.centralwidget)
        self.btn_save.setGeometry(QtCore.QRect(120, 920, 200, 40))
        icon4 = QtGui.QIcon()
        icon4.addPixmap(QtGui.QPixmap(_fromUtf8("pictures/save.svg")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.btn_save.setIcon(icon4)
        self.btn_save.setIconSize(QtCore.QSize(24, 24))
        self.btn_save.setObjectName(_fromUtf8("btn_save"))

        self.timer = QtCore.QBasicTimer()

        StartingWindow.setCentralWidget(self.centralwidget)
        #self.statusbar = QtGui.QStatusBar(StartingWindow)
        #self.statusbar.setObjectName(_fromUtf8("statusbar"))
        #StartingWindow.setStatusBar(self.statusbar)

        self.retranslateUi(StartingWindow)
        QtCore.QMetaObject.connectSlotsByName(StartingWindow)

    def retranslateUi(self, StartingWindow):
        '''Attach names to all widgets set up in setupUi function.
        '''

        StartingWindow.setWindowTitle(_translate("StartingWindow", "Eyetracter -- start" + eyetracker.version, None))
        #self.lbl_title.setText(_translate("StartingWindow", "Eyetracker "+eyetracker.version, None))
        self.btn_start.setText(_translate("StartingWindow", "START", None))
        self.lbl_setCamera.setText(_translate("StartingWindow", "Choose camera:", None))
        self.lbl_setResolution.setText(_translate("StartingWindow", "Choose resolution:", None))
        self.chb_flip.setText(_translate("StartingWindow", "Flip", None))
        self.chb_mirror.setText(_translate("StartingWindow", "Mirror", None))
        self.lbl_pupilDetection.setText(_translate("StartingWindow", "Pupil detection threshold:", None))
        self.lbl_pupilNumber.setText(_translate("StartingWindow", "Number of pupils to track:", None))
        self.lbl_glintDetection.setText(_translate("StartingWindow", "Number of glints to track:", None))
        self.lbl_alpha.setText(_translate("StartingWindow", "Alpha threshold:", None))
        self.lbl_pupilStackDeph.setText(_translate("StartingWindow", "PupilStackDeph:", None))
        self.lbl_decisionStackDeph.setText(_translate("StartingWindow", "DecisionStackDeph:", None))
        
        self.btn_save.setText(_translate("StartingWindow", "SAVE", None))
        self.groupBoxCamera.setTitle(_translate("MainWindow", "Camera settings", None))
        self.groupBoxDetection.setTitle(_translate("MainWindow", "Detection settings", None))
        
if __name__ == '__main__':
    print 'Using this class without it\'s functional part may be possible, but'
    print 'it would be completely useless.'

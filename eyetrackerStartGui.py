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
    def setupUi(self, StartingWindow):
        StartingWindow.setObjectName(_fromUtf8("StartingWindow"))
        StartingWindow.setEnabled(True)
        StartingWindow.resize(640, 480)
        StartingWindow.setMinimumSize(QtCore.QSize(640, 480))
        StartingWindow.setMaximumSize(QtCore.QSize(640, 480))
        
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(_fromUtf8("icon1.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        
        StartingWindow.setWindowIcon(icon)
        self.centralwidget = QtGui.QWidget(StartingWindow)
        self.centralwidget.setObjectName(_fromUtf8("centralwidget"))
        
        self.graphicsScene = QtGui.QGraphicsScene()
        
        self.graphicsView = QtGui.QGraphicsView(self.graphicsScene , self.centralwidget)
        self.graphicsView.setGeometry(QtCore.QRect(20, 80, 320, 240))
        self.graphicsView.setObjectName(_fromUtf8("graphicsView"))
        
        self.lbl_title = QtGui.QLabel(self.centralwidget)
        self.lbl_title.setEnabled(True)
        self.lbl_title.setGeometry(QtCore.QRect(130, 30, 111, 16))
        self.lbl_title.setTextFormat(QtCore.Qt.RichText)
        self.lbl_title.setObjectName(_fromUtf8("lbl_title"))
        
        self.btn_start = QtGui.QPushButton(self.centralwidget)
        self.btn_start.setGeometry(QtCore.QRect(20, 380, 120, 35))
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap(_fromUtf8("start.svg")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.btn_start.setIcon(icon1)
        self.btn_start.setObjectName(_fromUtf8("btn_start"))
        
        self.btn_settings = QtGui.QPushButton(self.centralwidget)
        self.btn_settings.setGeometry(QtCore.QRect(220, 330, 120, 35))
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap(_fromUtf8("prop.svg")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.btn_settings.setIcon(icon2)
        self.btn_settings.setIconSize(QtCore.QSize(24, 24))
        self.btn_settings.setObjectName(_fromUtf8("btn_settings"))
        
        self.lbl_setCamera = QtGui.QLabel(self.centralwidget)
        self.lbl_setCamera.setGeometry(QtCore.QRect(410, 30, 111, 20))
        self.lbl_setCamera.setObjectName(_fromUtf8("lbl_setCamera"))
        
        self.lbl_setResolution = QtGui.QLabel(self.centralwidget)
        self.lbl_setResolution.setGeometry(QtCore.QRect(410, 100, 141, 20))
        self.lbl_setResolution.setObjectName(_fromUtf8("lbl_setResolution"))
        
        self.cmb_setCamera = QtGui.QComboBox(self.centralwidget)
        self.cmb_setCamera.setGeometry(QtCore.QRect(410, 60, 100, 30))
        self.cmb_setCamera.setObjectName(_fromUtf8("cmb_setCamera"))
        
        self.cmb_setResolution = QtGui.QComboBox(self.centralwidget)
        self.cmb_setResolution.setGeometry(QtCore.QRect(410, 130, 100, 30))
        self.cmb_setResolution.setObjectName(_fromUtf8("cmb_setResolution"))
        
        self.chb_flip = QtGui.QCheckBox(self.centralwidget)
        self.chb_flip.setGeometry(QtCore.QRect(410, 170, 94, 20))
        self.chb_flip.setObjectName(_fromUtf8("chb_flip"))
        
        self.chb_mirror = QtGui.QCheckBox(self.centralwidget)
        self.chb_mirror.setGeometry(QtCore.QRect(410, 195, 94, 20))
        self.chb_mirror.setObjectName(_fromUtf8("chb_mirror"))
        
        self.lbl_pupilDetection = QtGui.QLabel(self.centralwidget)
        self.lbl_pupilDetection.setGeometry(QtCore.QRect(410, 240, 111, 20))
        self.lbl_pupilDetection.setObjectName(_fromUtf8("lbl_pupilDetection"))
        
        self.hsb_pupil1 = QtGui.QScrollBar(self.centralwidget)
        self.hsb_pupil1.setEnabled(False)
        self.hsb_pupil1.setGeometry(QtCore.QRect(410, 270, 160, 16))
        self.hsb_pupil1.setMaximum(255)
        self.hsb_pupil1.setOrientation(QtCore.Qt.Horizontal)
        self.hsb_pupil1.setObjectName(_fromUtf8("hsb_pupil1"))
        
        self.lbl_pupil1 = QtGui.QLabel(self.centralwidget)
        self.lbl_pupil1.setGeometry(QtCore.QRect(580, 270, 20, 16))
        self.lbl_pupil1.setText(_fromUtf8(""))
        self.lbl_pupil1.setObjectName(_fromUtf8("lbl_pupil1"))
        
        self.lbl_pupil2 = QtGui.QLabel(self.centralwidget)
        self.lbl_pupil2.setGeometry(QtCore.QRect(580, 290, 20, 16))
        self.lbl_pupil2.setText(_fromUtf8(""))
        self.lbl_pupil2.setObjectName(_fromUtf8("lbl_pupil2"))
        
        self.hsb_pupil2 = QtGui.QScrollBar(self.centralwidget)
        self.hsb_pupil2.setEnabled(False)
        self.hsb_pupil2.setGeometry(QtCore.QRect(410, 290, 160, 16))
        self.hsb_pupil2.setMaximum(3)
        self.hsb_pupil2.setOrientation(QtCore.Qt.Horizontal)
        self.hsb_pupil2.setObjectName(_fromUtf8("hsb_pupil2"))
        
        self.hsb_pupil3 = QtGui.QScrollBar(self.centralwidget)
        self.hsb_pupil3.setEnabled(False)
        self.hsb_pupil3.setGeometry(QtCore.QRect(410, 310, 160, 16))
        self.hsb_pupil3.setMaximum(255)
        self.hsb_pupil3.setOrientation(QtCore.Qt.Horizontal)
        self.hsb_pupil3.setObjectName(_fromUtf8("hsb_pupil3"))
        
        self.lbl_pupil3 = QtGui.QLabel(self.centralwidget)
        self.lbl_pupil3.setGeometry(QtCore.QRect(580, 310, 20, 16))
        self.lbl_pupil3.setText(_fromUtf8(""))
        self.lbl_pupil3.setObjectName(_fromUtf8("lbl_pupil3"))
        
        self.lbl_glintDetection = QtGui.QLabel(self.centralwidget)
        self.lbl_glintDetection.setGeometry(QtCore.QRect(410, 340, 111, 20))
        self.lbl_glintDetection.setObjectName(_fromUtf8("lbl_glintDetection"))
        
        self.hsb_glint2 = QtGui.QScrollBar(self.centralwidget)
        self.hsb_glint2.setEnabled(False)
        self.hsb_glint2.setGeometry(QtCore.QRect(410, 390, 160, 16))
        self.hsb_glint2.setMaximum(107)
        self.hsb_glint2.setOrientation(QtCore.Qt.Horizontal)
        self.hsb_glint2.setObjectName(_fromUtf8("hsb_glint2"))
        
        self.hsb_glint3 = QtGui.QScrollBar(self.centralwidget)
        self.hsb_glint3.setEnabled(False)
        self.hsb_glint3.setGeometry(QtCore.QRect(410, 410, 160, 16))
        self.hsb_glint3.setMaximum(255)
        self.hsb_glint3.setOrientation(QtCore.Qt.Horizontal)
        self.hsb_glint3.setObjectName(_fromUtf8("hsb_glint3"))
        
        self.lbl_glint2 = QtGui.QLabel(self.centralwidget)
        self.lbl_glint2.setGeometry(QtCore.QRect(580, 390, 20, 16))
        self.lbl_glint2.setText(_fromUtf8(""))
        self.lbl_glint2.setObjectName(_fromUtf8("lbl_glint2"))
        
        self.lbl_glint1 = QtGui.QLabel(self.centralwidget)
        self.lbl_glint1.setGeometry(QtCore.QRect(580, 370, 20, 16))
        self.lbl_glint1.setText(_fromUtf8(""))
        self.lbl_glint1.setObjectName(_fromUtf8("lbl_glint1"))
        
        self.lbl_glint3 = QtGui.QLabel(self.centralwidget)
        self.lbl_glint3.setGeometry(QtCore.QRect(580, 410, 20, 16))
        self.lbl_glint3.setText(_fromUtf8(""))
        self.lbl_glint3.setObjectName(_fromUtf8("lbl_glint3"))
        
        self.hsb_glint1 = QtGui.QScrollBar(self.centralwidget)
        self.hsb_glint1.setEnabled(False)
        self.hsb_glint1.setGeometry(QtCore.QRect(410, 370, 160, 16))
        self.hsb_glint1.setMaximum(255)
        self.hsb_glint1.setOrientation(QtCore.Qt.Horizontal)
        self.hsb_glint1.setObjectName(_fromUtf8("hsb_glint1"))
        
        self.cmb_setAlgorithm = QtGui.QComboBox(self.centralwidget)
        self.cmb_setAlgorithm.setGeometry(QtCore.QRect(20, 340, 120, 30))
        self.cmb_setAlgorithm.setObjectName(_fromUtf8("cmb_setAlgorithm"))
        
        self.btn_load = QtGui.QPushButton(self.centralwidget)
        self.btn_load.setGeometry(QtCore.QRect(220, 420, 120, 35))
        icon3 = QtGui.QIcon()
        icon3.addPixmap(QtGui.QPixmap(_fromUtf8("load.svg")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.btn_load.setIcon(icon3)
        self.btn_load.setIconSize(QtCore.QSize(24, 24))
        self.btn_load.setObjectName(_fromUtf8("btn_load"))
        
        self.btn_save = QtGui.QPushButton(self.centralwidget)
        self.btn_save.setGeometry(QtCore.QRect(220, 380, 120, 35))
        icon4 = QtGui.QIcon()
        icon4.addPixmap(QtGui.QPixmap(_fromUtf8("save.svg")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.btn_save.setIcon(icon4)
        self.btn_save.setIconSize(QtCore.QSize(24, 24))
        self.btn_save.setObjectName(_fromUtf8("btn_save"))
        
        StartingWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtGui.QStatusBar(StartingWindow)
        self.statusbar.setObjectName(_fromUtf8("statusbar"))
        StartingWindow.setStatusBar(self.statusbar)

        self.retranslateUi(StartingWindow)
        QtCore.QMetaObject.connectSlotsByName(StartingWindow)

    def retranslateUi(self, StartingWindow):
        StartingWindow.setWindowTitle(_translate("StartingWindow", "Eyetracter -- start", None))
        self.lbl_title.setText(_translate("StartingWindow", "Eyetracker v_0.1", None))
        self.btn_start.setText(_translate("StartingWindow", "START", None))
        self.btn_settings.setText(_translate("StartingWindow", "PROP", None))
        self.lbl_setCamera.setText(_translate("StartingWindow", "Choose camera:", None))
        self.lbl_setResolution.setText(_translate("StartingWindow", "Choose resolution:", None))
        self.chb_flip.setText(_translate("StartingWindow", "Flip", None))
        self.chb_mirror.setText(_translate("StartingWindow", "Mirror", None))
        self.lbl_pupilDetection.setText(_translate("StartingWindow", "Pupil detection:", None))
        self.lbl_glintDetection.setText(_translate("StartingWindow", "Glint detection:", None))
        self.btn_load.setText(_translate("StartingWindow", "LOAD", None))
        self.btn_save.setText(_translate("StartingWindow", "SAVE", None))


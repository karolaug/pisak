# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'eyetracker-ng.ui'
#
# Created: Mon Nov 25 13:48:43 2013
#      by: PyQt4 UI code generator 4.10.3
#
# WARNING! All changes made in this file will be lost!

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
        StartingWindow.resize(640, 640)
        StartingWindow.setMinimumSize(QtCore.QSize(640, 640))
        StartingWindow.setMaximumSize(QtCore.QSize(640, 640))
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(_fromUtf8("../../Obrazy/icon.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        StartingWindow.setWindowIcon(icon)
        
        self.centralwidget = QtGui.QWidget(StartingWindow)
        self.centralwidget.setObjectName(_fromUtf8("centralwidget"))
        
        self.graphicsView = QtGui.QGraphicsView(self.centralwidget)
        self.graphicsView.setGeometry(QtCore.QRect(20, 40, 320, 240))
        self.graphicsView.setObjectName(_fromUtf8("graphicsView"))
        
        self.lbl_title = QtGui.QLabel(self.centralwidget)
        self.lbl_title.setEnabled(True)
        self.lbl_title.setGeometry(QtCore.QRect(260, 10, 120, 16))
        font = QtGui.QFont()
        font.setBold(True)
        font.setItalic(True)
        font.setWeight(75)
        self.lbl_title.setFont(font)
        self.lbl_title.setTextFormat(QtCore.Qt.RichText)
        self.lbl_title.setObjectName(_fromUtf8("lbl_title"))
        
        self.btn_start = QtGui.QPushButton(self.centralwidget)
        self.btn_start.setGeometry(QtCore.QRect(150, 560, 120, 35))
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap(_fromUtf8("../../Obrazy/Ikonki/Faenza_1.3/actions/dialog-ok.svg")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.btn_start.setIcon(icon1)
        self.btn_start.setObjectName(_fromUtf8("btn_start"))
        
        self.lbl_setCamera = QtGui.QLabel(self.centralwidget)
        self.lbl_setCamera.setGeometry(QtCore.QRect(360, 40, 111, 20))
        self.lbl_setCamera.setObjectName(_fromUtf8("lbl_setCamera"))
        
        self.lbl_setResolution = QtGui.QLabel(self.centralwidget)
        self.lbl_setResolution.setGeometry(QtCore.QRect(360, 110, 141, 20))
        self.lbl_setResolution.setObjectName(_fromUtf8("lbl_setResolution"))
        
        self.cmb_setCamera = QtGui.QComboBox(self.centralwidget)
        self.cmb_setCamera.setGeometry(QtCore.QRect(360, 70, 100, 30))
        self.cmb_setCamera.setObjectName(_fromUtf8("cmb_setCamera"))
        
        self.cmb_setResolution = QtGui.QComboBox(self.centralwidget)
        self.cmb_setResolution.setGeometry(QtCore.QRect(360, 140, 100, 30))
        self.cmb_setResolution.setObjectName(_fromUtf8("cmb_setResolution"))
        
        self.chb_flip = QtGui.QCheckBox(self.centralwidget)
        self.chb_flip.setGeometry(QtCore.QRect(360, 180, 94, 20))
        self.chb_flip.setObjectName(_fromUtf8("chb_flip"))
        
        self.chb_mirror = QtGui.QCheckBox(self.centralwidget)
        self.chb_mirror.setGeometry(QtCore.QRect(360, 205, 94, 20))
        self.chb_mirror.setObjectName(_fromUtf8("chb_mirror"))
        
        self.lbl_pupilDetection = QtGui.QLabel(self.centralwidget)
        self.lbl_pupilDetection.setGeometry(QtCore.QRect(360, 250, 111, 20))
        self.lbl_pupilDetection.setObjectName(_fromUtf8("lbl_pupilDetection"))
        
        self.hsb_pupil1 = QtGui.QScrollBar(self.centralwidget)
        self.hsb_pupil1.setEnabled(False)
        self.hsb_pupil1.setGeometry(QtCore.QRect(360, 280, 160, 16))
        self.hsb_pupil1.setMaximum(255)
        self.hsb_pupil1.setOrientation(QtCore.Qt.Horizontal)
        self.hsb_pupil1.setObjectName(_fromUtf8("hsb_pupil1"))
        
        self.lbl_pupil1 = QtGui.QLabel(self.centralwidget)
        self.lbl_pupil1.setGeometry(QtCore.QRect(530, 280, 20, 16))
        self.lbl_pupil1.setText(_fromUtf8(""))
        self.lbl_pupil1.setObjectName(_fromUtf8("lbl_pupil1"))
        
        self.lbl_glintDetection = QtGui.QLabel(self.centralwidget)
        self.lbl_glintDetection.setGeometry(QtCore.QRect(360, 310, 111, 20))
        self.lbl_glintDetection.setObjectName(_fromUtf8("lbl_glintDetection"))
        
        self.lbl_glint1 = QtGui.QLabel(self.centralwidget)
        self.lbl_glint1.setGeometry(QtCore.QRect(530, 340, 20, 16))
        self.lbl_glint1.setText(_fromUtf8(""))
        self.lbl_glint1.setObjectName(_fromUtf8("lbl_glint1"))
        
        self.hsb_glint1 = QtGui.QScrollBar(self.centralwidget)
        self.hsb_glint1.setGeometry(QtCore.QRect(360, 340, 160, 16))
        self.hsb_glint1.setMaximum(255)
        self.hsb_glint1.setOrientation(QtCore.Qt.Horizontal)
        self.hsb_glint1.setObjectName(_fromUtf8("hsb_glint1"))
        
        self.cmb_setAlgorithm = QtGui.QComboBox(self.centralwidget)
        self.cmb_setAlgorithm.setGeometry(QtCore.QRect(20, 560, 120, 35))
        self.cmb_setAlgorithm.setObjectName(_fromUtf8("cmb_setAlgorithm"))
        
        self.btn_load = QtGui.QPushButton(self.centralwidget)
        self.btn_load.setGeometry(QtCore.QRect(500, 510, 120, 35))
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap(_fromUtf8("../../Obrazy/Ikonki/Faenza_1.3/actions/document-open.svg")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.btn_load.setIcon(icon2)
        self.btn_load.setIconSize(QtCore.QSize(24, 24))
        self.btn_load.setObjectName(_fromUtf8("btn_load"))
        
        self.btn_save = QtGui.QPushButton(self.centralwidget)
        self.btn_save.setGeometry(QtCore.QRect(500, 560, 120, 35))
        icon3 = QtGui.QIcon()
        icon3.addPixmap(QtGui.QPixmap(_fromUtf8("../../Obrazy/Ikonki/Faenza_1.3/actions/document-import.svg")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.btn_save.setIcon(icon3)
        self.btn_save.setIconSize(QtCore.QSize(24, 24))
        self.btn_save.setObjectName(_fromUtf8("btn_save"))
        
        self.graphicsView_2 = QtGui.QGraphicsView(self.centralwidget)
        self.graphicsView_2.setGeometry(QtCore.QRect(20, 290, 320, 240))
        self.graphicsView_2.setObjectName(_fromUtf8("graphicsView_2"))
        
        StartingWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtGui.QStatusBar(StartingWindow)
        self.statusbar.setObjectName(_fromUtf8("statusbar"))
        StartingWindow.setStatusBar(self.statusbar)

        self.retranslateUi(StartingWindow)
        QtCore.QMetaObject.connectSlotsByName(StartingWindow)

    def retranslateUi(self, StartingWindow):
        StartingWindow.setWindowTitle(_translate("StartingWindow", "Eyetracter -- start", None))
        self.lbl_title.setText(_translate("StartingWindow", "Eyetracker v0.2", None))
        self.btn_start.setText(_translate("StartingWindow", "START", None))
        self.lbl_setCamera.setText(_translate("StartingWindow", "Choose camera:", None))
        self.lbl_setResolution.setText(_translate("StartingWindow", "Choose resolution:", None))
        self.chb_flip.setText(_translate("StartingWindow", "Flip", None))
        self.chb_mirror.setText(_translate("StartingWindow", "Mirror", None))
        self.lbl_pupilDetection.setText(_translate("StartingWindow", "Pupil detection:", None))
        self.lbl_glintDetection.setText(_translate("StartingWindow", "Glint detection:", None))
        self.btn_load.setText(_translate("StartingWindow", "LOAD", None))
        self.btn_save.setText(_translate("StartingWindow", "SAVE", None))


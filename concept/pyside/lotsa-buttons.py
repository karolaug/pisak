#!/usr/bin/python

import sys, time
from PySide import QtGui, QtCore

class CycleThread(QtCore.QThread):
    tick_on = QtCore.Signal(int)
    tick_off = QtCore.Signal(int)

    def __init__(self, window):
        super(CycleThread, self).__init__()
        self.finished = False
        self.window = window
        self.tick_on.connect(self.window.hilite_on)
        self.tick_off.connect(self.window.hilite_off)

    def run(self):
        current_row = 0
        while not self.finished:
            self.tick_on.emit(current_row)
            time.sleep(1)
            self.tick_off.emit(current_row)
            current_row = (current_row + 1) % self.window.rows

class MainWindow(QtGui.QWidget):
    rows = 15
    cols = 16

    def __init__(self):
        super(MainWindow, self).__init__()
        self.buttons = []
        self.resize(250, 150)
        self.setWindowTitle("Simple")
        self._init_buttons()
        self.showFullScreen()
        self.setStyleSheet("font: 8pt")

    def _init_buttons(self):
        grid = QtGui.QGridLayout()
        for i in range(self.rows):
           row = []
           for j in range(self.cols):
               button = QtGui.QPushButton("%d, %d" % (j, i), self)
               row.append(button)
               grid.addWidget(button, i, j)
           self.buttons.append(row)
        self.setLayout(grid)

    @QtCore.Slot(int)
    def hilite_on(self, i):
        self.row_style(i, "background-color: rgb(128, 160, 225)")

    @QtCore.Slot(int)
    def hilite_off(self, i):
        self.row_style(i, "")

    def row_style(self, i, style):
        for button in self.buttons[i]:
            button.setStyleSheet(style)

class PisakApp(QtGui.QApplication):
    def __init__(self):
        super(PisakApp, self).__init__(sys.argv)
        self.main_window = MainWindow()
        self.cycle_thread = CycleThread(self.main_window)
        self.cycle_thread.start()

    @classmethod
    def run_main(cls):
        app = cls()
        ret = app.exec_()
        app.cycle_thread.finished = True
        app.cycle_thread.wait()
        sys.exit(ret)

PisakApp.run_main()

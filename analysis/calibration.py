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
from analysis.processing import mark

def get_resolution():#for use only if PySide is not in use, it's there already
    '''
    Only to be used in Linux and when PySide is not in use, as there 
    the size of the screen can be queried from 
    "app = QtGui.QApplication(sys.argv)" 
    with 
    "app.dektop().screenGeometry()".

    Function uses Linux command "xrandr" to query the system about current
    resoulution.

    Returns:
    --------
    tuple(width, height) - where width and height are "int"
    '''
    from os import popen
    screen = popen('xrandr -q').readlines()[0] #to do: mistake-proof parsing
    width = int(screen.split()[7])
    height = int(screen.split()[9][:-1])
    return (width, height)

def create_image(name, screen_size=None):
    '''
    Creates a fullscreen image for calibration purposes.

    Parameters:
    -----------
    name - name of the window, will be displayed at the top of the window
    screen_size - tuple(width, height)

    Returns:
    --------
    don't know yet;)
    '''
    window = cv2.namedWindow(str(name))
    if screen_size is None:
        screen_size = get_resolution()
    image = np.zeros((screen_size[1], screen_size[0], 3), np.uint8)
    


def pointers(image, number, size_diff):
    


if __name__ == '__main__':
    '''to do!'''

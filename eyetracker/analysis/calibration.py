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
from .processing import mark

def get_resolution():#for use only if PySide is not in use, it's there already
    ''' Checks current screen resolution

    Only to be used in Linux and when PySide is not in use, as there
    the size of the screen can be queried from
    app = QtGui.QApplication(sys.argv) with
    app.dektop().screenGeometry().

    Function uses Linux command "xrandr" to query the system about current
    resoulution.

    Returns
    --------
    size : tuple of ints (width, height)
        size of screen in pixels
    '''
    from os import popen
    screen = popen('xrandr -q').readlines()[0]
    width = int(screen.split()[7])
    height = int(screen.split()[9][:-1])
    return (width, height)

def where_circles(resolution=False, rad=30):
    ''' Clears the image and draws a new circle.

    Parameters
    -----------
    resolution : tuple 
        ints (width, height)
    rad : int
        radius of the biggest circle that will be drawn
    
    Returns
    --------
    coordinates : tuples
        coordinates of nine places where the circles will be drawn
    '''

    if not resolution:
        resolution = get_resolution()

    w = resolution[0]
    h = resolution[1]
    
    circles = {'C' : (w/2, h/2), 'N' : (w/2, rad), 'S' : (w/2, h-rad), 
               'W': (rad, h/2), 'E' : (w-rad, h/2), 'NW' : (rad, rad),
               'NE' : (w-rad, rad), 'SE' : (w-rad, h-rad), 'SW' : (rad, h-rad),
               'radius' : rad}
    
    return circles, resolution

def draw_watch_points(circles, resolution):
    base_image = np.zeros((resolution[1], resolution[0], 3), np.uint8)
    mod_image = base_image.copy()
    

def calibrate(resolution=False):

    if not resolution:
        resolution = get_resolution()

    base_image = np.zeros((resolution[1], resolution[0], 3), np.uint8)
    mod_image = base_image.copy()
    return


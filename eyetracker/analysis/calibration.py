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
    ''' Check what current resolution is

    Only to be used in Linux and when PySide is not in use, as there
    the size of the screen can be queried from
    app = QtGui.QApplication(sys.argv) with
    app.dektop().screenGeometry().

    Function uses Linux command "xrandr" to query the system about current
    resoulution.

    Returns
    --------
    size : tuple of int (width, height)
        size of screen in pixels
    '''
    from os import popen
    screen = popen('xrandr -q').readlines()[0] #to do: mistake-proof parsing
    width = int(screen.split()[7])
    height = int(screen.split()[9][:-1])
    return (width, height)

screen_size = get_resolution()

base_image = np.zeros((screen_size[1], screen_size[0], 3), np.uint8)

def draw_circle(where_mark, radius, color='red', image=False):
    ''' Clears the image and draws a new circle.

    Parameters
    -----------
    where_mark : int
        where is to be placed new mark
    radius : int
        radius of the mark
    color : string
        color of the mark
        allowed are keys from analysis.processing colors dictionary
        as of now it is red, green or blue

    Returns
    --------
    image : np.array
        shape (height, width, 3) with the drawn circle
    '''

    if image == False:
        image = np.zeros((screen_size[1], screen_size[0], 3), np.uint8)
    mod_image = image.copy()
    mark(mod_image, where_mark, radius, colors[color], thickness=10)
    return mod_image

#def calibration(with_purkinje=False):
#    ''' Displays a set of points to look at for calibration.
#
#    Parameters
#    -----------
#    with_purkinje : If with_purkinje=True, additional dictionary is returned
#        with vector distances of virtual purkinje image and the estimated middle
#        of retina.
#
#    Returns
#    --------
#    Dictionary of tuples being the cooridnates of the estimated middle of
#    retina while looking at different points on the screen.
#
#    Additional dictionary of vector distances if with_purkinje=True.
#    '''




if __name__ == '__main__':
    '''to do!'''

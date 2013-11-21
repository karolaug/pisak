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
# e-mail: saszasasha@gmail.com
# University of Warsaw 2013

import cv2
import numpy as np

from ..analysis.detect import pupil, glint
from ..analysis.processing import threshold , mark

colors = {'blue' : (255, 0, 0), 'green' : (0, 255, 0), 'red' : (0, 0, 255)}

thresholds = {'otsu' : cv2.THRESH_OTSU, 'bin' : cv2.THRESH_BINARY, 
              'bin_inv' : cv2.THRESH_BINARY_INV, 
              'zero' : cv2.THRESH_TOZERO, 'zero_inv' : cv2.THRESH_TOZERO_INV,
              'trunc' : cv2.THRESH_TRUNC}

def displayGlint(gray, thres):
    '''
    To do
    '''
    where_glint = glint(gray)
    if where_glint != None:
        color = cv2.cvtColor(gray, cv2.COLOR_GRAY2BGR)
        for cor in where_glint:
            cv2.circle(color, tuple(cor), 10, (255, 0, 0), 3)
    return color

def displayPupil(image , thres):
    '''
    To do
    '''
    black1 = threshold(image, thresh_v=thres[2], max_v=thres[0], thresh_type='trunc')#thresholds[thres[1]])
    where_pupil = pupil(black1)
    if where_pupil != None:
        black1 = cv2.cvtColor(black1, cv2.COLOR_GRAY2BGR)
        for cor in where_pupil:
            cv2.circle(black1, tuple(cor[:2]), cor[2], (0, 0, 255), 3)
    return black1

def displayImage(image , where='new'):
    '''
    To do
    '''
    if where == 'new':
        cv2.namedWindow('new' , flags=cv2.CV_WINDOW_AUTOSIZE)
    cv2.imshow( where , image)
            
if __name__ == '__main__':
    pass

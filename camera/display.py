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

def displayGlint(gray):
    '''
    To do
    '''
    where_glint = glint(gray)
    if where_glint != None:
        gray = cv2.cvtColor(gray, cv2.COLOR_GRAY2BGR)
        for cor in where_glint:
            cv2.circle(gray, tuple(cor), 10, 'blue', 3)
    return gray

def displayPupil(image , thres):
    '''
    To do
    '''
    black1 = threshold(image, thresh_v=thres[2], max_v=thres[0], thresh_type=thresholds[thres[1]])
    where_pupil = pupil(black1)
    if where_pupil != None:
        black1 = cv2.cvtColor(black1, cv2.COLOR_GRAY2BGR)
        for cor in where_pupil:
            cv2.circle(black1, tuple(cor[:2]), cor[2], 'red', 3)
    return black1

if __name__ == '__main__':
    pass

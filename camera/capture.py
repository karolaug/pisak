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
from glob import iglob

def grabFrame(cap=None):
    '''
    To do
    '''
    if cap == None:
        im = self.im[self.index]
        im = cv2.resize(im,(320,240))
    else:
        try:
            ret, im = self.cap.read()
        except:                             # KONIECZNIE TRZEBA TU WSTAWIĆ TYP WYJĄTKU!!!
            print 'Wrong capture stream.'
    return im
    
def lookForCameras():
    '''
    To do
    '''
    listOfCameras = {''.join(['Camera_', str(i+1)]) : i 
                     for i, cam in enumerate(iglob('/dev/video*'))}
    listOfCameras['dummy'] = None
    return listOfCameras

if __name__ == '__main__':
    print 'Lista odnalezionych kamer wraz z "dummy":\n', lookForCameras()

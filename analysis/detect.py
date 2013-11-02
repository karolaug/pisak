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

def eye(image):
    #should return a mask
    pass

def blink():
    #should return bin
    pass

def glint(image, maxCorners=2, quality=0.0001, minDist=20, mask=None, 
          blockSize=3):
    '''
    TO DO!
    '''
    where = cv2.goodFeaturesToTrack(image, maxCorners=maxCorners, 
                                    qualityLevel=quality, minDistance=minDist, 
                                    mask=mask, blockSize=blockSize)
    #TODO: add constrain of max distance
    if where != None:
        where = np.array([where[i][0] for i in xrange(where.shape[0])])
    return where

def pupil(image):
    '''
    TO DO!
    '''
    circles = cv2.HoughCircles(image, cv2.cv.CV_HOUGH_GRADIENT, 1, 100, 
                               param1=50, param2=10, minRadius=20, maxRadius=70)
    if circles != None:
        circles = np.uint16(np.around(circles))[0] 
    return circles

if __name__ == '__main__':
    from analysis.processing import threshold, gray2bgr, bgr2gray, mark

    im_gray = cv2.imread('examples/eyeIR.png', 0)#invoke from main folder

    where_glint = glint(im_gray)
    
    im_gray = threshold(im_gray, thresh_v=73)
    where_pupil = pupil(im_gray)

    im = gray2bgr(im_gray)
    
    mark(im, where_glint)
    
    mark(im, where_pupil, color='blue')
    
    while(1):
        cv2.imshow('Pupil(blue) and glint(red) detection, exit with "q" or "esc"', im)
        k = cv2.waitKey(0) & 0xFF
        if k == 27 or k == ord('q'):
            break

    cv2.destroyAllWindows()

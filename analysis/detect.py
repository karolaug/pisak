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

# author: Sasza Kijek
# e-mail: saszasasha@gmail.com
# University of Warsaw 2013

import cv2
import numpy as np

def glint(image):
    '''
    TO DO!
    '''
    where = cv2.goodFeaturesToTrack(image, 2, 0.0001, 20)
    #TODO: add constrain of max distance
    if where != None:
        where = np.array([where[i][0] for i in xrange(where.shape[0])])
        return where
    else:
        return None

def pupil(image):
    '''
    TO DO!
    '''
    circles = cv2.HoughCircles(image, cv2.cv.CV_HOUGH_GRADIENT, 1, 100, 
                               param1=50, param2=10, minRadius=20, maxRadius=70)
    if circles != None:
        circles = np.uint16(np.around(circles))
        return circles[0] #list of x-es,y-es and radiuses 
    else:
        return None

if __name__ == '__main__':
    im_gray = cv2.imread('../examples/eyeIR.png', 0) #make it work always
    
    where_glint = glint(im_gray)
    
    ret, im_gray = cv2.threshold(im_gray, 73, 255, cv2.THRESH_TRUNC)
    where_pupil = pupil(im_gray)

    im = cv2.cvtColor(im_gray, cv2.COLOR_GRAY2BGR)
    
    for cor in where_glint:
        cv2.circle(im, tuple(cor), 10, (0, 0, 255), 3)

    for cor in where_pupil:
        cv2.circle(im, tuple(cor[:2]), cor[2], (255, 0 , 0), 3)
    
    while(1):
        cv2.imshow('Pupil(blue) and glint(red) detection, exit with "q" or "esc"', im)
        k = cv2.waitKey(0) & 0xFF
        if k == 27 or k == ord('q'):
            break

    cv2.destroyAllWindows()

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
    Function detects glint on the retina, based on the func 
    cv2.goodFeaturesToTrack.

    Parameters:
    -----------
    image - image of the eye where the glints are supposed to be detected
    Optional:
      maxCorners - how many glints should it detect, default is 2
      quality - minimal accepted quality of image corners
      minDist - minimum distance between the detected glints, default is 20
      mask - area of the image that should be used for glint detection, 
      default is None so it looks through the whole picture
      blockSize - size of an average block for computing a derivative
      covariation matrix over each pixel neighborhood

    for more info on parameters check the docs for opencv and 
    goofFeaturesToTrack

    Returns:
    --------
    where - array of coordinates(a list [x, y]) for found glints
    '''
    where = cv2.goodFeaturesToTrack(image, maxCorners=maxCorners, 
                                    qualityLevel=quality, minDistance=minDist,
                                    mask=mask, blockSize=blockSize)
    #TODO: add constrain of max distance
    if where != None:
        where = np.array([where[i][0] for i in xrange(where.shape[0])])
    return where

def pupil(image, dp=1, minDist=100, param1=50, param2=10, minRadius=20, 
          maxRadius=70):
    '''
    Function detects pupil on the image of an eye, based on the func 
    cv2.HoughCircles.

    Parameters:
    -----------
    image - image of the eye where the pupil is supposed to be detected
    Optional:
      dp - inverse ratio of the accumulator resolution to the image's,
      default 1
      minDist - minimum distance between found circles, default 100
      param1 - higher threshold for the Canny edge detector, default 50
      param2 - accumulator threshold for the circles centers, smaller it is,
      more false positives, default 10
      minRadius - minimal radius of the detected circle, default 20
      maxRadius - maximal radius of the detected circle, default 70
    
    for more info on parameters check the docs for opencv and HoughCircles

    Returns:
    --------
    where - array of coordinates and the radius of the circle(a list 
    [x, y, z] for found pupils
    '''
    circles = cv2.HoughCircles(image, cv2.cv.CV_HOUGH_GRADIENT, dp, minDist, 
                               param1=param1, param2=param2, 
                               minRadius=minRadius, maxRadius=maxRadius)
    if circles != None:
        circles = np.uint16(np.around(circles))[0] 
    return circles

if __name__ == '__main__':
    from processing import threshold, gray2bgr, bgr2gray, mark

    im_gray = cv2.imread('../../pictures/eyeIR.png', 0)

    where_glint = glint(im_gray)
    
    im_bw = threshold(im_gray, thresh_v=73)
    where_pupil = pupil(im_bw)

    im = gray2bgr(im_gray)
    
    mark(im, where_glint)
    
    mark(im, where_pupil, color='blue')
    
    while(1):
        cv2.imshow('Pupil(blue) and glint(red) detection, exit with "q" or "esc"', im)
        k = cv2.waitKey(0) & 0xFF
        if k == 27 or k == ord('q'):
            break

    cv2.destroyAllWindows()

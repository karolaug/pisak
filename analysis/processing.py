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

thresholds = {'otsu' : cv2.THRESH_OTSU, 'bin' : cv2.THRESH_BINARY, 
              'bin_inv' : cv2.THRESH_BINARY_INV, 
              'zero' : cv2.THRESH_TOZERO, 'zero_inv' : cv2.THRESH_TOZERO_INV,
              'trunc' : cv2.THRESH_TRUNC}

adaptiveMethods = {'gaussian' : cv2.ADAPTIVE_THRESH_GAUSSIAN_C, 
                   'mean' : cv2.ADAPTIVE_THRESH_MEAN_C}

def bgr2gray(imageBGR):
    '''Convert color image(BGR) to gray image.'''
    return cv2.cvtColor(imageBGR, cv2.COLOR_BGR2GRAY)

def gray2bgr(imageGRAY):
    '''Convert gray image to color image(BGR).'''
    return cv2.cvtColor(imageGRAY, cv2.COLOR_GRAY2BGR)

def threshold(image, thresh_v=25, max_v=255, thresh_type='trunc'):
    '''
    Threshold the image.

    Parameters:
    -----------
    image - 2d 8-bit array depicting an image in one-channel color(ex. grayscale)
    thresh_v - value of threshold cut-off
    max_v - maximal value when thresholding, relevant only if thresh_type is 'bin' or 'bin_inv'
    thresh_type - type of thresholding, possible 'otsu', 'bin', 'bin_inv', 'zero', 'zero_inv', 'trunc'
    
    For corresponding threshold types description see docs.opencv.org:
    {'otsu' : cv2.THRESH_OTSU, 
     'bin' : cv2.THRESH_BINARY, 'bin_inv' : cv2.THRESH_BINARY_INV, 
     'zero' : cv2.THRESH_TOZERO, 'zero_inv' : cv2.THRESH_TOZERO_INV,
     'trunc' : cv2.THRESH_TRUNC}
    '''
    thresh_v = int(thresh_v)
    max_v = int(max_v)

    ret, thresholded_image = cv2.threshold(image, thresh_v, max_v, 
                                           thresholds[thresh_type])
    return thresholded_image


def adaptiveThreshold(image, max_v=255, adaptiveMethod='gaussian', 
                      thresh_type='bin', blockSize=33, 
                      subtConstant=50):
    '''
    Threshold the image using adaptive methods.
	
    Parameters:
    -----------
    image - 2D array depicting an image in one-scale color(ex. grayscale)
    max_v - maximal value to be used in threshold
    adaptiveMethod - method used for thresholding, possible 'gaussian' or 'mean'
    thresh_type - prethresholding, possible thresholds 'bin'(binary) or 'bin_inv'(inversed binary)
    blockSize - Size of a pixel neighborhood that is used to calculate a threshold value, the size must be an odd number.
    subtConstant - a constant that will be subtracted from mean or weighted mean(depending on adaptiveMethod chosen)

    For corresponding adaptive methods see docs.opencv.org:
    {'gaussian' : cv2.ADAPTIVE_THRESH_GAUSSIAN_C, 
     'mean' : cv2.ADAPTIVE_THRESH_MEAN_C}
    '''
    
    max_v = int(max_v)
    blockSize = int(blockSize)
    subtConstant = int(subtConstant)

    if thresh_type is not 'bin' and thresh_type is not 'bin_inv':
        raise AttributeError('thresh_type may be "bin" or "bin_inv" here.')

    return cv2.adaptiveThreshold(image, max_v, adaptiveMethods[adaptiveMethod], 
                                 thresholds[thresh_type], blockSize, 
                                 subtConstant)

if __name__ == '__main__':
    im = cv2.imread('examples/eyeIR.png', -1)

    im_gray = bgr2gray(im)

    im_back = gray2bgr(im_gray)

    #for depicting that there are 3 channels
    im_back[0:10, :] = (255, 0, 0)
    im_back[-10:-1, :] = (0, 255, 0)
    im_back[:, 0:10] = (0, 0, 255)
    im_back[:, -10:-1] = (0, 0, 255)

    im_thresh = threshold(im_gray)

    im_thresh_adapt = adaptiveThreshold(im_gray)

    pics = {'original image' : im, 'one-channel gray image' : im_gray, 
            'converted back to 3 channel' : im_back, 
            'thresholded' : im_thresh, 
            'thresholded adaptively' :im_thresh_adapt}

    while(1):
        [cv2.imshow(descp, pic) for descp, pic in pics.iteritems()]
        
        k = cv2.waitKey(0) & 0xFF
        if k == 27 or k == ord('q'):
            break

        cv2.destroyAllWindows()

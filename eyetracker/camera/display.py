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

from cv2 import namedWindow, CV_WINDOW_AUTOSIZE, imshow

from ..analysis.detect import pupil, glint
from ..analysis.processing import threshold, mark, gray2bgr, bgr2gray

def drawGlint(image):
    '''
    Function takes an image, converts it to grayscale if it is not,
    detects glint and draws it on a new image.

    Parameters:
    -----------
    image - image where the glint is to be detected
    
    Returns:
    --------
    color image - returns a numpy array in a bgr scale with the glint 
    marked in blue
    '''
    if len(image.shape) == 3:
        image = bgr2gray(image)
    where_glint = glint(image)
    bgr = gray2bgr(image)
    mark(bgr, where_glint)
    return bgr

def drawPupil(image, thres):
    '''
    Function takes an image, applies 'trunc' threshold(cv2.THRESH_TRUNC),
    detects pupil and draws it on a new image.

    Parameters:
    -----------
    image - image where the pupil is to be detected
    thres - value of the threshold
    
    Returns:
    --------
    color image - returns a numpy array in a bgr scale with the pupil 
    marked in red
    '''
    if len(image.shape) == 3:
        image = bgr2gray(image)
    thresholded = threshold(image, thresh_v=thres)
    where_pupil = pupil(thresholded)
    bgr = gray2bgr(thresholded)
    mark(bgr, where_pupil, color='blue')
    return bgr

def displayImage(image, where='new'):
    '''
    Function displays the image in a new window or in the pointed window.
    Returns the displayed image as a numpy array.

    Parameters:
    -----------
    image - numpy array being an image to be displayed
    where - name of the window as string in which the image is to be
    displayed, not providing the name will create a new one
    
    Returns:
    -----------
    image - numpy array being an displayed image.
    '''
    if where == 'new':
        namedWindow('new', flags=CV_WINDOW_AUTOSIZE)
        imshow(where, image)
    return image
            
if __name__ == '__main__':
    from cv2 import imread, waitKey

    im = imread('../../pictures/eyeIR.png', 0)

    pupil = drawPupil(im, 35)
    glint = drawGlint(im)

    displayImage(pupil, where='Pupil detection.')
    displayImage(glint, where='Glint detection.')
    waitKey(0)

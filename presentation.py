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

from sys import argv
import cv2
import numpy as np
from scipy.stats import mode
from analysis.processing import threshold, bgr2gray, gray2bgr, mark
from analysis.detect import pupil

def nothing(x):
    pass

def get_middle(cap, windowName):
    cv2.namedWindow('Look at the middle')
    middle = np.zeros((1080, 1920, 3), np.uint8)
    middle[500:580, 920:1000] = (0, 0, 255)
    press = raw_input('After key press please look in front of yourself.')
    while(1):
        ret, frame = cap.read()
        
        frame_gray = bgr2gray(frame)
        frame_thresh = th
        
        cv2.imshow('Look at the middle', middle)
        cv2.imshow('camera', frame)

if __name__ == '__main__':
    cv2.namedWindow('From camera')
    cv2.namedWindow('Choice')
    cv2.namedWindow('camera')

    cv2.createTrackbar('threshold', 'From camera', 0, 255, nothing)
    cap = cv2.VideoCapture(int(argv[1]))
    
    cv2.createTrackbar('threshold', 'camera', 0, 255, nothing)
    

    choice = np.zeros((480, 640, 3), np.uint8)

    cv2.namedWindow('Look at the middle')
    
    middle = np.zeros((1080, 1920, 3), np.uint8)
    middle[530:550, 950:970] = (0, 0, 255)
    press = raw_input('After key press please look in front of yourself.')
    
    middles = np.zeros(2, np.uint8)

    while(1):
        ret, frame = cap.read()
        
        frame_gray = bgr2gray(frame)
        
        thresh = cv2.getTrackbarPos('threshold', 'camera')
        
        frame_thresh = threshold(frame_gray, thresh_v=thresh)

        where_pupil = pupil(frame_thresh, param2=20, minRadius=20)

        mark(frame, where_pupil)
        
        cv2.imshow('Look at the middle', middle)
        cv2.imshow('camera', frame)

        if where_pupil is not None and len(where_pupil) == 1:
            middles = np.vstack((middles, where_pupil[0][:2]))

        if cv2.waitKey(1) & 0xFF == ord('q') or len(middles) == 1000:
            break

    cv2.destroyWindow('Look at the middle')
    cv2.destroyWindow('camera')


    middle = mode(middles)[0][0]

    while(1):

        ret, frame = cap.read()
        
        frame_gray = bgr2gray(frame)
        
        thresh = cv2.getTrackbarPos('threshold', 'From camera')
        
        frame_thresh = threshold(frame_gray, thresh_v=thresh)

        where_pupil = pupil(frame_thresh, param2=20, minRadius=20)

        mark(frame_thresh, where_pupil)

        if where_pupil is not None and len(where_pupil) == 1:
            if where_pupil[0][0] > middle[0] + 30:
                x = -1
            elif where_pupil[0][0] < middle[0] - 30:
                x = 1
            else:
                x = 0
            if where_pupil[0][1] > middle[1] + 30:
                y = 1
            elif where_pupil[0][1] < middle[1] - 30:
                y = -1
            else:
                y = 0
       
            if x == 0 and y == 0:
                choice = np.zeros((480, 640, 3), np.uint8)
                choice[160:320, 213:426] = (0, 255, 0)
            else:
                choice = np.zeros((480, 640, 3), np.uint8)
                choice[160+(y*160):320+(y*160), 213+(x*213):426+(x*213)] = (0, 255, 0)

        frame_backBGR = gray2bgr(frame_thresh)

        cv2.imshow('From camera', frame_backBGR)

        cv2.imshow('Choice', choice)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

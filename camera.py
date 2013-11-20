#!/usr/bin/python
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

class Camera(object):
    def __init__(self, camera, **kwargs):
        self.camera = int(camera)
        self.cap = cv2.VideoCapture(self.camera)
        if kwargs:
            for propID, value in kwargs.iteritems():
                self.camera.set(propID, value)
        first_frame = self.frame() #initialize at the start so that no loss of time occurs later on, not needed later on so no 'self'
    
    def frame(self):
        if self.cap.isOpened:
            return self.cap.read()[1]
        else:
            print 'Cap is not opened.'

    def close(self):
        self.cap.release()

    def reOpen(self, cameraIndex):
        self.cap.open(self.camera)
        first_frame = self.frame() #same purpose as in __init__


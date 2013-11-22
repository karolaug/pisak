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

from cv2 import VideoCapture

class Camera(object):
    '''
    Class governing the communication with the camera.

    Parameters:
    -----------
    camera - the index of the camera, best taken from func lookForCameras,
    from eyetracker.camera.capture
    dic - dic{propID : value}, to check corresponding propIDs check
    opencv documentation: http://docs.opencv.org/modules/highgui/doc/ under
    the term VideoCapture::get - they will be set in the moment of object
    creation.

    Defines:
    --------
    self.camera - index of the camera
    self.cap - capturing object

    self.frame - returns a frame from camera

    self.close - closes cap
    self.reOpen - reopens cap
    '''
    def __init__(self, camera, dic=None):
        self.camera = int(camera)
        self.cap = VideoCapture(self.camera)
        if dic:
            for propID, value in dic.iteritems():
                self.cap.set(propID, value)
        first_frame = self.frame() #initialize at the start so that no loss of time occurs later on, not needed later on so no 'self'
    
    def frame(self):
        '''
        Read frame from camera.

        Returns:
        --------
        frame - numpy array being a frame from camera
        '''
        if self.cap.isOpened:
            return self.cap.read()[1]
        else:
            print 'Cap is not opened.'
            return None

    def set(self, **kwargs):
        '''
        Set camera parameters.

        Parameters:
        -----------
        **kwargs - {propID : value}
        '''
        for propID, value in kwargs.iteritems():
            self.cap.set(propID, value)

    def close(self):
        '''
        Closes cap, you can reopen it with self.reOpen.
        '''
        self.cap.release()

    def reOpen(self, cameraIndex):
        '''
        Reopens cap.
        '''
        self.cap.open(self.camera)
        first_frame = self.frame() #same purpose as in __init__


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

from glob import iglob

def lookForCameras():
    ''' Function looks for cameras available cameras.

    Returns
    --------
    dic : {Camera_i , index}
        where i is the 1,2,3 etc. and index
        is an int corresponding to the camera that should be passed on
        to cv2.VideoCapture or to class Camera from eyetracker.camera.camera.
    '''
    listOfCameras = {''.join(['Camera_', str(i+1)]) : int(i)
                     for i, cam in enumerate(iglob('/dev/video*'))}
    #listOfCameras['dummy'] = None
    return listOfCameras

if __name__ == '__main__':
    print 'Found cameras:\n', lookForCameras()

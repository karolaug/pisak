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

def find_purkinje(purkinje1, purkinje2):
    '''
    Find virtual purkinje image in a two IR LED setting.

    Parameters:
    -----------
    purkinje1 - tuple of x, y being the coordinates of first purkinje image
    purkinje2 - as above but of the second purkinje image
    '''
    purkinje = tuple(sum(coord)/2 for coord in zip(purkinje1, purkinje2))
    return purkinje

if __name__ == '__main__':
    '''to do!'''

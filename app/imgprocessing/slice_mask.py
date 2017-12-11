'''
Copyright (C) 2015 Jeison Pacateque, Santiago Puerto, Wilmar Fernandez

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>
'''

import numpy as np


def sector_mask(shape, centre=(50, 50), radius=50, angle_range=(0, 360)):
    """
    This method provides a circular mask over a numpy array (image), its purpose
    is to differentiate the air void pixels within the cylindrical toymodel
    from the air void space outward.

    :param shape: shape of the image
    :type shape: two-dimensional tuple of integers
    :param centre: point from where the circular mask is applied
    :type centre: two-dimensional tuple of integers
    :param float radius: length of the radius for the circular mask
    :param angle_range: circular sector where the mask is applied, the whole
        circle by default
    :type angle_range: two-dimensional tuple of integers
    :return: mask for a circular sector
    :rtype: 2d boolean numpy array
    """

    x,y = np.ogrid[:shape[0],:shape[1]]
    cx,cy = centre
    tmin,tmax = np.deg2rad(angle_range)

    # ensure stop angle > start angle
    if tmax < tmin:
            tmax += 2*np.pi

    # convert cartesian --> polar coordinates
    r2 = (x-cx)*(x-cx) + (y-cy)*(y-cy)
    theta = np.arctan2(x-cx,y-cy) - tmin

    # wrap angles between 0 and 2*pi
    theta %= (2*np.pi)

    # circular mask
    circmask = r2 <= radius*radius

    # angular mask
    anglemask = theta <= (tmax-tmin)

    return circmask*anglemask

def apply_mask(collection):
    col_length = len(collection)
    for i in range(col_length):
        mask = sector_mask(collection[i].shape)
        collection[i][~mask] = -1

    return collection

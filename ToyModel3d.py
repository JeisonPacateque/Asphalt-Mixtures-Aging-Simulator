# -*- coding: utf-8 -*-
"""
Created on Tue May 27 09:10:49 2014

@author: sjdps
"""

from mayavi import mlab
#from tvtk.api import tvtk


def ToyModel3d(sample):
    src = mlab.pipeline.scalar_field(sample)
    mlab.pipeline.iso_surface(src, contours=[1], opacity=0.4)
    mlab.pipeline.iso_surface(src, opacity=0.4)
    #
    mlab.pipeline.image_plane_widget(src,
                                plane_orientation='x_axes',
                                slice_index=10,
                            )
    #fig=mlab.pipeline.iso_surface(src, color=(1.0,1.0,0.0), contours=[0.1, ], opacity=0.3)
    #mlab.pipeline.iso_surface(src, color=(1.0,1.0,1.0),contours=[-2, ], opacity=0.3)
    mlab.show()
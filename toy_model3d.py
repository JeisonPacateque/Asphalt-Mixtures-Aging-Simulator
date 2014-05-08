# -*- coding: utf-8 -*-

import glob
import numpy as np
from mayavi import mlab
from tvtk.api import tvtk
from file_loader import FileLoaderNPY

loader = FileLoaderNPY()
mypath = '/home/sjdps/MUESTRA/66719/6/Segmented_and_reduced_100/'
loader.load_path(mypath)
archives = loader.get_collection()

temp = archives[0]
#print temp
len_x = temp.shape[0]
len_y = temp.shape[1]
len_z = len(archives)/16



s = np.empty((len_x, len_y, len_z))

for i in xrange(len_z):
    s[..., ..., i] = archives[i]


src = mlab.pipeline.scalar_field(s)
mlab.pipeline.iso_surface(src, contours=[1], opacity=0.4)
mlab.pipeline.iso_surface(src, opacity=0.4)
#
mlab.pipeline.image_plane_widget(src,
                            plane_orientation='z_axes',
                            slice_index=10,
                        )
#fig=mlab.pipeline.iso_surface(src, color=(1.0,1.0,0.0), contours=[0.1, ], opacity=0.3)
#mlab.pipeline.iso_surface(src, color=(1.0,1.0,1.0),contours=[-2, ], opacity=0.3)
mlab.show()
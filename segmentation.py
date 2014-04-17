# -*- coding: utf-8 -*-
"""
Created on Mon Apr 14 19:37:32 2014

@author: sjdps
"""

import matplotlib.pyplot as plt
import dicom 
import pylab
import numpy as np
from scipy import ndimage
#from scipy.stats import cumfreq
from matplotlib import colors
#from scipy.cluster.vq import kmeans,vq
#from skimage.filter import threshold_adaptive
#from skimage.segmentation import felzenszwalb, slic, quickshift
#from skimage.filter import canny
#from skimage.filter import rank
#from skimage.morphology import disk
from skimage.segmentation import *


def read_image(image):
    #ds=dicom.read_file('/home/santiago/Documentos/Pruebas Python/PruebasGraficas/00490278')
    ds=dicom.read_file('/home/sjdps/MUESTRA/66719/6/00490278')
    arreglo=ds.pixel_array
    fixed=arreglo[35:485, 35:485]
    return fixed

def reduction(img, factor):
#    factor_zoom=(100.0/450) #El punto le indica al interprete que el resultado sera float
    img_reduced=ndimage.interpolation.zoom(img, factor)
        
    #dado que la imagen se rota al reducirla, se 
    reduced=ndimage.rotate(img_reduced, 180, reshape=False)
    reduced=np.fliplr(reduced)
    
    return reduced

def clasify(img):
    for elem in np.nditer(img, op_flags=['readwrite']):
        if elem[...]<=-1200:
            elem[...]=0
        elif -500<elem[...]<1600:
            elem[...]=1
        elif elem[...]>=1600:
            elem[...]=2
    
    return img 

def view(fixed, img_clas):
    cmap = colors.ListedColormap(['white', 'blue', 'red'])
    bounds=[0, 1, 2, 3]
    norm = colors.BoundaryNorm(bounds, cmap.N)
    f = pylab.figure()
 
    f.add_subplot(1, 2, 1)  # this line outputs images on top of each other       
    implot=plt.imshow(fixed)
    #implot.set_cmap('afmhot')
#    implot.set_cmap('BrBG')
    #implot.set_cmap('spectral')
#    implot.set_cmap('seismic')
    implot.set_cmap('seismic')
    plt.colorbar()
    f.add_subplot(1, 2, 2)  # this line outputs images side-by-side
#    img = plt.imshow(fixed, interpolation='nearest', origin='lower', cmap=cmap, norm=norm)
#    img = plt.imshow(img_clas, interpolation='nearest', origin='lower', cmap=cmap, norm=norm)
    img = plt.imshow(img_clas)
#    img.set_cmap('seismic')
    # make a color bar
#    plt.colorbar(img, cmap=cmap, norm=norm, boundaries=bounds, ticks=[0, 1, 2, 3])
    
    pylab.show()

def histograma(img_red):   
#    values, bins=np.histogram(img_red, bins=3)
#    print bins
#    print values
#    plt.plot(values, bins[:-1], lw=2)
#    plt.show()
    pylab.hist(img_red, bins=3, histtype='bar')
    pylab.show()



image ='/home/sjdps/MUESTRA/66719/6/00490278'          
fixed_arreglo = read_image(image)

factor_zoom = (100.0/450)
img_red = reduction(fixed_arreglo, factor_zoom)
histograma(fixed_arreglo)
#img_red = clasify(img_red)
label=felzenszwalb(img_red)
img_red=mark_boundaries(img_red, label)
view(fixed_arreglo, img_red)
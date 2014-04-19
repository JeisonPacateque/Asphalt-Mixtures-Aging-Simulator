# -*- coding: utf-8 -*-
"""
Created on Mon Apr 14 19:37:32 2014

@author: sjdps
"""

import matplotlib.pyplot as plt
import dicom 
import numpy as np
from scipy import ndimage
from matplotlib import colors
from sklearn import cluster


def read_image(image):
    #ds=dicom.read_file('/home/santiago/Documentos/Pruebas Python/PruebasGraficas/00490278')
    ds=dicom.read_file('/home/sjdps/MUESTRA/66719/6/00490278')
    arreglo=ds.pixel_array
    fixed=arreglo[35:485, 35:485]
    return fixed

def reduction(img, factor):
    img_reduced=ndimage.interpolation.zoom(img, factor)
        
    #dado que la imagen se rota al reducirla, se 
    reduced=ndimage.rotate(img_reduced, 180, reshape=False)
    reduced=np.fliplr(reduced)
    
    return reduced

def view(fixed, img_clas, values):
    
#    cmap = colors.ListedColormap(['white', 'blue', 'red'])
#    bounds=values
#    norm = colors.BoundaryNorm(bounds, cmap.N)
    
    f = plt.figure()
    f.add_subplot(1, 2, 1)  # this line outputs images on top of each other       
    implot=plt.imshow(fixed, cmap='seismic')
    plt.colorbar(implot, cmap='seismic')
    
    f.add_subplot(1, 2, 2)  # this line outputs images side-by-side
    img = plt.imshow(img_clas, 'seismic')

    # make a color bar
    plt.colorbar(img, cmap='seismic')
    
    plt.show()

def histograma(img_red):   
#    values, bins=np.histogram(img_red, bins=3)
#    print bins
#    print values
#    plt.plot(values, bins[:-1], lw=2)
#    plt.show()
    pl.hist(img_red, bins=3, histtype='bar')
    pl.show()

def clasify(img):
    n_clusters = 3 # number of clusters: void, aggregate and mastic
    
    #convert the image to a linear array
    X = img.reshape((-1, 1))  # We need an (n_sample, n_feature) array
    
    k_means = cluster.KMeans(n_clusters=n_clusters, n_init=4)#create the object kmeans
    k_means.fit(X)# execute kmeans over the image
    
    values = k_means.cluster_centers_.squeeze() #extractthe valyes (centroids)
    labels = k_means.labels_

    
    # create an array from labels and values
    img_segmented = np.choose(labels, values) #label the image
    img_segmented.shape = img.shape #reshape the image with original dimensions
    
    return img_segmented, values
    



ruta ='/home/sjdps/MUESTRA/66719/6/00490278'          
fixed_arreglo = read_image(ruta)

factor_zoom = (100.0/450)


#histograma(fixed_arreglo)

img_seg, values = clasify(fixed_arreglo)

img_red = reduction(img_seg, factor_zoom)
view(img_seg, img_red, values)
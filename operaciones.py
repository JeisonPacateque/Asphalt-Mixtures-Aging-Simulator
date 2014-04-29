# -*- coding: utf-8 -*-
"""
Created on Mon Apr 28 21:34:04 2014

@author: santiago
"""
import matplotlib.pyplot as plt
import dicom
import numpy as np
from scipy import ndimage
from matplotlib import colors
from sklearn import cluster


def read_image(image):
    #ds=dicom.read_file('/home/santiago/Documentos/Pruebas Python/PruebasGraficas/00490278')
    #ds=dicom.read_file('/home/sjdps/MUESTRA/66719/6/00490278')
    ds=dicom.read_file(image)
    arreglo=ds.pixel_array
    fixed=arreglo[35:485, 35:485]
    return fixed

def reduction(img, factor, values):

#    for elem in np.nditer(img, op_flags=['readwrite']):
#        if elem[...]<=values[0]:
#            elem[...]=int(0)
#        elif values[0]<elem[...]<values[1]:
#            elem[...]=int(1)
#        elif elem[...]>=values[2]:
#            elem[...]=int(2)

    reduced=ndimage.interpolation.zoom(img, factor)

    #dado que la imagen se rota al reducirla
    reduced=ndimage.rotate(reduced, 180, reshape=False)
    reduced=np.fliplr(reduced)

    return reduced

def view(original, segmentada, reducida, values):

    f = plt.figure()

    f.add_subplot(1, 3, 1)  # Imagen original
    plt.imshow(original, cmap='seismic')
#    plt.colorbar()

    f.add_subplot(1, 3, 2)  # Imagen segmentada: K-Means
    plt.imshow(segmentada, cmap='seismic')
#    plt.colorbar()

    f.add_subplot(1, 3, 3)  # Imagen reducida por interpolacion zoom
    plt.imshow(reducida, interpolation='nearest', origin='lower', cmap='seismic' )
#    plt.colorbar()

    plt.show()

def histograma(img_red):
    plt.hist(img_red, bins=3, histtype='bar')
    plt.show()

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

    valores=sorted(values)

    return img_segmented, valores

#====================================================================#

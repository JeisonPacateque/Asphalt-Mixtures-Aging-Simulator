# -*- coding: utf-8 -*-
"""
Created on Mon Apr 14 19:37:32 2014

@author: sjdps
"""

import matplotlib.pyplot as plt
import dicom
import numpy as np
from scipy import ndimage
from sklearn import cluster


class Segmentation(object):

    def read_image(self, ruta):
        # we could provide slices as parameters in order to
        # customize the dimension of fixed
        ds = dicom.read_file(ruta)
        arreglo = ds.pixel_array  # get the data (image) from the file
        fixed = arreglo[35:485, 35:485]  # cut the image

        return fixed

    def reduction(self, img, factor=(100./450.)):

        reduced = ndimage.interpolation.zoom(img, factor)

        # since the image is turned over when it is reduced
        # we should turn it over again
        reduced = ndimage.rotate(reduced, 180, reshape=False)
        reduced = np.fliplr(reduced)

        return reduced[1:, 1:]  # return and cut "noise"

    def view(self, original, segmented, reduced, values):

        f = plt.figure()

        f.add_subplot(1, 3, 1)  # Original image
        plt.imshow(original, cmap='seismic')
    #    plt.colorbar()

        f.add_subplot(1, 3, 2)  # Segmented image  by K-means
        plt.imshow(segmented, cmap='seismic')
    #    plt.colorbar()

        f.add_subplot(1, 3, 3)  # Reduced image
        plt.imshow(reduced, interpolation='nearest',
                   origin='lower', cmap='seismic')
    #    plt.colorbar()

        plt.show()

    def histograma(self, img_red):

        plt.hist(img_red, bins=3, histtype='bar')
        plt.show()

    def clasify(self, img):
        n_clusters = 3  # number of clusters: void, aggregate and mastic

        # convert the image to a linear array
        X = img.reshape((-1, 1))  # We need an (n_sample, n_feature) array

        k_means = cluster.KMeans(n_clusters=n_clusters,
                                 n_init=4)  # create the object kmeans
        k_means.fit(X)  # execute kmeans over the image

        # extract the valyes (centroids)
        values = k_means.cluster_centers_.squeeze()
        labels = k_means.labels_

        print labels

        # create an array from labels and values
        img_segmented = np.choose(labels, values)  # label the image
        img_segmented.shape = img.shape  # reshape with original dimensions

        # Since the values returned by k-means are always different, we
        # sort them to ease later labeling...
        valores = sorted(values)

        return img_segmented, valores

if __name__ == '__main__':

    ruta1 = '/home/sjdps/MUESTRA/66719/6/00490278'
    ruta2 = '/home/santiago/Documentos/Pruebas Python/PruebasGraficas/00490278'

    seg1 = Segmentation()
    img_org = seg1.read_image(ruta1)
    img_temporal = img_org.copy()  # Copy of the image to process

    img_seg, values = seg1.clasify(img_org)  # Segment orginal image

    # Reduce img_temporal (avoid manipulation of the variable)
    img_red = seg1.reduction(img_temporal)

    red_seg, val_red = seg1.clasify(img_red)  # Segment reduced image

    seg1.view(img_org, img_seg, red_seg, val_red) # Show results
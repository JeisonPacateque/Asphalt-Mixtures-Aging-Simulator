'''
..  Copyright (C) 2015 Jeison Pacateque, Santiago Puerto

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

from matplotlib import pyplot, colors
import numpy as np
import time
from scipy import ndimage
from sklearn import cluster
from slice_mask import sector_mask

class Segmentation(object):

    def __init__(self):
        r"""
        This class  provides the methods to reduce and segment the images of the
        toy model. It assumes that the set of Dicom files that represents the toy
        model have been tranformed in an array of numpy.
        """

    def reduction(self, img, factor=(100. / 450.)):
        r"""
        This method reduces the set of images of the toymodel by a given scale
        factor or zoom factor, using the C-Spline algorithm which is provided
        by the ndimage module of scipy

        C-Spline algorithm consists in funding a function which is the linear
        combination of piecewise definened functions known as Basis Splines
        (B-Splines), which are smooth functions whose first, second and third
        derivative pass through one point of the given discrete set:

        .. math::
            \beta ^3(x) =\begin{cases}
            \frac{2}{3} - |x|^2 + \frac{|x|^3}{2}  &  0\leqslant |x|< 1 \\
            \frac{(2-|x|)^3}{6} & 1\leqslant |x| < 2 \\
            0 & 2\leqslant |x|
            \end{cases}

        The linear combination of the B-Spline functions can be expressed by the
        next equation:

        .. math::
            \zeta (x) = \sum _{k\in Z} c(K)\beta ^n(x-K)

        :param img: representation of the toy model
        :type img: 3d numpy array
        :param float factor: zoom factor in which the image is reduced
        :return: the image rescaled
        :rtype: 3d numpy array
        """
        print "Running reduction..."
        start_time = time.time()  # Measures file loading time
        reduced = ndimage.interpolation.zoom(img, factor, output=np.int16)
        # since the image is turned over when it is reduced
        # we should turn it over again
        reduced = ndimage.rotate(reduced, 180, reshape=False)
        reduced = np.fliplr(reduced)

        end_time = time.time()  # Get the time when method ends
        print "Reduction completed in ", str(end_time - start_time), " seconds."

        return reduced[1:, 1:]  # return and cut "noise"

    def view(self, original, segmented, reduced):
        r"""
        This method is implemented for test purposes, it takes as arguments
        an untreated slice, a segmented slice and a reduced and segmented
        slice showing its differences on screen using a matplotlib figure

            view(original, segmented, reduced)
        """

        f = pyplot.figure()
        levels = [0, 1, 2]
        colores = ['red', 'white', 'blue', 'red']
        cmap, norm = colors.from_levels_and_colors(levels, colores, extend='both')

       # org = self.sample_mask(original) #Mask irelevant data

        f.add_subplot(1, 3, 1)  # Original image
        pyplot.imshow(original, cmap='binary', interpolation='nearest')
        pyplot.colorbar()

        f.add_subplot(1, 3, 2)  # Segmented image  by K-means
        pyplot.imshow(segmented, interpolation='nearest', cmap=cmap, norm=norm)
        pyplot.colorbar()

        f.add_subplot(1, 3, 3)  # Reduced image
        pyplot.imshow(reduced, interpolation='nearest',
                      origin='lower', cmap = cmap, norm = norm)
        pyplot.colorbar()
        pyplot.show()

    def histogram(self, img_red):
        r"""
        Plots an histogram of the materials distibution over the toy model
        using matplotlib. It is neccesary to reduce the toy model before
        plotting the histogram. For test porpuses

            histogram(reduced_toymodel)
        """
        pyplot.hist(img_red, bins=3, histtype='bar')
        pyplot.show()

    def clasify(self, img, normalize=True):
        r"""
        This method segments or clasify the values of the given image in three
        different groups of values, thus the different Hounsfield unit values
        found in the image are replaced by only three different values. If the
        parameter normalize is true, these values are:

        - **0** for the air-void
        - **1** for the mastic
        - **2** for the aggregates

        For this porpuse, a implementation of the K-means algorithm, provided
        by the cluster module of the Scikit-learn library, is used. K-means
        algorithm takes a dataset X of N values, and a parameter K specifies how
        many cluster to create. K-means finds evenly-spaced sets of points in
        subsets of Euclidean spaces called Voronoi diagrams. Each found partitions
        will be a uniformly shaped region called Voronoi cell, one for each
        material. This process is executed in two steps:

        *   The assign step consists in calculating a Voronoi diagram having a
            set of centroids :math:`\mu_n`. The clusters are updated to contain
            the closest points in distance to each centroid as it is described
            by the equation:

            .. math::
                c_k = \left \{ X_n:\left \| X_n -\mu_k \right \| \leqslant
                \left \| X_n - \mu_l \right \|\right \}

        *   The upadate step, given a set of clusters, recalculates the centroids
            as the means of all points belonging to a cluster:

            .. math::
                \mu_k = \frac{1}{C_k}\sum _{X_n\in C_k} Xn

        The k-means algorithm loops through the two previous steps until the
        assignments of clusters and centroids no longer change. The convergence
        is guaranteed but the solution might be a local minimum as shown in the
        next equation:

        .. math::
            \sum _{k=1}^K\sum _{X_n\in C_k}\left \| X_n - \mu_k \right \|^2 ,
            \text{with respect to } C_k, \mu_k

        :param img: a slice of the toy model
        :type img: 2d numpy array
        :param boolean normalize: If it is true, the segmentation mark the three
            group of values as 0, 1 and 2. If it is false, the marks are the
            default values generated by k-means.
        :return: the image segmented, with only three different possible values
        :rtype: 3d numpy array
        """

        n_clusters = 3  # number of clusters: void, aggregate and mastic

        # convert the image to a linear array
        X = img.reshape((-1, 1))  # We need an (n_sample, n_feature) array

        k_means = cluster.KMeans(n_clusters=n_clusters, n_init=4)  # create the object kmeans
        k_means.fit(X)  # execute kmeans over the image

        # extract the valyes (centroids)
        values_kmeans = k_means.cluster_centers_.squeeze()
        labels = k_means.labels_

        if normalize:
            # normalize values, so all slices have the same values
            values = values_kmeans.copy()
            values_kmeans = values_kmeans.tolist()
            values.sort()
            normalized_values = np.empty(len(values_kmeans))
            for i in xrange(len(values)):
                index = values_kmeans.index(values[i])
                normalized_values[index] = i
            # label the image with norma values [0, 1, 2, 3, ...]
            img_segmented = np.choose(labels, normalized_values)
        else:
            img_segmented = np.choose(labels, values_kmeans)

        img_segmented.shape = img.shape  # reshape with original dimensions
        convert_matrix = img_segmented.astype(np.int16)

        return convert_matrix

    def segment_all_samples(self, samples):
        r"""
        Take the given samples, uses K-Means algorithm with each sample slice
        and returns all the segmented samples. it also cuts irrelevant data
        corresponding to voids outside of the lenth of the radius of the toymodel

        :param samples: the set of slices of the toy model
        :type samples: list of 2d numpy arrays
        :return: the toy model with its materials classified in airvoids,
            mastic and aggregates.
        :rtype: list of 2d numpy arrays
        """

        start_time = time.time()  # Measures file loading t
        segmented = samples
        col_length = len(segmented)
        print "Running segmentation for", str(col_length), "samples..."

        for i in xrange(col_length):
            segmented[i] = self.clasify(segmented[i])

        for i in range(col_length):
            mask = sector_mask(segmented[i].shape)
            segmented[i][~mask] = -1

        end_time = time.time()  # Get the time when method ends
        print "Segmentation finished with", str(col_length), "samples in", \
        str(end_time - start_time), "seconds."

        return segmented

#----------------------------------------------------------------------------------

if __name__ == '__main__':
    import sys, os

    sys.path.insert(0, os.path.abspath('../'))

    from integration.file_loader import FileLoader

    loader = FileLoader()
    file_path = os.path.dirname('../')+'/samples/4/sample_20.dcm'

    segmentation = Segmentation()
    img_org = loader.single_dicom_read(file_path)
    img_temporal = img_org.copy()  # Copy of the image to process

    img_seg = segmentation.clasify(img_org)  # Segment original image

    # Reduce img_temporal (avoid manipulation of the variable)
    img_red = segmentation.reduction(img_temporal)

    red_seg = segmentation.clasify(img_red)  # Segment reduced image

    segmentation.view(img_org, img_seg, red_seg)  # Show results

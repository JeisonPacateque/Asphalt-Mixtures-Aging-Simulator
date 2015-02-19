'''
Copyright (C) 2015 Jeison Pacateque, Santiago Puerto

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
from file_loader import FileLoader
from slice_mask import sector_mask

class Segmentation(object):

    def __init__(self):
        """
        This class handle all the methods to reduce and segment the asphalt
        mixture reconstruction from Dicom images
        """
        self.loader = FileLoader()

    def reduction(self, img, factor=(100. / 450.)):
        """
        This method takes the numpy array representation of toyModel (img)
         and a zoom factor, returning the toymodel scaled for its posterior
         segmentation.

             reduction(toymodel, zoomfactor)

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
        """
        This method is implemented for test purposes, it takes as argument
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
        """
        Plots an histogram of the materials distibution over the toy model
        using matplotlib. It is neccesary to reduce the toy model before
        plotting the histogram

            histogram(reduced_toymodel)
        """
        pyplot.hist(img_red, bins=3, histtype='bar')
        pyplot.show()

    def clasify(self, img, normalize=True):
        """
        K-means algorithm implementation. Take a raw slice as an input returning
        it with the same size and proportions replacing all the Houndsfield unit
        values from X-Ray CT for the detected material id.
            0: For air-voids.
            1: For mastic.
            2: For aggregates.
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
        """Take all the samples, uses K-Means algorithm with each sample slice
        and returns the interpolated samples"""
        start_time = time.time()  # Measures file loading t
        segmented = samples
        col_length = len(segmented)
        print "Running segmentation for", str(col_length), "samples..."

        for i in xrange(col_length):
            segmented[i] = self.clasify(segmented[i])

        masked = self.sample_mask(segmented) #Mask irelevant data

        end_time = time.time()  # Get the time when method ends
        print "Segmentation finished with",str(col_length),"samples in", str(end_time - start_time), "seconds."

        return masked

    def sample_mask(self, sample):
        """Applies a mask to fit the form of the toy model"""
        for i in range(len(sample)):
            mask = sector_mask(sample[i].shape)
            sample[i][~mask] = -1

        return sample

    def get_sample_empty_pixels(self):
        return self.mask_empty_pixels


#----------------------------------------------------------------------------------

if __name__ == '__main__':

    import os
    file_path = os.path.dirname(os.path.abspath(__file__))+'/samples/4/sample_20.dcm'

    segmentation = Segmentation()
    img_org = segmentation.loader.single_dicom_read(file_path)
    img_temporal = img_org.copy()  # Copy of the image to process

    img_seg = segmentation.clasify(img_org)  # Segment original image

    # Reduce img_temporal (avoid manipulation of the variable)
    img_red = segmentation.reduction(img_temporal)

    red_seg = segmentation.clasify(img_red)  # Segment reduced image

    segmentation.view(img_org, img_seg, red_seg)  # Show results
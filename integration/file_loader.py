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

import os
import dicom
from matplotlib.pyplot import imread
import numpy as np
import re
from PIL import Image


class FileLoader(object):
    """
    This class have all the needed method to load all the Dicom files from the
    X-Ray CT scan, processing the images and create a reconstruction of the
    asphalt mixture using numpy data types.
    """

    def __init__(self):

        self.coleccion_imagenes = []  # Image list

    def get_collection(self):
        return self.coleccion_imagenes

    def human_key(self, key):
        """Method to 'Natural sort' a list"""
        parts = re.split('(\d*\.\d+|\d+)', key)
        return tuple((e.swapcase() if i % 2 == 0 else float(e))
                for i, e in enumerate(parts))

    def read_single_dicom(self, dicom_file):
        """Read a single DICOM file
        :return numpy array"""
        temp = dicom.read_file(dicom_file)  # Read the file as DICOM image
        px_array = temp.pixel_array  # Transform DICOM image as numpy array
        dicom_slice = px_array[35:485, 35:485] #Cut the slice to match draw area
        #print "Loaded", str(dicom_file)
        return dicom_slice

    def read_single_tiff(self, tiff_file):
        """Read a single TIFF file
        :return numpy array"""
        # im = Image.open(tiff_file)
        # im.show()
        # print im
        # imarray = np.array(im)
        # print imarray.shape, imarray
        # return imarray
        # im = imread(tiff_file)
        # print im.shape
        return imread(tiff_file)

    def load_path(self, path):
        """
        Load a whole folder of Dicom files and return a NumPy toyModel
        """
        try:
            # start_time = time.time()  # Measures file loading time
            del self.coleccion_imagenes[:]#Clean collection if previous executions

            for dirname, dirnames, filenames in os.walk(path):

                # print path to all sub-directories first
                for subdirname in dirnames:
                    print os.path.join(dirname, subdirname)

                filenames.sort(key=self.human_key)  # Sort files by name
                # print "Loading " + str(len(filenames)) + " DICOM files from: " + path


                for filename in filenames: # join the path with all filenames.
                    file_path = os.path.join(dirname, filename)  # Set the path file
                    try:
                        image = self.read_single_dicom(file_path) # try to read a dicom file
                    except:
                        try:
                            image = self.read_single_tiff(file_path) # try to read a tiff file
                        except:
                            raise Exception("File not supported")

                    self.coleccion_imagenes.append(image)  # Add current image to a list

            num_archivos = len(self.coleccion_imagenes)
            # end_time = time.time()  # Get the time when method ends
            print num_archivos, "files loaded"#in ", str(end_time - start_time), " seconds."
        except Exception as e:
            print "Error reading the image files", e
            raise
        else:
            return self.get_collection()  # Access method to the loaded images

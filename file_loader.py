'''
Created on 2/05/2014

@author: santiago
'''
import glob
import os
import dicom
import time
import re
import numpy as np


class FileLoader(object):

    def __init__(self):
        self.coleccion_imagenes = []  # Image list

    def human_key(self, key):
        """Method to 'Natural sort' a list"""
        parts = re.split('(\d*\.\d+|\d+)', key)
        return tuple((e.swapcase() if i % 2 == 0 else float(e))
                for i, e in enumerate(parts))

    def single_dicom_read(self, dicom_file):
        """Read a single DICOM file and return a NumPy Pixel Array"""
        temp = dicom.read_file(dicom_file)  # Read the file as DICOM image
        px_array = temp.pixel_array  # Transform DICOM image as numpy array
        dicom_slice = px_array[35:485, 35:485] #Cut the slice to match draw area
        #print "Loaded", str(dicom_file)
        return dicom_slice

    def load_path(self, path):

        start_time = time.time()  # Measures file loading time
        del self.coleccion_imagenes[:]#Clean collection if previous executions
        
        for dirname, dirnames, filenames in os.walk(path):

            # print path to all sub-directories first
            for subdirname in dirnames:
                print os.path.join(dirname, subdirname)

            filenames.sort(key=self.human_key)  # Sort files by name
            print "Loading " + str(len(filenames)) + " DICOM files from: " + path

            # join the path with all filenames.
            for filename in filenames:
                file_path = os.path.join(dirname, filename)  # Set the path file
                # print file_path
                image = self.single_dicom_read(file_path)
                self.coleccion_imagenes.append(image)  # Add current image to a list

        num_archivos = len(self.coleccion_imagenes)
        end_time = time.time()  # Get the time when method ends
        print num_archivos, "DICOM files loaded in ", str(end_time - start_time), " seconds."
        return self.coleccion_imagenes  # Access method to the loaded images
    
    def get_collection(self):
            return self.coleccion_imagenes
            

class FileLoaderNPY(FileLoader):
    """The aim of this class is to provide to the user the
    ability to read segmented files (*npy)"""

    def __init__(self):
        self.coleccion_imagenes = []

    def load_path(self, path):
        archives_list = glob.glob(path + "*.npy")
        archives_list.sort()

        num_archives = len(archives_list)

        for i in xrange(num_archives):
            archive = archives_list[i]
            print archive
            img = np.load(archive)
            self.coleccion_imagenes.append(img)

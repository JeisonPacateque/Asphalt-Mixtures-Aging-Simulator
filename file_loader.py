'''
Created on 2/05/2014

@author: santiago
'''

import glob
import os
import dicom
import time
import numpy as np

class FileLoader(object):
    """This Class provides the logic to read DICOM images and return it as NumPy arrays """

    def __init__(self, path):
        self.samples_collection = []    # Image list
        self.coleccion_reducida = []    # Toy Model
        self.path = path                # Set the working Path
        self.archive_list = np.array

    def load_path(self):

        start_time = time.time()  # Measures file loading time
        print "Loading dicom files..."

        for dirname, dirnames, filenames in os.walk(self.path):

            # print path to all subdirectories first.s
            for subdirname in dirnames:
                print os.path.join(dirname, subdirname)

            filenames.sort()  # Sort files by name

            # join the path with all filenames.
            for filename in filenames:
                ruta_archivo=os.path.join(dirname, filename)        #Set the path file
                temporal = dicom.read_file(ruta_archivo)            #Read the file as DICOM image
                imagen = temporal.pixel_array                       #Transform DICOM image as numpy array
                fixed = imagen[35:485, 35:485]                      #Cut image to fit plot
                self.samples_collection.append(fixed)               #Add current image to a list


        num_archivos=len(self.samples_collection)
        end_time=time.time()    #Get the time when method ends
        print num_archivos, "dicom files loaded in ", str(end_time - start_time), " seconds."
        return self.samples_collection  # Access method to the loaded images

    def analize_path(self, path):
        archives_list = glob.glob(path+"*.dcm")
        print "Total files detected: "+str(len(archives_list))


class FileLoaderNPY(FileLoader):
    """The aim of this class is to provide to the user the
    ability to read segmented files (*.npy)"""

    def __init__(self):
        self.samples_collection = []

    def load_path(self, path):
        archives_list = glob.glob(path+"*.npy")
        archives_list.sort()

        num_archives = len(archives_list)

        for i in xrange(num_archives):
            archive = archives_list[i]
            print archive
            img = np.load(archive)
            self.samples_collection.append(img)
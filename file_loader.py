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
        """Method to 'Natural sorting' a list"""
        parts = re.split('(\d*\.\d+|\d+)', key)
        return tuple((e.swapcase() if i % 2 == 0 else float(e))
                for i, e in enumerate(parts))

    def load_path(self, path):

        start_time = time.time()  # Measures file loading time
        print "Loading DICOM files from: "+path
        for dirname, dirnames, filenames in os.walk(path):

            # print path to all subdirectories first.s
            for subdirname in dirnames:
                print os.path.join(dirname, subdirname)

            filenames.sort(key=self.human_key)  # Sort files by name


            # join the path with all filenames.
            for filename in filenames:
                ruta_archivo=os.path.join(dirname, filename)        #Set the path file
                #print ruta_archivo                                 #Print file path
                temporal = dicom.read_file(ruta_archivo)            #Read the file as DICOM image
                imagen = temporal.pixel_array                       #Transform DICOM image as numpy array
                fixed = imagen[35:485, 35:485]                      #Cut image to fit plot
                self.coleccion_imagenes.append(fixed)                    #Add current image to a list

        num_archivos=len(self.coleccion_imagenes)
        end_time=time.time()    #Get the time when method ends
        print num_archivos, "dicom files loaded in ", str(end_time - start_time), " seconds."
        return self.coleccion_imagenes  # Access method to the loaded images

    def show_path(self):
        print "Path: ", self.path


class FileLoaderNPY(FileLoader):
    """The aim of this class is to provide to the user the
    ability to read segmented files (*npy)"""

    def __init__(self):
        self.coleccion_imagenes = []
#        self.load_path(path)

    def load_path(self, path):
        archives_list = glob.glob(path+"*.npy")
        archives_list.sort()

        num_archives = len(archives_list)

        for i in xrange(num_archives):
            archive = archives_list[i]
            print archive
            img = np.load(archive)
            self.coleccion_imagenes.append(img)
'''
Created on 2/05/2014

@author: santiago
'''

import glob
import dicom
import time
import numpy as np

class FileLoader(object):
    """This Class provides the logic to read DICOM images and return it as
    NumPy arrays """

    def __init__(self, path):
        self.path = path                # Set the working Path
        self.archives_list = []
        shape = self.analize_path(path)
        self.len_sample = len(self.archives_list)
        self.sample = np.zeros((shape[0], shape[1], self.len_sample+1))

    def analize_path(self, path):
        self.archives_list = glob.glob(path+"*.dcm")
        print "Total files detected: "+str(len(self.archives_list))

        temp = self.archives_list[0]
        ds = dicom.read_file(temp)
        img = ds.pixel_array
        return img.shape


    def load_path(self):

        for archive in self.archives_list:
            ds = dicom.read_file(archive)
            img = ds.pixel_array
            i = ds.InstanceNumber
            self.sample[..., ..., i] = img
            print i

#        return self.sample


class FileLoaderNPY(FileLoader):
    """The aim of this class is to provide to the user the
    ability to read segmented files (*.npy)"""

    def analize_path(self, path):
        archives_list = glob.glob(path+"*.npy")
        print "Total files detected: "+str(len(archives_list))

        return archives_list

    def load_path(self):

        for i in xrange(self.len_sample):
            archive = self.archives_list[i]
            print archive
            img = np.load(archive)
            self.sample[i] = img.copy()
#            print i

        return self.sample

if __name__ == '__main__':
    file_loader = FileLoader('/home/sjdps/MUESTRA/66719/6/')
    collection = file_loader.load_path()
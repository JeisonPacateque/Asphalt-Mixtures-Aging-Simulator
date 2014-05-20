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
        self.archive_list = self.analize_path(path)
        self.len_sample = len(self.archive_list)
        self.sample = np.array(self.len_sample)

    def analize_path(self, path):
        archives_list = glob.glob(path+"*.dcm")
        print "Total files detected: "+str(len(archives_list))

        return archives_list

    def load_path(self, path):

        for i in xrange(self.len_sample):
            archive = archives_list[i]
            print archive
            img = np.load(archive)
            self.sample[i] = img.copy()

        return self.sample


class FileLoaderNPY(FileLoader):
    """The aim of this class is to provide to the user the
    ability to read segmented files (*.npy)"""

    def analize_path(self, path):
        archives_list = glob.glob(path+"*.npy")
        print "Total files detected: "+str(len(archives_list))

        return archives_list

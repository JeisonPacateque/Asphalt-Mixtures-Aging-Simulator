# -*- coding: utf-8 -*-
"""
Created on Mon May  5 16:43:58 2014

@author: sjdps
"""
import glob
import numpy as np

from segmentation import Segmentation


def segment(mypath='/home/sjdps/MUESTRA/66719/6/'):
    """ function that segments all files in a given directory,
     it's assumed there are no segmented files yet (*npy),
    or any other type of file; so execute only once"""

    #Santiago, descomentar si quiere probar este script con su ruta
    #path = '/home/santiago/Documentos/Pruebas Python/PruebasGraficas/00490278'

    archives = glob.glob(mypath+"*")  # read all files in the given path
    archives.sort()

    segmentation = Segmentation()

    for path in archives:
        image = segmentation.read_image(path)
        img_seg = segmentation.clasify(image)
        print "Writing " + path + ".npy"
        np.save(path, img_seg)

if __name__ == '__main__':
    segment()
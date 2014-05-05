'''
Created on 2/05/2014

@author: santiago
'''
import os
import dicom
import matplotlib.pyplot as plt


coleccion_imagenes=[] #Arreglo de archivos

for dirname, dirnames, filenames in os.walk('/home/santiago/Documentos/Pruebas Python/66719/6/'):
    # print path to all subdirectories first.s
    for subdirname in dirnames:
        print os.path.join(dirname, subdirname)

    # print path to all filenames.
    for filename in filenames:
        ruta_archivo=os.path.join(dirname, filename)    #Crea la ruta del archivo
        print ruta_archivo                              #Muesta la ruta de cada archivo por consola
        temporal=dicom.read_file(ruta_archivo)          #Variable temporal para poder usar el metodo pixel_array
        imagen=temporal.pixel_array                     #Tranformacion de imagen dicom a arreglo numpy
        coleccion_imagenes.append(imagen)               #Agrega la imagen a memoria

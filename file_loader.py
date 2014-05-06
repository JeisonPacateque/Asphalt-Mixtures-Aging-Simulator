'''
Created on 2/05/2014

@author: santiago
'''
import os
import dicom
import matplotlib.pyplot as plt

coleccion_imagenes = [] #Image list

for dirname, dirnames, filenames in os.walk('/home/santiago/Documentos/Pruebas Python/66719/6/'):
    # print path to all subdirectories first.s
    for subdirname in dirnames:
        print os.path.join(dirname, subdirname)

    # print path to all filenames.
    for filename in filenames:
        ruta_archivo=os.path.join(dirname, filename)        #Set the path file
        print ruta_archivo                                  #Print file path
        temporal = dicom.read_file(ruta_archivo)            #Read the file as DICOM image
        imagen = temporal.pixel_array                       #Transform DICOM image as numpy array
        fixed = imagen[35:485, 35:485]                      #Cut image to fit plot
        coleccion_imagenes.append(fixed)                    #Add current image to a list
        
print "Finalizada la carga de archivos"

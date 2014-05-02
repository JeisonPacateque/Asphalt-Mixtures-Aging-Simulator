'''
Created on 2/05/2014

@author: santiago
'''
import os
import dicom

archivos=[] #Arreglo de archivos

for dirname, dirnames, filenames in os.walk('/home/santiago/Documentos/Pruebas Python/66719/6/'):
    # print path to all subdirectories first.
    for subdirname in dirnames:
        print os.path.join(dirname, subdirname)

    # print path to all filenames.
    for filename in filenames:
        ruta_archivo=os.path.join(dirname, filename)
        print ruta_archivo
        #print os.path.join(filename)
        archivos.append(dicom.read_file(ruta_archivo))
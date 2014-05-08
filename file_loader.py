'''
Created on 2/05/2014

@author: santiago
'''
import os
import dicom

coleccion_imagenes = [] #Image list

class FileLoader:
    
    def load_path(self, path):

        for dirname, dirnames, filenames in os.walk(path):
#        '/home/santiago/Documentos/Pruebas Python/66719/6/'
            # print path to all subdirectories first.s
            for subdirname in dirnames:
                print os.path.join(dirname, subdirname)
            
            filenames.sort()    #Sort all the files by name
        
            # print path to all filenames.
            for filename in filenames:
                ruta_archivo=os.path.join(dirname, filename)        #Set the path file
                print ruta_archivo                                  #Print file path
                temporal = dicom.read_file(ruta_archivo)            #Read the file as DICOM image
                imagen = temporal.pixel_array                       #Transform DICOM image as numpy array
                fixed = imagen[35:485, 35:485]                      #Cut image to fit plot
                coleccion_imagenes.append(fixed)                    #Add current image to a list
                
        num_archivos=len(coleccion_imagenes)        
        print "Finalizada la carga de ", num_archivos, " archivos."
        
    def get_collection(self):
        return coleccion_imagenes   #Access method to the loaded images
        
    def show_path(self):
        print "Path: ", self.path

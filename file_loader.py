'''
Created on 2/05/2014

@author: santiago
'''
import os
import dicom
import time

coleccion_imagenes = [] #Image list

class FileLoader:
    
    def load_path(self, path):
        
        start_time=time.time()  #Measures file loading time       
        print "Loading dicom files..."

        for dirname, dirnames, filenames in os.walk(path):

            # print path to all subdirectories first.s
            for subdirname in dirnames:
                print os.path.join(dirname, subdirname)
            
            filenames.sort()    #Sort files by name
        
            # join the path with all filenames.
            for filename in filenames:
                ruta_archivo=os.path.join(dirname, filename)        #Set the path file
                #print ruta_archivo                                  #Print file path
                temporal = dicom.read_file(ruta_archivo)            #Read the file as DICOM image
                imagen = temporal.pixel_array                       #Transform DICOM image as numpy array
                fixed = imagen[35:485, 35:485]                      #Cut image to fit plot
                coleccion_imagenes.append(fixed)                    #Add current image to a list
                
        num_archivos=len(coleccion_imagenes)        
        end_time=time.time()    #Get the time when method ends
        print num_archivos, "dicom files loaded in ", str(end_time - start_time), " seconds."
        
    def get_collection(self):
        return coleccion_imagenes   #Access method to the loaded images
        
    def show_path(self):
        print "Path: ", self.path

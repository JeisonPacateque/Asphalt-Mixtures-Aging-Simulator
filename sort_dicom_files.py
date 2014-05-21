'''
Created on 20/05/2014

@author: santiago
'''
import dicom
import shutil
import glob
import time

path = "/home/santiago/Documentos/Pruebas Python/66719/6/"
new_path = "/home/santiago/samples/6/"

archives_list = glob.glob(path+"*.dcm")
print "Total files detected: "+str(len(archives_list))

start_time = time.time()  # Measures file loading time

for archive in archives_list:
    ds = dicom.read_file(archive)
    img = ds.pixel_array
    newName = ds.InstanceNumber
    temporal = new_path+"sample_"+str(newName)+".dcm"
    print "Writing file: "+temporal
    shutil.copy2(archive, temporal)
    
end_time=time.time()    #Get the time when method ends
print str(len(archives_list)), "dicom files renamed in ", str(end_time - start_time), " seconds."
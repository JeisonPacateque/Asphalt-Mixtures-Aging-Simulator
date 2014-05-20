'''
Created on 20/05/2014

@author: santiago
'''
import dicom
import shutil
import glob

path = "/home/santiago/Documentos/Pruebas Python/66719/6/"
new_path = "/home/santiago/Proyecto-de-Grado-Codes/samples/"

archives_list = glob.glob(path+"*.dcm")
print "Total files detected: "+str(len(archives_list))


for archive in archives_list:
    ds = dicom.read_file(archive)
    img = ds.pixel_array
    newName = ds.InstanceNumber
    temporal = new_path+"sample_"+str(newName)+".dcm"
    print "Creando archivo: "+temporal
    shutil.copy2(archive, temporal)

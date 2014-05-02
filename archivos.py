'''
Created on 2/05/2014

@author: santiago
'''
import os

for dirname, dirnames, filenames in os.walk('/home/santiago/Documentos/Pruebas Python/66719/6/'):
    # print path to all subdirectories first.
    for subdirname in dirnames:
        print os.path.join(dirname, subdirname)

    # print path to all filenames.
    for filename in filenames:
        #print os.path.join(dirname, filename)
        print os.path.join(filename)

    # Advanced usage:
    # editing the 'dirnames' list will stop os.walk() from recursing into there.
    #if '.git' in dirnames:
        # don't go into any .git directories.
        #dirnames.remove('.git')
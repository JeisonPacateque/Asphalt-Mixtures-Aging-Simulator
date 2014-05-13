from __future__ import unicode_literals
import sys
import numpy as np
import matplotlib.image as mpimg
from PyQt4 import QtGui, QtCore
from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from file_loader import FileLoader, FileLoaderNPY


class ApplicationWindow(QtGui.QMainWindow):
    
    global collection

    def __init__(self):

        QtGui.QMainWindow.__init__(self)
        self.setAttribute(QtCore.Qt.WA_DeleteOnClose)
        self.setWindowTitle("Ventana Principal")

        self.file_menu = QtGui.QMenu('&Archivo', self)
        self.file_menu.addAction('&Salir', self.fileQuit,
                                 QtCore.Qt.CTRL + QtCore.Qt.Key_Q)
        self.menuBar().addMenu(self.file_menu)

        self.help_menu = QtGui.QMenu('&Ayuda', self)
        self.menuBar().addSeparator()
        self.menuBar().addMenu(self.help_menu)

        self.help_menu.addAction('&Acerca de...', self.about)

        open_button = QtGui.QPushButton('Choose work path', self)
        open_button.clicked[bool].connect(self.open_path) #Button listener

        self.main_widget = QtGui.QWidget(self)

        l = QtGui.QGridLayout(self.main_widget)
        self.dc = MyDynamicMplCanvas(self.main_widget, width=5, height=4, dpi=100)
        
        self.folder_path = QtGui.QLineEdit(self)
        self.folder_path.setReadOnly(True) #The only way to edit path should be by using the button

        l.addWidget(self.folder_path, 1, 1)
        l.addWidget(open_button, 1, 2)
        l.addWidget(self.dc, 2, 1, 2, 2)

        self.main_widget.setFocus()
        self.setCentralWidget(self.main_widget)
        
    def open_path(self, pressed):
        chosen_path = QtGui.QFileDialog.getExistingDirectory(None, 
                                                         'Open working directory', 
                                '/home/santiago/Documentos/Pruebas Python/66719/', 
                                                    QtGui.QFileDialog.ShowDirsOnly)

        path = str(chosen_path) #QString to python string
        print "Load files from: " + path
        self.folder_path.setText(path)

        loader=FileLoader() #Creates the FileLoader object
        loader.load_path(path) #Load the path
        global collection
        collection = loader.get_collection()

        timer = QtCore.QTimer(self)     #Timer intended to update the image
        QtCore.QObject.connect(timer, QtCore.SIGNAL("timeout()"), self.dc.update_figure)
        timer.start(100)                #Set the update time

    def update_staus(self, message):
        self.statusBar().showMessage("Muestra: "+message)

    def fileQuit(self):
        self.close()

    def closeEvent(self, ce):
        self.fileQuit()

    def contador(self):
        return self

    def about(self):
        QtGui.QMessageBox.about(self, "Acerca de",
        """Primera prueba del entorno Qt utilizando tipos de datos
MatPlotLib renderizados con la libreria grafica Qt en Python

        Desarrollado por:
        Jeison Pacateque
        Santiago Puerto""")
        
class Canvas(FigureCanvas):
#Set the graphical elements to show in a Qt Window
    def __init__(self, parent=None, width=5, height=4, dpi=100):
        fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = fig.add_subplot(111)
        # We want the axes cleared every time plot() is called
        self.axes.hold(False)
        initial = mpimg.imread('/home/santiago/Proyecto-de-Grado-Codes/images/python.png')
        self.axes.imshow(initial)   #Show an initial image for the app
        FigureCanvas.__init__(self, fig)
        self.setParent(parent)
 
        FigureCanvas.setSizePolicy(self,
                                   QtGui.QSizePolicy.Expanding,
                                   QtGui.QSizePolicy.Expanding)
        FigureCanvas.updateGeometry(self)

#-------------------------------------------------------------------------------

class MyDynamicMplCanvas(Canvas):
    # Load the dinamic plot
    global index
    index = 0
    def update_figure(self):
        #Read and plot all the images stored in the image list
        global index        #Call the index counter
        global collection   #Call the collection from loader
        if index != len(collection) : #Conditional to restart the loop
            self.axes.imshow(collection[index], cmap='seismic')
            aw.update_staus(str(index)) #Show in status bar the current index
            index += 1
            self.draw()
        else:
            index=0

#------------------------------------------------------------------------


qApp = QtGui.QApplication(sys.argv)

aw = ApplicationWindow()
aw.setWindowTitle("Visor de muestra DICOM")
aw.show()
sys.exit(qApp.exec_())
#qApp.exec_()
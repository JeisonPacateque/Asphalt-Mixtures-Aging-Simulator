from __future__ import unicode_literals
import sys
from PyQt4 import QtGui, QtCore
from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from file_loader import FileLoader


class MyMplCanvas(FigureCanvas):
#Set the graphical elements to show in a Qt Window
    def __init__(self, parent=None, width=5, height=4, dpi=100):
        fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = fig.add_subplot(111)
        # We want the axes cleared every time plot() is called
        self.axes.hold(False)

        self.compute_initial_figure()

        FigureCanvas.__init__(self, fig)
        self.setParent(parent)

        FigureCanvas.setSizePolicy(self,
                                   QtGui.QSizePolicy.Expanding,
                                   QtGui.QSizePolicy.Expanding)
        FigureCanvas.updateGeometry(self)

    def compute_initial_figure(self):
        pass

loader=FileLoader() #Creates the FileLoader object
collection=loader.get_collection() #Gets the collection of images

class MyDynamicMplCanvas(MyMplCanvas):
    #Load the dinamic plot    
    global index
    loader.load_path('/home/santiago/Documentos/Pruebas Python/66719/6/') #Load the path
    
    def __init__(self, *args, **kwargs):
        MyMplCanvas.__init__(self, *args, **kwargs)
        global index
        index = 0                       #Set the initial index
        timer = QtCore.QTimer(self)     #Timer intended to update the image
        QtCore.QObject.connect(timer, QtCore.SIGNAL("timeout()"), self.update_figure)
        timer.start(100)                #Set the update time

    def compute_initial_figure(self):
        self.axes.imshow(collection[0], cmap='seismic') #Set the initial image

    def update_figure(self):
        #Read and plot all the images stored in the image list
        global index
        if index != len(collection) : #Conditional to restart the loop  
            self.axes.imshow(collection[index], cmap='seismic')
            #print "Imagen numero: ",index
            aw.update_staus(str(index))
            index += 1
            self.draw()
        else:
            index=0


class ApplicationWindow(QtGui.QMainWindow):

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

        self.main_widget = QtGui.QWidget(self)

        l = QtGui.QGridLayout(self.main_widget)
        dc = MyDynamicMplCanvas(self.main_widget, width=5, height=4, dpi=100)
        l.addWidget(dc)

        self.main_widget.setFocus()
        self.setCentralWidget(self.main_widget)

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

qApp = QtGui.QApplication(sys.argv)

aw = ApplicationWindow()
aw.setWindowTitle("Visor de muestra DICOM")
aw.show()
sys.exit(qApp.exec_())
#qApp.exec_()
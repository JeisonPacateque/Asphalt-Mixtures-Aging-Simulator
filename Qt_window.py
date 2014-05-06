from __future__ import unicode_literals
import sys
from PyQt4 import QtGui, QtCore
from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import dicom
import file_loader


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


class MyStaticMplCanvas(MyMplCanvas):
    #Load the static plot
    def compute_initial_figure(self):
        ds = dicom.read_file('/home/santiago/Documentos/Pruebas Python/PruebasGraficas/00490278')
        arreglo = ds.pixel_array
        fixed = arreglo[35:485, 35:485]
        self.axes.imshow(fixed, cmap='seismic')


class MyDynamicMplCanvas(MyMplCanvas):
    #Load the dinamic plot    
    global miGlobal
    def __init__(self, *args, **kwargs):
        MyMplCanvas.__init__(self, *args, **kwargs)
        global miGlobal
        miGlobal = 0
        timer = QtCore.QTimer(self)
        QtCore.QObject.connect(timer, QtCore.SIGNAL("timeout()"), self.update_figure)
        timer.start(500)

    def compute_initial_figure(self):
        self.axes.imshow(file_loader.coleccion_imagenes[0], cmap='seismic')

    def update_figure(self):
        #Read and plot all the images stored in the image list
        global miGlobal
        if miGlobal != len(file_loader.coleccion_imagenes) : #Conditional to restart the loop
            self.axes.imshow(file_loader.coleccion_imagenes[miGlobal], cmap='seismic')
            print "Imagen numero: ",miGlobal
            miGlobal += 1
            self.draw()
        else:
            miGlobal=0

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
        sc = MyStaticMplCanvas(self.main_widget, width=5, height=4, dpi=100)
        dc = MyDynamicMplCanvas(self.main_widget, width=5, height=4, dpi=100)
        #l.addWidget(sc)
        l.addWidget(dc)


        self.main_widget.setFocus()
        self.setCentralWidget(self.main_widget)

        self.statusBar().showMessage("Cortes transverzales de la muestra")

    def fileQuit(self):
        self.close()

    def closeEvent(self, ce):
        self.fileQuit()

    def about(self):
        QtGui.QMessageBox.about(self, "About",
        """Primer prueba del entorno Qt utilizando tipos de datos de 
    MatPlotLib renderizados con la libreriagrafica Qt en Python""")

qApp = QtGui.QApplication(sys.argv)

aw = ApplicationWindow()
aw.setWindowTitle("Entorno Qt")
aw.show()
sys.exit(qApp.exec_())
#qApp.exec_()
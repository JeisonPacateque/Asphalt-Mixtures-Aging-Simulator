from __future__ import unicode_literals
import sys
from PyQt4 import QtGui, QtCore
from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import dicom
import archivos


class MyMplCanvas(FigureCanvas):
    """Ultimately, this is a QWidget (as well as a FigureCanvasAgg, etc.)."""
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
    """Simple canvas with a sine plot."""
    def compute_initial_figure(self):
        ds=dicom.read_file('/home/santiago/Documentos/Pruebas Python/PruebasGraficas/00490278')
        arreglo=ds.pixel_array
        fixed=arreglo[35:485, 35:485]
        self.axes.imshow(fixed, cmap='seismic')


class MyDynamicMplCanvas(MyMplCanvas):
    
    global miGlobal
    """A canvas that updates itself every second with a new plot."""
    def __init__(self, *args, **kwargs):
        MyMplCanvas.__init__(self, *args, **kwargs)
        global miGlobal
        miGlobal=0
        timer = QtCore.QTimer(self)
        QtCore.QObject.connect(timer, QtCore.SIGNAL("timeout()"), self.update_figure)
        timer.start(500)

    def compute_initial_figure(self):
        self.axes.imshow(archivos.coleccion_imagenes[0])

    def update_figure(self):
        # Build a list of 4 random integers between 0 and 10 (both inclusive)
        global miGlobal
        self.axes.imshow(archivos.coleccion_imagenes[miGlobal])
        miGlobal=miGlobal+1
        self.draw()
    
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
        l.addWidget(sc)
        l.addWidget(dc)


        self.main_widget.setFocus()
        self.setCentralWidget(self.main_widget)

        self.statusBar().showMessage("Vista Inicial")

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
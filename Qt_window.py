from __future__ import unicode_literals
import sys
import matplotlib.image as mpimg
from PyQt4 import QtGui, QtCore
from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from file_loader import FileLoader
from _markerlib import __init__


class ApplicationWindow(QtGui.QMainWindow):
    collection = [] #Class attribute
    timer = QtCore.QTimer()     #Timer intended to update the image

    def __init__(self):

        QtGui.QMainWindow.__init__(self)
        self.setAttribute(QtCore.Qt.WA_DeleteOnClose)

        self.file_menu = QtGui.QMenu('&File', self)
        self.file_menu.addAction('&Exit', self.fileQuit,
                                 QtCore.Qt.CTRL + QtCore.Qt.Key_Q)
        self.menuBar().addMenu(self.file_menu)
        
        self.sample_menu = QtGui.QMenu('&Sample', self)
        self.sample_menu.addAction('&Resume', self.resume_animation,
                                   QtCore.Qt.CTRL + QtCore.Qt.Key_R)
        self.sample_menu.addAction('&Pause', self.stop_animation,
                                   QtCore.Qt.CTRL + QtCore.Qt.Key_P)
        self.menuBar().addMenu(self.sample_menu)

        self.help_menu = QtGui.QMenu('&Help', self)
        self.menuBar().addSeparator()
        self.menuBar().addMenu(self.help_menu)

        self.help_menu.addAction('&About...', self.about)

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

        #Modifiying the class attribute to get the loaded collection of images
        self.__class__.collection = FileLoader().load_path(path)

        QtCore.QObject.connect(self.__class__.timer, QtCore.SIGNAL("timeout()"), self.dc.update_figure)
        self.__class__.timer.start(100)                #Set the update time

    def stop_animation(self):
        self.__class__.timer.stop()
        
    def resume_animation(self):
        self.__class__.timer.start(100)
        
    def update_staus(self, message):
        self.statusBar().showMessage("Sample: "+message)

    def fileQuit(self):
        self.close()

    def closeEvent(self, ce):
        self.fileQuit()

    def about(self):
        QtGui.QMessageBox.about(self, "About",
        """First attempt to inplement a Qt enviroment rendering 
MatPlotLib figures created from DICOM files

        Developed by:
        Jeison Pacateque
        Santiago Puerto""")
        
class Canvas(FigureCanvas):
#Set the graphical elements to show in a Qt Window
    def __init__(self, parent=None, width=5, height=4, dpi=100):
        fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = fig.add_subplot(111)
        self.axes.hold(False) #We want the axes cleared every time plot() is called
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
    index = 0
    def update_figure(self):
        #Read and plot all the images stored in the image list
        collection = ApplicationWindow.collection
        if self.__class__.index != len(collection) : #Conditional to restart the loop
            self.axes.imshow(collection[self.__class__.index], cmap='seismic')
            aw.update_staus(str(self.__class__.index)) #Show in status bar the current index
            self.__class__.index += 1
            self.draw()
        else:
            self.__class__.index=0

#------------------------------------------------------------------------


qApp = QtGui.QApplication(sys.argv)

aw = ApplicationWindow()
aw.setWindowTitle("DICOM Samples Viewer")
aw.show()
sys.exit(qApp.exec_())
#qApp.exec_()
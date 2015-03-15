#!/usr/bin/env python2
'''
Copyright (C) 2015 Jeison Pacateque, Santiago Puerto

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>
'''

import sys
import os
from PyQt4 import QtGui, QtCore
import matplotlib
matplotlib.use("Qt4Agg")
import matplotlib.image as mpimg
import matplotlib as mpl
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from integration.file_loader import  FileLoader
from output.results import Result
from graphic_controller import SegmentationController, SimulationController


class ApplicationWindow(QtGui.QMainWindow):
    def __init__(self):
        """This Class contains the main window of the program"""

        super(ApplicationWindow, self).__init__()

        self.collection = []
        self.loader = FileLoader()

        self._initUI()

    def _initUI(self):
        """ Gui initicializater"""

        self.timer = QtCore.QTimer()     #Timer intended to update the image
        self.setAttribute(QtCore.Qt.WA_DeleteOnClose)

        self.file_menu = QtGui.QMenu('File', self)
        self.file_menu.addAction('Choose path', self.open_path, QtCore.Qt.CTRL + QtCore.Qt.Key_O)
        self.file_menu.addAction('Exit', self.fileQuit, QtCore.Qt.CTRL + QtCore.Qt.Key_Q)
        self.menuBar().addMenu(self.file_menu)

        self.animation_menu = QtGui.QMenu('Animation', self)
        self.action_animation_start = self.animation_menu.addAction('&Start', self.start_animation, QtCore.Qt.Key_S)
        self.action_animation_pause = self.animation_menu.addAction('Pause/Resume', self.pause_animation, QtCore.Qt.Key_Space)
        self.paused = False #flag to control pause animation
        self.menuBar().addMenu(self.animation_menu)

        self.sample_menu = QtGui.QMenu('Sample', self)
        self.action_sample_segment = self.sample_menu.addAction('Segment sample', self.segment_sample, QtCore.Qt.CTRL + QtCore.Qt.Key_S)
        self.action_sample_3d = self.sample_menu.addAction('Show 3D model', self.show_3d_sample)
        self.action_sample_count = self.sample_menu.addAction('Count segmented elements', self.count_element_values)
        self.menuBar().addMenu(self.sample_menu)

        self.simulation_menu = QtGui.QMenu('Simulation', self)
        self.simulation_setup = self.simulation_menu.addAction('Set up simulation...', self.setup_simulation)
        self.menuBar().addMenu(self.simulation_menu)

        self.help_menu = QtGui.QMenu('Help', self)
        self.menuBar().addSeparator()
        self.menuBar().addMenu(self.help_menu)

        self.help_menu.addAction('Help', self.help_dialog)
        self.help_menu.addAction('About...', self.about)

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
        self.setGeometry(10, 35 , 560, 520)

        window_size = self.geometry()
        left = window_size.left()
        right = window_size.right()-500
        top = window_size.top()+200
        bottom = window_size.bottom()-20

        self.window_size = QtCore.QRect(left, top, bottom, right)
        self.main_widget.setFocus()
        self.setCentralWidget(self.main_widget)
        self.menu_buttons_state()


    def open_path(self):
        """
        Shows an "open folder dialog" looking for Dicom files to load
        """
        self.pause_animation();
        self.update_staus("Loading files from path...")
        current_path = os.path.dirname(os.path.abspath(__file__))+'/samples/4/'
        chosen_path = QtGui.QFileDialog.getExistingDirectory(None,
                                                         'Open working directory',
                                                                     current_path,
                                                   QtGui.QFileDialog.ShowDirsOnly)

        path = str(chosen_path+"/") #QString to Python string
        #Prevents the execution of load_path if the user don't select a folder
        if path != "/":
            self.collection = self.loader.load_path(path) #Load Files
            total_loaded = str(len(self.collection))+" DICOM files loaded."
            self.folder_path.setText(path)
            self.update_staus(total_loaded)
            self.menu_buttons_state(True)
            QtGui.QMessageBox.about(self, "Information:", total_loaded)


    def start_animation(self):
        """
        Run the 2D animation of the X-Ray raw or treated Dicom slices from
        the asphalt mixture sample
        """
        self.dc.reset_index()
        QtCore.QObject.connect(self.timer, QtCore.SIGNAL("timeout()"), self.dc.update_figure)
        self.timer.start(150)                #Set the update time
        self.paused = False

    def pause_animation(self):
        """
        Pause and Resume the 2D animation of the X-Ray raw or treated Dicom slices from
        the asphalt mixture sample
        """
        if self.paused:
            self.timer.start(150)
            self.paused = False
        else:
            self.timer.stop()
            self.paused = True

    def update_staus(self, message):
        """
        Set text over the status bar on the main window of the application
        """
        self.statusBar().showMessage(message)

    def segment_sample(self):
        """
        Thorugh a controller it reduces and segmentes the toymodel.
        This also enables the application window to show the animation of the
        treated sample
        """
        self.progressBar = QtGui.QProgressBar(self)
        #self.progressBar.setGeometry(QtCore.QRect(50, 210, 460, 40))
        self.progressBar.setGeometry(self.window_size)
        controller = SegmentationController(self.collection)
        self.update_staus("Segmenting and reducing the sample...")

        def onFinished():
            self.progressBar.setRange(0,1)
            self.progressBar.setValue(1)
            self.collection = controller.getData()
            self.update_staus("Segmenting and reducing completed...")

            self.dc.reset_index()
            self.action_sample_3d.setEnabled(True)  #Enables the 3D Model viewer
            self.action_sample_count.setEnabled(True) #Enables the count method
            self.simulation_setup.setEnabled(True) #Enables the simulation setup
            self.action_sample_segment.setEnabled(False) #Disables de segmentation action
            self.progressBar.close()

            self.count_element_values()

        controller.finished.connect(onFinished)
        controller.start()
        self.progressBar.show()
        self.progressBar.setRange(0,0)

    def show_3d_sample(self):
        """
        Load the 3D render script
        """
        try:
            from output.render_3d import ToyModel3d
            print "Running 3D Modeling..."
            self.update_staus("Running 3D Modeling...")
            ToyModel3d(self.collection)
        except:
            print "Please check Mayavi installation"
            QtGui.QMessageBox.information(self, "Error",
                                    "Please check your Mayavi installation")


    def count_element_values(self):
        """Shows the total count of detected elements after the segmentation"""
        from numpy import count_nonzero
        from imgprocessing.slice_mask import apply_mask

        collection_mask = self.collection.copy()
        collection_mask = apply_mask(collection_mask)

        empty = count_nonzero(collection_mask==0)
        mastic = count_nonzero(collection_mask==1)
        aggregate = count_nonzero(collection_mask==2)

        total = (empty+mastic+aggregate)

        QtGui.QMessageBox.about(self,
                    "Element counting",
                    """
                    <br>
                    <table>
                    <tr><th>The sample has = %s pixels:</th><\tr>
                    <tr>
                    <td>Empty pixels = %s</td> <td>%3.2f%%</td>
                    </tr>
                    <tr>
                    <td>Mastic pixels = %s</td> <td>%3.2f%%</td>
                    </tr>
                    <tr>
                    <td>Aggregate pixels = %s</td> <td>%3.2f%%</td>
                    </tr>
                    </table>
                    """
                    % (total, empty, ((empty*100.)/total), mastic,
                           ((mastic*100.)/total), aggregate,\
                           ((aggregate*100.)/total)) )

    def menu_buttons_state(self, state=False):
        """Enable/Disable menu options except the Count element option
        the count method requires samples to be segmented"""
        self.action_sample_count.setEnabled(False)
        self.action_sample_3d.setEnabled(False)
        self.simulation_setup.setEnabled(False)

        self.action_animation_pause.setEnabled(state)
#        self.action_animation_resume.setEnabled(state)
        self.action_animation_start.setEnabled(state)
        self.action_sample_segment.setEnabled(state)


    def fileQuit(self):
        """
        Pause the animation on the main window and destroy the canvas objects
        in order to close the application witout errors
        """
        self.pause_animation()
        self.dc.destroy()
        self.close()

    def closeEvent(self, ce):
        """ Handle the window close event"""
        self.fileQuit()

    def about(self):
        """Shows the about dialog"""

        QtGui.QMessageBox.about(self,
                                ("%s") % "About",\
                                """
                                <br><b>Asphalt Mixtures Aging Simulator</b>
                                <p>Copyright &copy; 2014-2015 Jeison Pacateque, Santiago Puerto
                                <br>Licensed under the terms of the GNU GPLv3 License
                                <p>Created by Santiago Puerto and Jeison Pacateque
                                <p>This project performs a 3D reconstruction of a cylindrical asphalt mixture
                                sample from a set images on a Dicom file format. The components of asphalt
                                mixture will be identified through 3-phase segmentation. Additionally, a
                                3D model of the asphalt mixture reconstruction was developed. The project
                                was implemented on the Python programming language using the open-source
                                libraries Numpy, Scipy, Pydicom, Scikit-learn, Matplotlib and Mayavi.
                                A simulation of the asphalt mixtures aging process is implemented using
                                numerical methods on the mechanical, themical and chemical fields.

                                <p>The source is hosted on
                                <a href="https://github.com/JeisonPacateque/Asphalt-Mixtures-Aging-Simulator"> Github</a>

                                <p>Research Group TOPOVIAL
                                <br>Distrital University Francisco Jose de Caldas
                                """)

    def help_dialog(self):
        QtGui.QMessageBox.about(self, "Help",
        """<b>Asphalt Mixtures Aging Simulator</b>

        <p>You can find <a href="http://asphalt-mixtures-aging-simulator.readthedocs.org"> here </a>
        the complete documentation of the project.

        <p>Research Group TOPOVIAL <br/>
        Universidad Distrital Francisco Jose de Caldas
        """)

    def get_collection(self):
        return self.collection

    def set_collection(self, collection):
        self.collection = collection

    def setup_simulation(self):
        """Shows the configure simulation dialog"""

        self.config_dialog = ConfigureSimulationDialog(self.collection)
        self.config_dialog.exec_() #Prevents the dialog to disappear


class Canvas(FigureCanvas):
    """Set the graphical elements to show in a Qt Window"""
    def __init__(self, parent=None, width=5, height=4, dpi=100):
        self.fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = self.fig.add_subplot(111)
        self.axes.hold(False) #We want the axes cleared every time plot() is called
        FigureCanvas.__init__(self, self.fig)
        self.setParent(parent)

        FigureCanvas.setSizePolicy(self,
                                   QtGui.QSizePolicy.Expanding,
                                   QtGui.QSizePolicy.Expanding)
        FigureCanvas.updateGeometry(self)

#-------------------------------------------------------------------------------

class MyDynamicMplCanvas(Canvas):
    """This Class implements the canvas update method to animate the samples """
    def __init__(self, main_widget, width=5, height=4, dpi=100):
        super(MyDynamicMplCanvas, self).__init__(main_widget, width=5, height=4, dpi=100)
        self.index = 0
        self.collection = "Empty"
        self.myFigure = Canvas()
        initial = mpimg.imread('images/python.png')
        self.temp = self.axes.imshow(initial)

        min, max = (-1, 2)
        step = 1
        # Setting up a colormap
        self.mymap = mpl.colors.LinearSegmentedColormap.from_list('mycolors',['blue', 'white', 'red'])
        Z = [[0,0],[0,0]]
        levels = range(min,max+step,step)
        material_colors = plt.contourf(Z, levels, cmap=self.mymap)
        plt.clf()

        # Plotting what I actually want
        X=[[1,2],[1,2],[1,2],[1,2]]
        Y=[[1,2],[1,3],[1,4],[1,5]]
        Z=[-50,-1,0,50]
        for x,y,z in zip(X,Y,Z):
            # setting rgb color based on z normalized to my range
            r = (float(z)-min)/(max-min)
            g = 0
            b = 1-r
        plt.plot(x,y,color=(r,g,b))
        self.fig_colorbar = self.myFigure.fig.colorbar(material_colors, ax=self.axes)
        self.fig_colorbar.set_ticklabels(['','', '', ''])


    def update_figure(self):
        """Read and plot all the images stored in the image list"""
        #Set the labels for the materials
        self.fig_colorbar.set_ticklabels(['','Voids', 'Mastic', 'Aggregate'])
        if type(self.collection) == str:
            self.collection = aw.get_collection()
        if self.index != len(self.collection) : #Conditional to restart the loop

            self.temp = self.axes.imshow(self.collection[self.index], cmap='seismic', interpolation='nearest')

            status_text = "Sample: "+str(self.index)
            aw.update_staus(status_text) #Show in status bar the current index
            self.index += 1
            self.draw()
        else:
            self.index=0 #When iteration catches the len(self.collection) restart the loop


    def reset_index(self):
        """Reset the slice index to restart the animation"""
        self.index = 0
        self.collection = "Empty"


#------------------------------------------------------------------------
class ConfigureSimulationDialog(QtGui.QDialog):
    """
    This dialog enables the user to control the simulation parameters after
    the simulation runs
    """

    def __init__(self, collection):
        super(ConfigureSimulationDialog, self).__init__()

        self.collection = collection
        _, _, self.size_Z = self.collection.shape

        self._initUI()

    def _initUI(self):
        self.title = QtGui.QLabel('<b> Select the vertical slice </b>')

        self.slider = QtGui.QSlider()
        self.slider.setGeometry(QtCore.QRect(120, 380, 321, 31))
        self.slider.setOrientation(QtCore.Qt.Horizontal)
        self.slider.setRange(0, self.size_Z)
        self.slider.valueChanged.connect(self.changeText)

        self.sliderSelected = QtGui.QLineEdit()
        self.sliderSelected.setGeometry(QtCore.QRect(112, 280, 331, 20))

        self.mechanicsLabel = QtGui.QLabel("<b> Young's modulus </b>")
        self.modulusAggregateLabel = QtGui.QLabel("Aggregate:")
        self.modulusMasticLabel = QtGui.QLabel("Mastic:")
        self.modulusAirLabel = QtGui.QLabel("Air voids:")
        self.mechanicalForceLabel = QtGui.QLabel("Applied force: ")

        self.aggregate_YM = QtGui.QLineEdit()
        self.mastic_YM = QtGui.QLineEdit()
        self.air_YM = QtGui.QLineEdit()
        self.mechanicalForceEdit = QtGui.QLineEdit()

        self.thermalLabel = QtGui.QLabel("<b> Thermal conductivity </b>")
        self.thermalAggregateLabel = QtGui.QLabel("Aggregate:")
        self.thermalMasticLabel = QtGui.QLabel("Mastic:")
        self.thermalAirLabel = QtGui.QLabel("Air voids:")

        self.aggregate_TC = QtGui.QLineEdit()
        self.mastic_TC = QtGui.QLineEdit()
        self.air_TC = QtGui.QLineEdit()

        self.chemicalLabel = QtGui.QLabel("<b> Chemical constants </b>")
        self.chemicalAggregateLabel = QtGui.QLabel("Chemical value1:")
        self.chemicalMasticLabel = QtGui.QLabel("Chemical value2:")
        self.chemicalAirLabel = QtGui.QLabel("Chemical value3:")

        self.thermalStepsLabel = QtGui.QLabel("Steps:")
        self.thermalSteps = QtGui.QLineEdit()

        self.aggregate_CH = QtGui.QLineEdit()
        self.mastic_CH = QtGui.QLineEdit()
        self.air_CH = QtGui.QLineEdit()

        self.runSimulationButton = QtGui.QPushButton('Run simulation', self)
        self.runSimulationButton.clicked[bool].connect(self.runSimulation) #Listener

        self.cancelButton =  QtGui.QPushButton('Cancel', self)
        self.cancelButton.clicked[bool].connect(self.closeWindow)

        self.grid = QtGui.QGridLayout()
        self.grid.setSpacing(2)

        self.grid.addWidget(self.title, 0, 0)

        self.grid.addWidget(self.slider, 1, 0)
        self.grid.addWidget(self.sliderSelected, 1, 1)

        self.grid.addWidget(self.mechanicsLabel, 2, 0)
        self.grid.addWidget(self.modulusAggregateLabel, 3, 0)
        self.grid.addWidget(self.aggregate_YM, 3, 1)
        self.grid.addWidget(self.mechanicalForceLabel, 3, 2)
        self.grid.addWidget(self.mechanicalForceEdit, 3, 3)
        self.grid.addWidget(self.modulusMasticLabel, 4, 0)
        self.grid.addWidget(self.mastic_YM, 4, 1)
        self.grid.addWidget(self.modulusAirLabel, 5, 0)
        self.grid.addWidget(self.air_YM, 5, 1)

        self.grid.addWidget(self.thermalLabel, 6, 0)
        self.grid.addWidget(self.thermalAggregateLabel, 7, 0)
        self.grid.addWidget(self.aggregate_TC, 7, 1)
        self.grid.addWidget(self.thermalMasticLabel, 8, 0)
        self.grid.addWidget(self.mastic_TC, 8, 1)
        self.grid.addWidget(self.thermalAirLabel, 9, 0)
        self.grid.addWidget(self.air_TC, 9, 1)
        self.grid.addWidget(self.thermalStepsLabel, 7, 2)
        self.grid.addWidget(self.thermalSteps, 7, 3)

        self.grid.addWidget(self.chemicalLabel, 10, 0)
        self.grid.addWidget(self.chemicalAggregateLabel, 11, 0)
        self.grid.addWidget(self.aggregate_CH, 11, 1)
        self.grid.addWidget(self.chemicalMasticLabel, 12, 0)
        self.grid.addWidget(self.mastic_CH, 12, 1)
        self.grid.addWidget(self.chemicalAirLabel, 13, 0)
        self.grid.addWidget(self.air_CH, 13, 1)

        self.grid.addWidget(self.runSimulationButton, 14, 1)
        self.grid.addWidget(self.cancelButton, 14, 2)

        self.setLayout(self.grid)
        self.setGeometry(10, 35 , 560, 520)

        window_size = self.geometry()
        left = window_size.left()
        right = window_size.right()-500
        top = window_size.top()+200
        bottom = window_size.bottom()-20

        self.window_size = QtCore.QRect(left, top, bottom, right)
        self.setWindowTitle('Configure Simulation')
        self.setDefaultValues()
        self.show()

    def closeWindow(self):
        self.close()

    def changeText(self, value):
        self.z = value
        self.sliderSelected.setText(str(self.z))

    def setDefaultValues(self):
        """
        This method writes default test values over the configuration dialog
        """
        E2 = 21000000
        E1 = 10000000
        E0 = 100

        conductAsphalt = 0.75
        conductRock = 7.8
        conductAir = 0.026

        steps = 10000
        target_slice = self.size_Z/2

        mechanical_force = 800

        self.aggregate_YM.setText(str(E2))
        self.mastic_YM.setText(str(E1))
        self.air_YM.setText(str(E0))
        self.aggregate_TC.setText(str(conductRock))
        self.mastic_TC.setText(str(conductAsphalt))
        self.air_TC.setText(str(conductAir))
        self.thermalSteps.setText(str(steps))
        self.mechanicalForceEdit.setText(str(mechanical_force))
        self.sliderSelected.setText(str(target_slice))
        self.aggregate_CH.setText('Chem Aggregate')
        self.mastic_CH.setText('Chem Mastic')
        self.air_CH.setText('Chem Air')


    def runSimulation(self):
        """
        This method loads the user input and initialize the simulation engine
        """
        options = {
        'physical_cons': {
            'aggregate_YM': self.aggregate_YM.text(),
            'aggregate_TC': self.aggregate_TC.text(),
            'aggregate_CH': self.aggregate_CH.text(),

            'mastic_YM': self.mastic_YM.text(),
            'mastic_TC': self.mastic_TC.text(),
            'mastic_CH': self.mastic_CH.text(),

            'air_YM': self.air_YM.text(),
            'air_TC': self.air_TC.text(),
            'air_CH': self.air_CH.text(),
        },

        'inputs': {
            'force_input': int(self.mechanicalForceEdit.text()),
            'thermal_steps': int(self.thermalSteps.text()),
        }

        }

        slice_id = int(self.sliderSelected.text())

        #Close the dialog before the simulation starts

        self.progressBar = QtGui.QProgressBar(self)
        self.progressBar.setGeometry(QtCore.QRect(self.window_size))
        self.controller = SimulationController(self.collection, slice_id, **options)

        def onFinished():
            self.progressBar.setRange(0,1)
            self.progressBar.setValue(1)
            self.progressBar.hide()
            materials = self.controller.getData()
            output_results = Result(materials)
            output_results.showResults()

        self.controller.finished.connect(onFinished)
        self.controller.start()
        self.progressBar.show()
        self.progressBar.setRange(0,0)

#-----------------------------------------------------------------------------
if __name__ == '__main__':
    qApp = QtGui.QApplication(sys.argv)
    aw = ApplicationWindow()
    aw.setWindowTitle("Asphalt Mixtures Aging Simulator")
    aw.show()
    sys.exit(qApp.exec_())

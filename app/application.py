#!/usr/bin/python3
# -*- coding: utf-8 -*-
'''
Copyright (C) 2015 Jeison Pacateque, Santiago Puerto, Wilmar Fernandez

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

import os

from PyQt5 import QtWidgets, QtCore

from app.integration.file_loader import FileLoader
from app.graphic_controller import SegmentationController
from app.ui.canvas_2d import DynamicMplCanvas
from app.ui.configure_simulation import ConfigureSimulationDialog
from app.signals import signals


class Application(QtWidgets.QMainWindow):

    def __init__(self):
        """This Class contains the main window of the program"""

        super().__init__()

        self.collection = []
        self.loader = FileLoader()
        self.main_widget = QtWidgets.QWidget(self)
        self.dynamic_canvas = DynamicMplCanvas(self.main_widget, width=5, height=4,
                                               dpi=100, collection=self.collection) # to show 2D slices

        self._initUI()

    def _initUI(self):
        """ Gui initicializater"""

        self.setAttribute(QtCore.Qt.WA_DeleteOnClose)

        self.file_menu = QtWidgets.QMenu('File', self)
        self.file_menu.addAction('Choose path', self.open_path, QtCore.Qt.CTRL + QtCore.Qt.Key_O)
        self.file_menu.addAction('Exit', self.fileQuit, QtCore.Qt.CTRL + QtCore.Qt.Key_Q)
        self.menuBar().addMenu(self.file_menu)

        self.animation_menu = QtWidgets.QMenu('Animation', self)
        self.action_animation_start = self.animation_menu.addAction('&Start',
                                                                    self.dynamic_canvas.start_animation,
                                                                    QtCore.Qt.Key_S)
        self.action_animation_pause = self.animation_menu.addAction('Pause/Resume',
                                                                    self.dynamic_canvas.pause_animation,
                                                                    QtCore.Qt.Key_Space)
        self.paused = False  # flag to control pause ui
        self.menuBar().addMenu(self.animation_menu)

        self.sample_menu = QtWidgets.QMenu('Sample', self)
        self.action_sample_segment = self.sample_menu.addAction('Segment sample', self.segment_sample,
                                                                QtCore.Qt.CTRL + QtCore.Qt.Key_S)
        self.action_sample_3d = self.sample_menu.addAction('Show 3D model', self.show_3d_sample)
        self.action_sample_count = self.sample_menu.addAction('Count segmented elements', self.count_element_values)
        self.menuBar().addMenu(self.sample_menu)

        self.simulation_menu = QtWidgets.QMenu('Simulation', self)
        self.simulation_setup = self.simulation_menu.addAction('Set up simulation...', self.setup_simulation)
        self.menuBar().addMenu(self.simulation_menu)

        self.help_menu = QtWidgets.QMenu('Help', self)
        self.menuBar().addSeparator()
        self.menuBar().addMenu(self.help_menu)

        self.help_menu.addAction('Help', self.help_dialog)
        self.help_menu.addAction('About...', self.about)

        open_button = QtWidgets.QPushButton('Choose work path', self)
        open_button.clicked[bool].connect(self.open_path)  # Button listener

        layout = QtWidgets.QGridLayout(self.main_widget)

        self.folder_path = QtWidgets.QLineEdit(self)
        self.folder_path.setReadOnly(True)  # The only way to edit path should be by using the button

        layout.addWidget(self.folder_path, 1, 1)
        layout.addWidget(open_button, 1, 2)
        layout.addWidget(self.dynamic_canvas, 2, 1, 2, 2)
        self.setGeometry(10, 35, 560, 520)

        window_size = self.geometry()
        left = window_size.left()
        right = window_size.right() - 500
        top = window_size.top() + 200
        bottom = window_size.bottom() - 20

        self.window_size = QtCore.QRect(left, top, bottom, right)
        self.main_widget.setFocus()
        self.setCentralWidget(self.main_widget)
        self.menu_buttons_state()

        signals.slice_index.connect(self.update_status)


    def open_path(self):
        """
        Shows an "open folder dialog" looking for Dicom files to load
        """
        self.dynamic_canvas.pause_animation()
        self.update_status("Loading files from path...")
        current_path = os.path.dirname(os.path.abspath(__file__)) + '/samples/4/'
        chosen_path = QtWidgets.QFileDialog.getExistingDirectory(None,
                                                             'Open working directory',
                                                             current_path,
                                                             QtWidgets.QFileDialog.ShowDirsOnly)

        path = str(chosen_path + "/")  # QString to Python string
        # Prevents the execution of load_path if the user don't select a folder
        if path != "/":
            try:
                self.collection = self.loader.load_path(path)  # Load Files
                print(type(self.collection[0]), self.collection[0].shape)
            except Exception as msg_error:
                print("Error loading the image files", msg_error)
                QtWidgets.QMessageBox.information(self, "Error", str(msg_error))
            else:
                total_loaded = str(len(self.collection)) + " files loaded."
                self.folder_path.setText(path)
                self.update_status(total_loaded)
                self.menu_buttons_state(True)
                QtWidgets.QMessageBox.about(self, "Information:", total_loaded)
                self.dynamic_canvas.collection = self.collection
                self.dynamic_canvas.update_figure()

    @QtCore.pyqtSlot(str)
    def update_status(self, message):
        """
        Set text over the status bar on the main window of the application
        """
        self.statusBar().showMessage(message)


    def segment_sample(self):
        """
        Thorugh a controller it reduces and segmentes the toymodel.
        This also enables the application window to show the ui of the
        treated sample
        """

        self.dynamic_canvas.pause_animation()
        self.progressBar = QtWidgets.QProgressBar(self)
        # self.progressBar.setGeometry(QtCore.QRect(50, 210, 460, 40))
        self.progressBar.setGeometry(self.window_size)
        controller = SegmentationController(self.collection)
        self.update_status("Segmenting and reducing the sample...")


        def onFinished():
            self.progressBar.setRange(0, 1)
            self.progressBar.setValue(1)
            self.collection = controller.getData()
            self.update_status("Segmenting and reducing completed...")

            self.action_sample_3d.setEnabled(True)  # Enables the 3D Model viewer
            self.action_sample_count.setEnabled(True)  # Enables the count method
            self.simulation_setup.setEnabled(True)  # Enables the simulation setup
            self.action_sample_segment.setEnabled(False)  # Disables de segmentation action
            self.progressBar.close()

            # Refresh canvas with segmented images and pause
            self.dynamic_canvas.collection = self.collection
            self.dynamic_canvas.update_figure()

            self.count_element_values()


        controller.finished.connect(onFinished)
        controller.start()
        self.progressBar.show()
        self.progressBar.setRange(0, 0)

    def show_3d_sample(self):
        """
        Load the 3D render script
        """
        try:
            from app.ui.render_3d import ToyModel3d
            print("Running 3D Modeling...")
            self.update_status("Running 3D Modeling...")
            ToyModel3d(self.collection)
        except:
            print("Please check Mayavi installation")
            QtWidgets.QMessageBox.information(self, "Error",
                                          "Please check your Mayavi installation")

    def count_element_values(self):
        """Shows the total count of detected elements after the segmentation"""
        from numpy import count_nonzero
        from app.imgprocessing.slice_mask import apply_mask

        collection_mask = self.collection.copy()
        collection_mask = apply_mask(collection_mask)

        empty = count_nonzero(collection_mask == 0)
        mastic = count_nonzero(collection_mask == 1)
        aggregate = count_nonzero(collection_mask == 2)

        total = (empty + mastic + aggregate)

        QtWidgets.QMessageBox.about(self,
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
                                % (total, empty, ((empty * 100.) / total), mastic,
                                   ((mastic * 100.) / total), aggregate, \
                                   ((aggregate * 100.) / total)))

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
        Pause the ui on the main window and destroy the canvas objects
        in order to close the application witout errors
        """
        self.dynamic_canvas.pause_animation()
        self.dynamic_canvas.destroy()
        self.close()

    def closeEvent(self, ce):
        """ Handle the window close event"""
        self.fileQuit()

    def about(self):
        """Shows the about dialog"""

        QtWidgets.QMessageBox.about(self,
                                ("%s") % "About", \
                                """
                                <br><b>Asphalt Mixtures Aging Simulator</b>
                                <p>Copyright &copy; 2014-2015 Jeison Pacateque, Santiago Puerto, Wilmar Fernandez
                                <br>Licensed under the terms of the GNU GPLv3 License
                                <p>Created by Jeison Pacateque, Santiago Puerto and Wilmar Fernandez
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

                                <p>Pavements and Sustainable Materials Research Group
                                <br>Grupo de Investigaci&oacute;n en Pavimentos y Materiales Sostenibles
                                <br>Universidad Distrital Francisco Jos&eacute; de Caldas
                                """)

    def help_dialog(self):
        QtWidgets.QMessageBox.about(self, "Help",
                                """<b>Asphalt Mixtures Aging Simulator</b>

        <p>You can find <a href="http://asphalt-mixtures-aging-simulator.readthedocs.org"> here </a>
        the complete documentation of the project.

        <p>Pavements and Sustainable Materials Research Group<br/>
        Universidad Distrital Francisco Jos&eacute; de Caldas
        """)

    def get_collection(self):
        return self.collection

    def set_collection(self, collection):
        self.collection = collection

    def setup_simulation(self):
        """Shows the configure simulation dialog"""

        self.config_dialog = ConfigureSimulationDialog(self.collection)
        #self.config_dialog.exec_()  # Prevents the dialog to disappear
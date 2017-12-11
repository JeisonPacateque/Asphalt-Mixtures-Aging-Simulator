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

from PyQt5 import QtWidgets, QtCore

from app.graphic_controller import SimulationController
from app.output.results import Result

class ConfigureSimulationDialog(QtWidgets.QDialog):
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
        self.title = QtWidgets.QLabel('<b> Select the vertical slice </b>')

        self.slider = QtWidgets.QSlider()
        self.slider.setGeometry(QtCore.QRect(120, 380, 321, 31))
        self.slider.setOrientation(QtCore.Qt.Horizontal)
        print("valude size_z", self.size_Z)
        print("shape of collecton=", self.collection.shape)
        self.slider.setRange(0, self.size_Z)
        # self.slider.valueChanged.connect(self.changeText)
        self.lcd = QtWidgets.QLCDNumber(self) # replaces the QLineEdit() object
        # self.lcd.setDigitCount(2)
        self.slider.valueChanged.connect(self.lcd.display) # replaces the QLineEdit() object

        # self.sliderSelected = QtWidgets.QLineEdit()
        # self.sliderSelected.setGeometry(QtCore.QRect(112, 280, 331, 20))

        self.mechanicsLabel = QtWidgets.QLabel("<b> Young's modulus </b>")
        self.modulusAggregateLabel = QtWidgets.QLabel("Aggregate:")
        self.modulusMasticLabel = QtWidgets.QLabel("Mastic:")
        self.modulusAirLabel = QtWidgets.QLabel("Air voids:")
        self.mechanicalForceLabel = QtWidgets.QLabel("Applied force: ")

        self.aggregate_YM = QtWidgets.QLineEdit()
        self.mastic_YM = QtWidgets.QLineEdit()
        self.air_YM = QtWidgets.QLineEdit()
        self.mechanicalForceEdit = QtWidgets.QLineEdit()

        self.thermalLabel = QtWidgets.QLabel("<b> Thermal conductivity </b>")
        self.thermalAggregateLabel = QtWidgets.QLabel("Aggregate:")
        self.thermalMasticLabel = QtWidgets.QLabel("Mastic:")
        self.thermalAirLabel = QtWidgets.QLabel("Air voids:")

        self.aggregate_TC = QtWidgets.QLineEdit()
        self.mastic_TC = QtWidgets.QLineEdit()
        self.air_TC = QtWidgets.QLineEdit()

        self.chemicalLabel = QtWidgets.QLabel("<b> Chemical constants </b>")
        self.chemicalAggregateLabel = QtWidgets.QLabel("Chemical value1:")
        self.chemicalMasticLabel = QtWidgets.QLabel("Chemical value2:")
        self.chemicalAirLabel = QtWidgets.QLabel("Chemical value3:")

        self.thermalStepsLabel = QtWidgets.QLabel("Steps:")
        self.thermalSteps = QtWidgets.QLineEdit()

        self.aggregate_CH = QtWidgets.QLineEdit()
        self.mastic_CH = QtWidgets.QLineEdit()
        self.air_CH = QtWidgets.QLineEdit()

        self.runSimulationButton = QtWidgets.QPushButton('Run simulation', self)
        self.runSimulationButton.clicked[bool].connect(self.runSimulation)  # Listener

        self.cancelButton = QtWidgets.QPushButton('Cancel', self)
        self.cancelButton.clicked[bool].connect(self.closeWindow)

        self.grid = QtWidgets.QGridLayout()
        self.grid.setSpacing(2)

        self.grid.addWidget(self.title, 0, 0)

        self.grid.addWidget(self.slider, 1, 0)
        # self.grid.addWidget(self.sliderSelected, 1, 1)
        self.grid.addWidget(self.lcd, 1, 1)

        self.grid.addWidget(self.mechanicsLabel, 2, 0)
        self.grid.addWidget(self.modulusAggregateLabel, 3, 0)
        self.grid.addWidget(self.aggregate_YM, 3, 1)
        self.grid.addWidget(self.mechanicalForceLabel, 3, 2)
        self.grid.addWidget(self.mechanicalForceEdit, 3, 3)
        self.grid.addWidget(self.modulusMasticLabel, 4, 0)
        self.grid.addWidget(self.mastic_YM, 4, 1)
        self.grid.addWidget(self.modulusAirLabel, 5, 0)
        self.grid.addWidget(self.air_YM, 5, 1)

        # ==============================================================================
        # This graphical elements are commented because modifying those values strongly
        # affect the behavior of the simulation
        # ==============================================================================


        self.grid.addWidget(self.thermalLabel, 6, 0)
        #        self.grid.addWidget(self.thermalAggregateLabel, 7, 0)
        #        self.grid.addWidget(self.aggregate_TC, 7, 1)
        #        self.grid.addWidget(self.thermalMasticLabel, 8, 0)
        #        self.grid.addWidget(self.mastic_TC, 8, 1)
        #        self.grid.addWidget(self.thermalAirLabel, 9, 0)
        #        self.grid.addWidget(self.air_TC, 9, 1)
        self.grid.addWidget(self.thermalStepsLabel, 7, 1)
        self.grid.addWidget(self.thermalSteps, 7, 2)

        #        self.grid.addWidget(self.chemicalLabel, 10, 0)
        #        self.grid.addWidget(self.chemicalAggregateLabel, 11, 0)
        #        self.grid.addWidget(self.aggregate_CH, 11, 1)
        #        self.grid.addWidget(self.chemicalMasticLabel, 12, 0)
        #        self.grid.addWidget(self.mastic_CH, 12, 1)
        #        self.grid.addWidget(self.chemicalAirLabel, 13, 0)
        #        self.grid.addWidget(self.air_CH, 13, 1)

        self.grid.addWidget(self.runSimulationButton, 14, 1)
        self.grid.addWidget(self.cancelButton, 14, 2)

        self.setLayout(self.grid)
        self.setGeometry(10, 35, 560, 520)

        window_size = self.geometry()
        left = window_size.left()
        right = window_size.right() - 500
        top = window_size.top() + 200
        bottom = window_size.bottom() - 20

        self.window_size = QtCore.QRect(left, top, bottom, right)
        self.setWindowTitle('Configure Simulation')
        self.setDefaultValues()
        self.show()

    def closeWindow(self):
        self.close()

    def changeText(self, value):
        # deprecated
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
        target_slice = self.size_Z / 2

        mechanical_force = 800

        self.aggregate_YM.setText(str(E2))
        self.mastic_YM.setText(str(E1))
        self.air_YM.setText(str(E0))
        self.aggregate_TC.setText(str(conductRock))
        self.mastic_TC.setText(str(conductAsphalt))
        self.air_TC.setText(str(conductAir))
        self.thermalSteps.setText(str(steps))
        self.mechanicalForceEdit.setText(str(mechanical_force))
        # self.sliderSelected.setText(str(target_slice))
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

        # slice_id = int(self.sliderSelected.text())
        slice_id = int(self.lcd.value())
        print("slice_id", slice_id)
        # Close the dialog before the simulation starts

        self.progressBar = QtWidgets.QProgressBar(self)
        self.progressBar.setGeometry(QtCore.QRect(self.window_size))
        self.controller = SimulationController(self.collection, slice_id, **options)

        def onFinished():
            self.progressBar.setRange(0, 1)
            self.progressBar.setValue(1)
            self.progressBar.hide()
            data1, data2 = self.controller.getData()
            output_results1 = Result(data1, "data1")
            output_results1.showResults()
            output_results2 = Result(data2, "data2")
            output_results2.showResults()
            QtWidgets.QMessageBox.about(self, "Information:",
                                    "Simulation done, results saved at Results folder")

        self.controller.finished.connect(onFinished)
        self.controller.start()
        self.progressBar.show()
        self.progressBar.setRange(0, 0)
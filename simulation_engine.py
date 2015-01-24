# -*- coding: utf-8 -*-
"""
Created on Fri Jan 16 20:33:56 2015

@author: Santiago
"""
import sys
from PyQt4 import QtGui
from thermal_model import ThermalModel
from fem_mechanics import FEMMechanics

class SimulationEngine(object):
    def __init__(self, Material):
        self.Material = Material
        self.configureWindow = ConfigureSimulationDialog()
        self.configureWindow.setDefaultValues(
            self.Material.E2,
            self.Material.E1,
            self.Material.E0,
            self.Material.conductAsphalt,
            self.Material.conductRock,
            self.Material.conductAir
        )
        self.configureWindow.exec_() #Prevents the dialog to disappear
        self.Thermal = ThermalModel(self.Material)
        self.Mechanics = FEMMechanics(self.Material)


class ConfigureSimulationDialog(QtGui.QDialog):

    def __init__(self):
        super(ConfigureSimulationDialog, self).__init__()

        self.title = QtGui.QLabel('Configure the physical constants')

        self.mechanicsLabel = QtGui.QLabel("Young's modulus")
        self.modulusAggregateLabel = QtGui.QLabel("Aggregate:")
        self.modulusMasticLabel = QtGui.QLabel("Mastic:")
        self.modulusAirLabel = QtGui.QLabel("Air voids:")

        self.modulusAggregateEdit = QtGui.QLineEdit()
        self.modulusMasticEdit = QtGui.QLineEdit()
        self.modulusAirEdit = QtGui.QLineEdit()

        self.thermalLabel = QtGui.QLabel("Thermal conductivity")
        self.thermalAggregateLabel = QtGui.QLabel("Aggregate:")
        self.thermalMasticLabel = QtGui.QLabel("Mastic:")
        self.thermalAirLabel = QtGui.QLabel("Air voids:")

        self.thermalAggregateEdit = QtGui.QLineEdit()
        self.thermalMasticEdit = QtGui.QLineEdit()
        self.thermalAirEdit = QtGui.QLineEdit()

        self.chemicalLabel = QtGui.QLabel("Chemical constants")
        self.chemicalAggregateLabel = QtGui.QLabel("Chemical value1:")
        self.chemicalMasticLabel = QtGui.QLabel("Chemical value2:")
        self.chemicalAirLabel = QtGui.QLabel("Chemical value3:")

        self.chemicalAggregateEdit = QtGui.QLineEdit()
        self.chemicalMasticEdit = QtGui.QLineEdit()
        self.chemicalAirEdit = QtGui.QLineEdit()

        self.runSimulationButton = QtGui.QPushButton('Run simulation', self)
        self.runSimulationButton.clicked[bool].connect(self.runSimulation) #Listener

        self.cancelButton =  QtGui.QPushButton('Cancel', self)
        self.cancelButton.clicked[bool].connect(self.closeWindow)

        self.grid = QtGui.QGridLayout()
        self.grid.setSpacing(1)

        self.grid.addWidget(self.title, 1, 0)

        self.grid.addWidget(self.mechanicsLabel, 2, 0)
        self.grid.addWidget(self.modulusAggregateLabel, 3, 0)
        self.grid.addWidget(self.modulusAggregateEdit, 3, 1)
        self.grid.addWidget(self.modulusMasticLabel, 4, 0)
        self.grid.addWidget(self.modulusMasticEdit, 4, 1)
        self.grid.addWidget(self.modulusAirLabel, 5, 0)
        self.grid.addWidget(self.modulusAirEdit, 5, 1)

        self.grid.addWidget(self.thermalLabel, 6, 0)
        self.grid.addWidget(self.thermalAggregateLabel, 7, 0)
        self.grid.addWidget(self.thermalAggregateEdit, 7, 1)
        self.grid.addWidget(self.thermalMasticLabel, 8, 0)
        self.grid.addWidget(self.thermalMasticEdit, 8, 1)
        self.grid.addWidget(self.thermalAirLabel, 9, 0)
        self.grid.addWidget(self.thermalAirEdit, 9, 1)

        self.grid.addWidget(self.chemicalLabel, 10, 0)
        self.grid.addWidget(self.chemicalAggregateLabel, 11, 0)
        self.grid.addWidget(self.chemicalAggregateEdit, 11, 1)
        self.grid.addWidget(self.chemicalMasticLabel, 12, 0)
        self.grid.addWidget(self.chemicalMasticEdit, 12, 1)
        self.grid.addWidget(self.chemicalAirLabel, 13, 0)
        self.grid.addWidget(self.chemicalAirEdit, 13, 1)

        self.grid.addWidget(self.runSimulationButton, 14, 1)
        self.grid.addWidget(self.cancelButton, 14, 2)


        self.setLayout(self.grid)

        self.setGeometry(300, 300, 350, 300)
        self.setWindowTitle('Configure Simulation')
        self.show()


    def setDefaultValues(self, E2, E1, E0, conductAsphalt, conductRock, conductAir):
        self.modulusAggregateEdit.setText(str(E2))
        self.modulusMasticEdit.setText(str(E1))
        self.modulusAirEdit.setText(str(E0))
        self.thermalAggregateEdit.setText(str(conductRock))
        self.thermalMasticEdit.setText(str(conductAsphalt))
        self.thermalAirEdit.setText(str(conductAir))
        self.chemicalAggregateEdit.setText('Chem Aggregate')
        self.chemicalMasticEdit.setText('Chem Mastic')
        self.chemicalAirEdit.setText('Chem Air')

    def runSimulation(self):
        print "Running simulation..."
        SimulationEngine.Thermal.runSimulation()
    def closeWindow(self):
        self.close()

#------------------------------------------------------------------------------
if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)
    ex = ConfigureSimulationDialog()
    sys.exit(app.exec_())
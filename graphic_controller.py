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

from simulation.simulation_engine import SimulationEngine
from imgprocessing.segmentation import Segmentation
from PyQt5 import QtCore

class GraphicController(QtCore.QThread, QtCore.QObject):
    def __init__(self, collection, parent=None):
        QtCore.QObject.__init__(self, parent)
        self.data = collection

    def getData(self):
        return self.data

class SegmentationController(GraphicController):
    finished = QtCore.pyqtSignal()
    def __init__(self, collection):
        super(SegmentationController, self).__init__(collection)
        self.segmenter = Segmentation()

    def run(self):
        reduced = self.segmenter.reduction(self.data)
        self.data = self.segmenter.segment_all_samples(reduced)

#        self.emit(QtCore.SIGNAL("finished()"))
        self.finished.emit()

class SimulationController(GraphicController):
    finished = QtCore.pyqtSignal()
    def __init__(self, collection, slice_id, **options):
        super(SimulationController, self).__init__(collection)
        self.physical_cons = options['physical_cons']
        self.inputs = options['inputs']
        self.slice_id = slice_id

    def run(self):
        self.engine = SimulationEngine(self.data, self.slice_id, **self.physical_cons)
        self.data = self.engine.simulationCicle(**self.inputs)
        self.finished.emit()

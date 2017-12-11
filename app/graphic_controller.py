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

from app.simulation.simulation_engine import SimulationEngine
from app.imgprocessing.segmentation import Segmentation
from PyQt5 import QtCore
from app.signals import signals

class GraphicController(QtCore.QThread):
    def __init__(self, collection, parent=None):
        QtCore.QObject.__init__(self, parent)
        self.data = collection

    def getData(self):
        return self.data

class SegmentationController(GraphicController):

    def __init__(self, collection):
        super(SegmentationController, self).__init__(collection)
        self.segmenter = Segmentation()

    def run(self):
        reduced = self.segmenter.reduction(self.data)
        self.data = self.segmenter.segment_all_samples(reduced)

        signals.segmentation_finished.emit()

class SimulationController(GraphicController):

    def __init__(self, collection, slice_id, **options):
        super(SimulationController, self).__init__(collection)
        self.physical_cons = options['physical_cons']
        self.inputs = options['inputs']
        self.slice_id = slice_id

    def run(self):
        self.engine = SimulationEngine(self.data, self.slice_id, **self.physical_cons)
        self.data = self.engine.simulationCicle(**self.inputs)
        signals.simulation_finished.emit()

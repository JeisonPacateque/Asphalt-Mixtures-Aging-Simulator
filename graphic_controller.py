# -*- coding: utf-8 -*-
"""
Created on Tue Mar  3 20:35:32 2015

@author: sjdps
"""
from simulation.simulation_engine import SimulationEngine
from imgprocessing.segmentation import Segmentation
from PyQt4 import QtCore

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
                                            
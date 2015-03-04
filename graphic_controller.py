# -*- coding: utf-8 -*-
"""
Created on Tue Mar  3 20:35:32 2015

@author: sjdps
"""
from simulation.simulation_engine import SimulationEngine
from imgprocessing.segmentation import Segmentation
from PyQt4 import QtCore
from time import sleep

class GraphicController(QtCore.QThread):
    def __init__(self, collection, parent=None): 
        QtCore.QThread.__init__(self, parent)
        self.collection = collection
        
    def getCollection(self):
        return self.collection

class SegmentationController(GraphicController):
    def __init__(self, collection):
        super(SegmentationController, self).__init__(collection)
        self.segmenter = Segmentation()

    def run(self):
        reduced = self.segmenter.reduction(self.collection)
        self.collection = self.segmenter.segment_all_samples(reduced)
        
        self.emit(QtCore.SIGNAL("finished()"))

class SimulationController(GraphicController):
    def __init__(self, collection, slice_id, **options):
        
        self.physical_cons = options['physical_cons']
        self.inputs = options['inputs']
        super(SimulationController, self).__init__(collection)
        self.engine = SimulationEngine(self.collection, slice_id,
                                       **self.physical_cons)
    
    def run(self):
#        self.materials = self.engine.simulationCicle(**self.inputs['inputs'])
        sleep(5)
        self.finished.emit()
#        self.emit(QtCore.SIGNAL("done()"))
    
#    def output(self):
#        output_results = Result(materials)
#        output_results.showResults()                                           
                                            
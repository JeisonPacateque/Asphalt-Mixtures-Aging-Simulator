# -*- coding: utf-8 -*-
"""
Created on Tue Mar  3 20:35:32 2015

@author: sjdps
"""

from PyQt4 import QtCore
       
class GraphicController(QtCore.QThread):
    def __init__(self): 
#        taskFinished = QtCore.pyqtSignal()
        super(GraphicController, self).__init__()

    def run(self):
        pass

class SegmentationController(GraphicController):   
    taskFinished = QtCore.pyqtSignal()
    def __init__(self, collection):
        super(SegmentationController, self).__init__()
        from imgprocessing.segmentation import Segmentation
        self.segmenter = Segmentation()
        self.collection = collection
    
    def run(self):
        reduced = self.segmenter.reduction(self.collection)
        self.collection = self.segmenter.segment_all_samples(reduced)
        
        self.taskFinished.emit()
    
    def getCollection(self):
        return self.collection

#class SimulationController(GraphicController):
#    def __init__(self):
#        super(SimulationController, self).__init__()
#        from simulation.simulation_engine import SimulationEngine
#        engine = SimulationEngine(aggregate_parameters, mastic_parameters,
#                                  air_parameters, self.collection, slice_parameter)
#    
#    def run(self):
#        materials = engine.simulationCicle(no_thermal_iter=thermal_steps,
#                                           mechanical_force = force_parameter)
        
    
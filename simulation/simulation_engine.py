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

from thermal_model import ThermalModel
from fem_mechanics import FEMMechanics
from chemical_model import ChemicalModel
import numpy as np
from material import Material
import copy

class SimulationEngine(object):
    """
    This class configures the sample as a materials array in order to run the
    simulations defined in the thermal, mechanical and chemical models.
    """
    def __init__(self, collection, slice_id, **physical_cons):

        self.collection = collection

        # materials creation
        self.mastic = Material('mastic',
                               physical_cons['mastic_YM'], # young modulus
                               physical_cons['mastic_TC'], # thermal conducticity
                               physical_cons['mastic_CH']) # chemical
                               
        self.aggregate = Material('aggregate',
                                  physical_cons['aggregate_YM'],
                                  physical_cons['aggregate_TC'],
                                  physical_cons['aggregate_CH'])
                                    
        self.airvoid = Material('airvoid',
                                physical_cons['air_YM'],
                                physical_cons['air_TC'],
                                physical_cons['air_CH'])

        vertical_slice = self._loadVerticalSlice(slice_id)

        # Structure data where the simulation takes place
        self.matrix_materials = self._getMatrixMaterials(vertical_slice)

    def _loadVerticalSlice(self, slice_id):
        """Cut the slice of the collection in the position id"""
        vertical_slice = self.collection[:, :, slice_id]
        vertical_slice = vertical_slice.copy() # avoid side effects
        return vertical_slice.transpose()

    def _getMatrixMaterials(self, vertical_slice):
        """Create the matrix material from a vertical slice"""
        material_matrix = np.empty(vertical_slice.shape, dtype=object)

        for (x,y), _ in np.ndenumerate(vertical_slice):
            if vertical_slice[x, y] == 2:
                material_matrix[x,y] = copy.deepcopy(self.aggregate)
            elif vertical_slice[x,y] == 1:
                material_matrix[x,y] = copy.deepcopy(self.mastic)
            elif vertical_slice[x,y] == 0 or  vertical_slice[x,y] == -1:
                material_matrix[x,y] = copy.deepcopy(self.airvoid)

        print "Materials matrix created, size:", material_matrix.shape
        return material_matrix
    
    def _calcNewModules(self, MM):
        print "recalculando los modulos"
        for i in xrange(MM.shape[0]):
            for j in xrange(MM.shape[1]):
                if MM[i,j].phase == 'mastic':
                    if MM[i,j].temperature <= 20:
                        MM[i,j].young_modulus = 16030
                        
                    elif MM[i,j].temperature <= 35:
                        MM[i,j].young_modulus = 5148
                        
                    else:
                        MM[i,j].young_modulus = 1527
        
    def simulationCicle(self, **inputs):
#==============================================================================
#       Thermal model implementation (Every model should run on a loop)
#==============================================================================
        max_TC = max(self.mastic.thermal_conductivity,
                     self.airvoid.thermal_conductivity,
                     self.aggregate.thermal_conductivity)
        
        self.chemical = ChemicalModel(self.matrix_materials)
        self.chemical.applySimulationConditions(74.47)
        self.matrix_materials = self.chemical.simulate()
        
        self.mechanics = FEMMechanics(self.matrix_materials)
        self.mechanics.applySimulationConditions(inputs['force_input'])
        self.matrix_materials = self.mechanics.simulate()
        
        data1 = self.matrix_materials.copy()

        self.thermal = ThermalModel(self.matrix_materials, max_TC)
        self.thermal.applySimulationConditions()
        self.matrix_materials = self.thermal.simulate(inputs['thermal_steps'])
        
        self._calcNewModules(self.matrix_materials)
        # cambiar la energia de activacion para correr el segundo modelo quimico
        
        self.chemical = ChemicalModel(self.matrix_materials)
        #A little change in the energy activation(EA) is emplemented
        # from a increase of 3.13 of the rca in three moths
        # it's obtained the following change in EA
        # 3.9700659563673262303399289700659563673262303399289700659*10e-7 each second
        # in 4 hours, that is, 144000 seconds, rca would increase 313/5475
        self.chemical.applySimulationConditions(313/5475.)
        self.matrix_materials = self.chemical.simulate()
        
        self.mechanics = FEMMechanics(self.matrix_materials)
        self.mechanics.applySimulationConditions(inputs['force_input'])
        self.matrix_materials = self.mechanics.simulate()
        
        data2 = self.matrix_materials.copy()       
        
        return data1, data2
from __future__ import print_function


__author__ = ["Tomas Mendez Echenagucia"]
__copyright__ = "Copyright 2020, Design Machine Group - University of Washington"
__license__ = "MIT License"
__email__ = "tmendeze@uw.edu"
__version__ = "0.1.0"

import os
import json
import compas_energyplus
from compas_energyplus.datastructures import Material
from compas_energyplus.datastructures import MaterialNoMass


m1 = Material()
m1.name                = 'C5 - 4 IN HW CONCRETE'
m1.roughness           = 'MediumRough'         
m1.thickness           = 0.1014984           
m1.conductivity        = 1.729577            
m1.density             = 2242.585            
m1.specific_heat       = 836.8000            
m1.thermal_absorptance = 0.9000000           
m1.solar_absorptance   = 0.6500000           
m1.visible_absorptance = 0.6500000           

m2 = MaterialNoMass()
m2.name                      = 'R13LAYER'
m2.roughness                 = 'Rough'
m2.thermal_resistance        = 2.290965
m2.thermal_absorptance       = 0.9000000
m2.solar_absorptance         = 0.7500000
m2.visible_absorptance       = 0.7500000

m3 = MaterialNoMass()
m3.name                      = 'R31LAYER'
m3.roughness                 = 'Rough'
m3.thermal_resistance        = 5.456
m3.thermal_absorptance       = 0.900000000
m3.solar_absorptance         = 0.750000000
m3.visible_absorptance       = 0.750000000


materials = [m1, m2, m3]
data = {}
for mat in materials:
    data[mat.name] = mat.data

filepath = os.path.join(compas_energyplus.DATA, 'materials', 'material_library_simple.json')
with open(filepath, 'w+') as fp:
    json.dump(data, fp)


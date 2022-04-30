from __future__ import print_function

import compas_energyplus

__author__ = ["Tomas Mendez Echenagucia"]
__copyright__ = "Copyright 2020, Design Machine Group - University of Washington"
__license__ = "MIT License"
__email__ = "tmendeze@uw.edu"
__version__ = "0.1.0"

import os
import json
from compas_energyplus.datastructures import Material


m1 = Material()
m1.name                = 'ExtFraming'
m1.roughness           = 'MediumRough'
m1.thickness           = 0.0254
m1.conductivity        = 1.802
m1.density             = 2255
m1.specific_heat       = 750
m1.thermal_absorptance = 0.9
m1.solar_absorptance   = 0.7
m1.visible_absorptance = 0.7


m2 = Material()
m2.name                = 'FacadeCladding'
m2.roughness           = 'MediumRough'
m2.thickness           = 0.0006
m2.conductivity        = 70
m2.density             = 2700
m2.specific_heat       = 870
m2.thermal_absorptance = 0.9
m2.solar_absorptance   = 0.7
m2.visible_absorptance = 0.7


m2 = Material()
m2.name                = 'Generic 25mm Insulation'
m2.roughness           = 'MediumRough'
m2.thickness           = 0.05
m2.conductivity        = 0.03
m2.density             = 43
m2.specific_heat       = 1210
m2.thermal_absorptance = 0.9
m2.solar_absorptance   = 0.7
m2.visible_absorptance = 0.7


m3 = Material()
m3.name                = 'Generic 25mm Wood'
m3.roughness           = 'MediumSmooth'
m3.thickness           = 0.0254
m3.conductivity        = 0.15
m3.density             = 608
m3.specific_heat       = 1630
m3.thermal_absorptance = 0.9
m3.solar_absorptance   = 0.5
m3.visible_absorptance = 0.5


m4 = Material()
m4.name                = 'Generic 50mm Insulation'
m4.roughness           = 'MediumRough'
m4.thickness           = 0.05
m4.conductivity        = 0.03
m4.density             = 43
m4.specific_heat       = 1210
m4.thermal_absorptance = 0.9
m4.solar_absorptance   = 0.7
m4.visible_absorptance = 0.7


m5 = Material()
m5.name                = 'Generic Acoustic Tile'
m5.roughness           = 'MediumSmooth'
m5.thickness           = 0.02
m5.conductivity        = 0.06
m5.density             = 368
m5.specific_heat       = 590
m5.thermal_absorptance = 0.9
m5.solar_absorptance   = 0.2
m5.visible_absorptance = 0.2

materials = [m1, m2, m3, m4, m5]
data = {}
for mat in materials:
    data[mat.name] = mat.data

filepath = os.path.join(compas_energyplus.DATA, 'materials', 'material_library1.json')
with open(filepath, 'w+') as fp:
    json.dump(data, fp)


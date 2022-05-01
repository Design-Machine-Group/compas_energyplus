from __future__ import print_function


__author__ = ["Tomas Mendez Echenagucia"]
__copyright__ = "Copyright 2020, Design Machine Group - University of Washington"
__license__ = "MIT License"
__email__ = "tmendeze@uw.edu"
__version__ = "0.1.0"

import os
import json
import compas_energyplus
from compas_energyplus.datastructures import Construction


c1 = Construction()
c1.name = 'ExtFraming'
c1.layers = ['ExteriorWall_05cef855',
             'FacadeCladding',       
             'AirGap',               
             'ContExtInsulation',    
             'ExtFraming']


# materials = [m1, m2, m3, m4, m5, m6, m7, m8, m9, m10, m11, m12]
# data = {}
# for mat in materials:
#     data[mat.name] = mat.data

# filepath = os.path.join(compas_energyplus.DATA, 'materials', 'material_library1.json')
# with open(filepath, 'w+') as fp:
#     json.dump(data, fp)


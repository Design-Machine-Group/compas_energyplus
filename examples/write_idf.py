from __future__ import print_function

__author__ = ["Tomas Mendez Echenagucia"]
__copyright__ = "Copyright 2020, Design Machine Group - University of Washington"
__license__ = "MIT License"
__email__ = "tmendeze@uw.edu"
__version__ = "0.1.0"

import os
import compas_energyplus
from compas_energyplus.datastructures import Building

for i in range(50): print('')

b = Building()
b.filepath = os.path.join(compas_energyplus.TEMP, 'idf_testing.idf')
b.write_idf()

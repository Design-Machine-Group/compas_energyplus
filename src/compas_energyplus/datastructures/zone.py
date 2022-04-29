from __future__ import print_function

__author__ = ["Tomas Mendez Echenagucia"]
__copyright__ = "Copyright 2020, Design Machine Group - University of Washington"
__license__ = "MIT License"
__email__ = "tmendeze@uw.edu"
__version__ = "0.1.0"

import os
from compas.datastructures import Mesh

class Zone(Mesh):
    def __init__(self):
        super(Mesh, self).__init__()

        self.default_face_attributes.update({'name': None,
                                             'construction':None,
                                             'adiabatic':False,
                                             })
    
    def __str__(self):
        return 'compas_energyplus Zone - {}'.format(self.name)

    def assign_zone_surface_attributes(self):

        self.face_attribute(0, 'Name', 'floor')
        self.face_attribute(0, 'construction', 'floor')
        self.face_attribute(0, 'adiabatic', True)

        self.face_attribute(1, 'Name', 'ceiling')
        self.face_attribute(1, 'construction', 'ceiling')
        self.face_attribute(1, 'adiabatic', True)

        self.faces_attribute('Name', 'wall', [2, 3, 4, 5])
        self.faces_attribute('construction', 'wall', [2, 3, 4, 5])
        self.faces_attribute('adiabatic', False, [2, 3, 4, 5])


from __future__ import print_function

__author__ = ["Tomas Mendez Echenagucia"]
__copyright__ = "Copyright 2020, Design Machine Group - University of Washington"
__license__ = "MIT License"
__email__ = "tmendeze@uw.edu"
__version__ = "0.1.0"

import os
import json
from compas.datastructures import Mesh

# TODO: Make custom object, use mesh only for surfaces

class Zone(object):
    def __init__(self):
        self.name =  ''
        self.surfaces = None

    def to_json(self, filepath):
        with open(filepath, 'w+') as fp:
            json.dump(self.data, fp)

    @property
    def data(self):
        data = {'name'                  : self.name,
                'surfaces'              : self.surfaces.to_data(),
                }
        return data
    
    @data.setter
    def data(self, data):
        surfaces = data.get('surfaces') or {}
        self.name               = data.get('name') or {}
        self.surfaces      = ZoneSurfaces.from_data(surfaces)


    def add_surfaces(self, mesh):
        self.surfaces = ZoneSurfaces.from_data(mesh.data)
        self.surfaces.assign_zone_surface_attributes()


    @classmethod
    def from_json(cls, filepath):
        with open(filepath, 'r') as fp:
            data = json.load(fp)
        zone = cls()
        zone.data = data
        return zone



class ZoneSurfaces(Mesh):
    def __init__(self):
        super(Mesh, self).__init__()

        self.default_face_attributes.update({'name': None,
                                             'construction':None,
                                             'surface_type': None,
                                             'outside_boundary_condition': None,
                                             })
    
    def __str__(self):
        return 'compas_energyplus Zone Surfaces - {}'.format(self.name)

    def assign_zone_surface_attributes(self):

        self.face_attribute(0, 'Name', 'floor')
        self.face_attribute(0, 'surface_type', 'Floor')
        self.face_attribute(0, 'construction', 'Interior Floor')
        self.face_attribute(0, 'outside_boundary_condition', 'Adiabatic')

        self.face_attribute(1, 'Name', 'ceiling')
        self.face_attribute(1, 'surface_type', 'Ceiling')
        self.face_attribute(0, 'construction', 'Interior Ceiling')
        self.face_attribute(1, 'outside_boundary_condition', 'Adiabatic')

        self.faces_attribute('Name', 'wall', [2, 3, 4, 5])
        self.faces_attribute('surface_type', 'Wall', [2, 3, 4, 5])
        self.faces_attribute('construction', 'Exterior Wall', [2, 3, 4, 5])
        self.faces_attribute('outside_boundary_condition', 'Outdoors', [2, 3, 4, 5])


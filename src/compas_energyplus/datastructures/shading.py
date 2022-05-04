from __future__ import print_function

__author__ = ["Tomas Mendez Echenagucia"]
__copyright__ = "Copyright 2020, Design Machine Group - University of Washington"
__license__ = "MIT License"
__email__ = "tmendeze@uw.edu"
__version__ = "0.1.0"


import json
from compas.datastructures import Mesh


class Shading(object):
    def __init__(self):
        self.name =  'Shading'
        self.mesh = None

    def to_json(self, filepath):
        with open(filepath, 'w+') as fp:
            json.dump(self.data, fp)

    @property
    def data(self):
        data = {'name'              : self.name,
                'mesh'              : self.mesh.to_data(),
                }
        return data
    
    @data.setter
    def data(self, data):
        mesh           = data.get('mesh') or {}
        self.name      = data.get('name') or {}
        self.mesh      = Mesh.from_data(mesh)


    def add_mesh(self, mesh):
        self.mesh = mesh

    @classmethod
    def from_data(cls, data):
        zone = cls()
        zone.data = data
        return zone

    @classmethod
    def from_json(cls, filepath):
        with open(filepath, 'r') as fp:
            data = json.load(fp)
        zone = cls()
        zone.data = data
        return zone



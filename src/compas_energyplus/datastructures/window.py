from __future__ import print_function

__author__ = ["Tomas Mendez Echenagucia"]
__copyright__ = "Copyright 2020, Design Machine Group - University of Washington"
__license__ = "MIT License"
__email__ = "tmendeze@uw.edu"
__version__ = "0.1.0"

import os
import json

# TODO: implement from wall and WWR

class Window(object):
    def __init__(self):
        self.name = None
        self.nodes = None
        self.building_surface = None
        self.construction = None
    
    @classmethod
    def from_wall_and_wwr(self, zone, wall_key, wwr):
        pass

    def to_json(self, filepath):
        with open(filepath, 'w+') as fp:
            json.dump(self.data, fp)

    @property
    def data(self):
        data = {'name'                  : self.name,
                'nodes'                 : self.nodes,
                'building_surface'      : self.building_surface,
                'construction'          : self.construction,
                }
        return data
    
    @data.setter
    def data(self, data):
        self.name               = data.get('name') or {}
        self.nodes              = data.get('nodes') or {}
        self.building_surface   = data.get('building_surface') or {}
        self.construction       = data.get('construction') or {}

    @classmethod
    def from_json(cls, filepath):
        with open(filepath, 'r') as fp:
            data = json.load(fp)
        window = cls()
        window.data = data
        return window
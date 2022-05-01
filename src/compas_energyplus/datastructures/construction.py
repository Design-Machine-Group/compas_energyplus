from __future__ import print_function

__author__ = ["Tomas Mendez Echenagucia"]
__copyright__ = "Copyright 2020, Design Machine Group - University of Washington"
__license__ = "MIT License"
__email__ = "tmendeze@uw.edu"
__version__ = "0.1.0"

import os
import json



class Construction(object):
    def __init__(self):
        self.name           = 'Construction'                   
        self.layers         = []

    def to_json(self, filepath):
        with open(filepath, 'w+') as fp:
            json.dump(self.data, fp)

    @property
    def data(self):
        data = {'name'      : self.name,
                'layers'    : self.layers,
                }
        return data
    
    @data.setter
    def data(self, data):
        self.name   = data.get('name') or {}
        self.layers = data.get('layers') or {}

    @classmethod
    def from_data(cls, data):
        construction = cls()
        construction.data = data
        return construction

    @classmethod
    def from_json(cls, filepath):
        with open(filepath, 'r') as fp:
            data = json.load(fp)
        construction = cls()
        construction.data = data
        return construction
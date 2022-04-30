from __future__ import print_function

__author__ = ["Tomas Mendez Echenagucia"]
__copyright__ = "Copyright 2020, Design Machine Group - University of Washington"
__license__ = "MIT License"
__email__ = "tmendeze@uw.edu"
__version__ = "0.1.0"

import os
import json


class Material(object):
    def __init__(self):
        self.name                       = 'Material'                   
        self.roughness                  = None
        self.thickness                  = None
        self.conductivity               = None
        self.density                    = None
        self.specific_heat              = None
        self.thermal_absorptance        = None
        self.solar_absorptance          = None
        self.visible_absorptance        = None
    

    def to_json(self, filepath):
        with open(filepath, 'w+') as fp:
            json.dump(self.data, fp)

    @property
    def data(self):
        data = {'name':                 self.name,
                'roughness':            self.roughness,
                'thickness':            self.thickness,
                'conductivity':         self.conductivity,
                'density':              self.density,
                'specific_heat':        self.specific_heat,
                'thermal_absorptance':  self.thermal_absorptance,
                'solar_absorptance':    self.solar_absorptance,
                'visible_absorptance':  self.visible_absorptance,
                }
        return data
    
    @data.setter
    def data(self, data):
        self.name                = data.get('name') or {}
        self.roughness           = data.get('roughness') or {}
        self.thickness           = data.get('thickness') or {}
        self.conductivity        = data.get('conductivity') or {}
        self.density             = data.get('density') or {}
        self.specific_heat       = data.get('specific_heat') or {}
        self.thermal_absorptance = data.get('thermal_absorptance') or {}
        self.solar_absorptance   = data.get('solar_absorptance') or {}
        self.visible_absorptance = data.get('visible_absorptance') or {}

    @classmethod
    def from_json(cls, filepath):
        with open(filepath, 'r') as fp:
            data = json.load(fp)
        material = cls()
        material.data = data
        return material
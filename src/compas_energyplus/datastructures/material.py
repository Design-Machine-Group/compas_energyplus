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
        self.__type__                   = 'Material'
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
        data = {'__type__':             self.__type__,
                'name':                 self.name,
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
        self.__type__            = data.get('__type__') or {}
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
    def from_data(cls, data):
        material = cls()
        material.data = data
        return material

    @classmethod
    def from_json(cls, filepath):
        with open(filepath, 'r') as fp:
            data = json.load(fp)
        material = cls()
        material.data = data
        return material


class MaterialNoMass(object):
    def __init__(self):
        self.__type__                   = 'MaterialNoMass'
        self.name                       = 'MaterialNoMass'
        self.roughness                  = None
        self.thermal_resistance         = None
        self.thermal_absorptance        = None
        self.solar_absorptance          = None
        self.visible_absorptance        = None
    

    def to_json(self, filepath):
        with open(filepath, 'w+') as fp:
            json.dump(self.data, fp)

    @property
    def data(self):
        data = {'__type__'              : self.__type__,
                'name'                  : self.name,
                'roughness'             : self.roughness,
                'thermal_resistance'    : self.thermal_resistance,
                'thermal_absorptance'   : self.thermal_absorptance,
                'thermal_absorptance'   : self.thermal_absorptance,
                'solar_absorptance'     : self.solar_absorptance,
                'visible_absorptance'   : self.visible_absorptance,
                }
        return data
    
    @data.setter
    def data(self, data):
        self.__type__            = data.get('__type__') or {}
        self.name                = data.get('name') or {}
        self.roughness           = data.get('roughness') or {}
        self.thermal_resistance  = data.get('thermal_resistance') or {}
        self.thermal_absorptance = data.get('thermal_absorptance') or {}
        self.thermal_absorptance = data.get('thermal_absorptance') or {}
        self.solar_absorptance   = data.get('solar_absorptance') or {}
        self.visible_absorptance = data.get('visible_absorptance') or {}

    @classmethod
    def from_data(cls, data):
        material = cls()
        material.data = data
        return material

    @classmethod
    def from_json(cls, filepath):
        with open(filepath, 'r') as fp:
            data = json.load(fp)
        material = cls()
        material.data = data
        return material


class WindowMaterialGas(object):
    def __init__(self):
        self.name              = 'WindowMaterialGas'                   
        self.gas_type          = None
        self.thickness         = None
    

    def to_json(self, filepath):
        with open(filepath, 'w+') as fp:
            json.dump(self.data, fp)

    @property
    def data(self):
        data = {'name'         : self.name,
                'gas_type'     : self.gas_type,
                'thickness'    : self.thickness,
                }
        return data
    
    @data.setter
    def data(self, data):
        self.name           = data.get('name') or {}
        self.gas_type       = data.get('gas_type') or {}
        self.thickness      = data.get('thickness') or {}

    @classmethod
    def from_data(cls, data):
        material = cls()
        material.data = data
        return material

    @classmethod
    def from_json(cls, filepath):
        with open(filepath, 'r') as fp:
            data = json.load(fp)
        material = cls()
        material.data = data
        return material


class WindowMaterialGlazing(object):
    def __init__(self):
        self.name                                       = 'WindowMaterialGlazing'                   
        self.optical_data_type                          = None
        self.win_glass_spectral_data_name               = None
        self.thickness                                  = None
        self.solar_transmittance                        = None
        self.front_solar_reflectance                    = None
        self.back_solar_reflectance                     = None 
        self.visible_transmittance                      = None    
        self.front_visible_reflectance                  = None
        self.back_visible_reflectance                   = None 
        self.infrared_transmittance                     = None     
        self.front_infrared_hemispherical_emissivity    = None
        self.back_infrared_hemispherical_emissivity     = None 
        self.conductivity                               = None                               
        self.dirt_correction_factor                     = None
        self.solar_diffusing                            = None


    def to_json(self, filepath):
        with open(filepath, 'w+') as fp:
            json.dump(self.data, fp)

    @property
    def data(self):
        data = {'name'                                      : self.name,                                   
                'optical_data_type'                         : self.optical_data_type,                     
                'win_glass_spectral_data_name'              : self.win_glass_spectral_data_name,
                'thickness'                                 : self.thickness,          
                'solar_transmittance'                       : self.solar_transmittance,                  
                'front_solar_reflectance'                   : self.front_solar_reflectance,                
                'back_solar_reflectance'                    : self.back_solar_reflectance,                 
                'visible_transmittance'                     : self.visible_transmittance,                  
                'front_visible_reflectance'                 : self.front_visible_reflectance,              
                'back_visible_reflectance'                  : self.back_visible_reflectance,               
                'infrared_transmittance'                    : self.infrared_transmittance,                 
                'front_infrared_hemispherical_emissivity'   : self.front_infrared_hemispherical_emissivity,
                'back_infrared_hemispherical_emissivity'    : self.back_infrared_hemispherical_emissivity, 
                'conductivity'                              : self.conductivity, 
                'dirt_correction_factor'                    : self.dirt_correction_factor,                 
                'solar_diffusing'                           : self.solar_diffusing,
                }
        return data
    
    @data.setter
    def data(self, data):
        self.name                                    = data.get('name') or {}
        self.optical_data_type                       = data.get('optical_data_type') or {}
        self.win_glass_spectral_data_name            = data.get('win_glass_spectral_data_name') or {}
        self.thickness                               = data.get('thickness') or {}
        self.solar_transmittance                     = data.get('solar_transmittance') or {}
        self.front_solar_reflectance                 = data.get('front_solar_reflectance') or {}
        self.back_solar_reflectance                  = data.get('back_solar_reflectance') or {}
        self.visible_transmittance                   = data.get('visible_transmittance') or {}
        self.front_visible_reflectance               = data.get('front_visible_reflectance') or {}
        self.back_visible_reflectance                = data.get('back_visible_reflectance') or {}
        self.infrared_transmittance                  = data.get('infrared_transmittance') or {}
        self.front_infrared_hemispherical_emissivity = data.get('front_infrared_hemispherical_emissivity') or {}
        self.back_infrared_hemispherical_emissivity  = data.get('back_infrared_hemispherical_emissivity') or {}
        self.conductivity                            = data.get('conductivity') or {}
        self.dirt_correction_factor                  = data.get('dirt_correction_factor') or {}
        self.solar_diffusing                         = data.get('solar_diffusing') or {}

    @classmethod
    def from_data(cls, data):
        material = cls()
        material.data = data
        return material

    @classmethod
    def from_json(cls, filepath):
        with open(filepath, 'r') as fp:
            data = json.load(fp)
        material = cls()
        material.data = data
        return material


if __name__ == '__main__':
    print('')
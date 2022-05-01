from __future__ import print_function

from compas_energyplus.datastructures.construction import Construction

__author__ = ["Tomas Mendez Echenagucia"]
__copyright__ = "Copyright 2020, Design Machine Group - University of Washington"
__license__ = "MIT License"
__email__ = "tmendeze@uw.edu"
__version__ = "0.1.0"

import os
import json
import compas_energyplus
import subprocess

from compas_energyplus.writer import write_idf
from compas_energyplus.datastructures.material import Material
from compas_energyplus.datastructures.material import MaterialNoMass
from compas_energyplus.datastructures.construction import Construction

class Building(object):
    def __init__(self, filepath, weather):
        self.filepath = filepath
        self.weather = weather

        self.name = 'Building'
        self.ep_version = '9.6'
        self.num_timesteps = 1
        self.terrain = 'City'
        self.solar_distribution = 'FullExteriorWithReflections'

        self.zones = {}
        self.windows = {}
        self.materials = {}
        self.window_materials_gas = {}
        self.window_materials_glazing = {}
        self.constructions = {}

    def write_idf(self):
        write_idf(self)

    def add_zone(self, zone):
        self.zones[len(self.zones)] = zone
    
    def add_window(self, window):
        self.windows[len(self.windows)] = window

    def add_material(self, material):
        self.materials[len(self.materials)] = material

    def add_materials_from_lib(self, lib):
        for mk in lib:
            t = lib[mk]['__type__']
            if t == 'Material':
                mat = Material.from_data(lib[mk])
            elif t == 'MaterialNoMass':
                mat = MaterialNoMass.from_data(lib[mk])
            else:
                continue
            self.add_material(mat)

    def add_constructions_from_lib(self, lib):
        for ck in lib:
            con = Construction.from_data(lib[ck])
            self.add_construction(con)

    def add_construction(self, construction):
        self.constructions[len(self.constructions)] = construction

    def analyze(self, exe=None):
        idf = self.filepath
        if not exe:
            eplus = 'energyplus'
        out = os.path.join(compas_energyplus.TEMP, 'eplus_output')
        print(exe, '-w', self.weather,'--output-directory', out, idf)
        subprocess.call([exe, '-w', self.weather,'--output-directory', out, idf])

if __name__ == '__main__':
    from compas_energyplus.datastructures import Zone
    from compas_energyplus.datastructures import Window

    for i in range(50): print('')

    data = compas_energyplus.DATA
    
    filepath = os.path.join(compas_energyplus.TEMP, 'idf_testing.idf')
    wea = os.path.join(data, 'weather_files', 'USA_WA_Seattle-Tacoma.Intl.AP.727930_TMY3.epw')
    # wea = os.path.join(data, 'weather_files', 'USA_CA_San.Francisco.Intl.AP.724940_TMY3.epw')
    b = Building(filepath, wea)

    z1 = Zone.from_json(os.path.join(compas_energyplus.DATA, 'building_parts', 'zone1.json'))
    b.add_zone(z1)

    # w1 = Window.from_json(os.path.join(compas_energyplus.DATA, 'building_parts', 'w1.json'))
    # b.add_window(w1)

    filepath = os.path.join(compas_energyplus.DATA, 'materials', 'material_library_simple.json')
    with open(filepath, 'r') as fp:
        lib = json.load(fp)
    b.add_materials_from_lib(lib)

    filepath = os.path.join(compas_energyplus.DATA, 'constructions', 'construction_library_simple.json')
    with open(filepath, 'r') as fp:
        lib = json.load(fp)
    b.add_constructions_from_lib(lib)


    b.write_idf()
    b.analyze(exe='/Applications/EnergyPlus-9-6-0/energyplus')


    

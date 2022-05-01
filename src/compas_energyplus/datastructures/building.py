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
from compas_energyplus.datastructures.construction import Construction

class Building(object):
    def __init__(self, filepath, weather):
        self.filepath = filepath
        self.weather = weather

        self.name = 'Building'
        self.ep_version = '9.5'
        self.num_timesteps = 6
        self.terrain = 'City'
        self.solar_distribution = 'FullExteriorWithReflections'

        self.zones = {}
        self.windows = {}
        self.materials = {}
        self.masterials_nomass = {}
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
            mat = Material.from_data(lib[mk])
            self.add_material(mat)

    def add_constructions_from_lib(self, lib):
        for ck in lib:
            con = Construction.from_data(lib[ck])
            self.add_construction(con)

    def add_construction(self, construction):
        self.constructions[len(self.constructions)] = construction

    def analyze(self):
        idf = self.filepath
        eplus = 'energyplus'
        out = os.path.join(compas_energyplus.TEMP, 'eplus_output')
        subprocess.call([eplus, '-w', self.weather,'--output-directory', out, idf])

if __name__ == '__main__':
    from compas_energyplus.datastructures import Zone
    from compas_energyplus.datastructures import Window

    data = compas_energyplus.DATA
    for i in range(50): print('')
    filepath = os.path.join(compas_energyplus.TEMP, 'idf_testing.idf')
    wea = os.path.join(data, 'weather_files', 'USA_WA_Seattle-Tacoma.Intl.AP.727930_TMY3.epw')
    b = Building(filepath, wea)

    z1 = Zone.from_json(os.path.join(compas_energyplus.DATA, 'building_parts', 'zone1.json'))
    b.add_zone(z1)

    w1 = Window.from_json(os.path.join(compas_energyplus.DATA, 'building_parts', 'w1.json'))
    b.add_window(w1)

    filepath = os.path.join(compas_energyplus.DATA, 'materials', 'material_library1.json')
    with open(filepath, 'r') as fp:
        lib = json.load(fp)
    b.add_materials_from_lib(lib)

    filepath = os.path.join(compas_energyplus.DATA, 'constructions', 'construction_library1.json')
    with open(filepath, 'r') as fp:
        lib = json.load(fp)
    b.add_constructions_from_lib(lib)


    b.write_idf()
    # b.analyze()


    # per zone ----------------------------
    # building_surface - DONE
    # fenestration_surface - DONE
    # zone_control_thermostat, schedule, thermostat_time, - DONE?
    # zone_hvac_equipment connections, node lists, ideal loads air system
    # outdoor air
    # zone supply air data
    # -------------------------------------


    # simulation control, heat balance, run period, shadow calc, sizing params

    # materials, window_materials

    # constructions

    # schedule type limits, day interval

    # zone list
    # lights
    # people
    # electric equipment
    # zone infiltration

    # outputs
    # daylighting controls
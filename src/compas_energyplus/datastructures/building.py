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

from compas.utilities import geometric_key

from compas_energyplus.read_write import write_idf
from compas_energyplus.read_write import read_mean_zone_temperatures
from compas_energyplus.datastructures.material import Material
from compas_energyplus.datastructures.material import MaterialNoMass
from compas_energyplus.datastructures.material import WindowMaterialGas
from compas_energyplus.datastructures.material import WindowMaterialGlazing
from compas_energyplus.datastructures.construction import Construction
from compas_energyplus.datastructures.zone import Zone
from compas_energyplus.datastructures.window import Window
from compas_energyplus.datastructures.shading import Shading

# TODO: Delete previous results

class Building(object):
    def __init__(self, path, weather):
        self.name = 'Building'
        self.path = path
        self.idf_filepath = os.path.join(path, f'{self.name}.idf')
        self.weather = weather

        self.ep_version = '9.6'
        self.num_timesteps = 1
        self.terrain = 'City'
        self.solar_distribution = 'FullExteriorWithReflections'
        self.zones = {}
        self.windows = {}
        self.materials = {}
        self.constructions = {}
        self.shadings = {}
        self.mean_air_temperatures = {}
        self.construction_key_dict = {}
        self.srf_cpt_dict = {}

    @property
    def data(self):

        zones = {}
        for zk in self.zones:
            zones[zk] = self.zones[zk].data

        windows = {}
        for wk in self.windows:
            windows[wk] = self.windows[wk].data

        materials = {}
        for mk in self.materials:
            materials[mk] = self.materials[mk].data

        constructions = {}
        for ck in self.constructions:
            constructions[ck] = self.constructions[ck].data

        shadings = {}
        for sk in self.shadings:
            shadings[sk] = self.shadings[sk].data


        data = {'idf_filepath' : self.idf_filepath,
                'path'         : self.path,
                'weather': self.weather,
                'name' : self.name,
                'ep_version' : self.ep_version,
                'num_timesteps' : self.num_timesteps,
                'terrain' : self.terrain,
                'solar_distribution' : self.solar_distribution,
                'zones' : zones,
                'windows' : windows,
                'materials' : materials,
                'constructions' : constructions,
                'shadings': shadings,
                'construction_key_dict': self.construction_key_dict, 
                'mean_air_temperatures' : self.mean_air_temperatures,
                }
        return data
    
    @data.setter
    def data(self, data):
        self.filepath              = data.get('filepath') or {}
        self.path                  = data.get('path') or {}
        self.weather               = data.get('weather') or {}
        self.name                  = data.get('name') or {}
        self.ep_version            = data.get('ep_version') or {}
        self.num_timesteps         = data.get('num_timesteps') or {}
        self.terrain               = data.get('terrain') or {}
        self.solar_distribution    = data.get('solar_distribution') or {}
        zones                      = data.get('zones') or {}
        windows                    = data.get('windows') or {}
        materials                  = data.get('materials') or {}
        constructions              = data.get('constructions') or {}
        shadings                   = data.get('shadings') or {}
        self.construction_key_dict = data.get('construction_key_dict') or {}
        self.mean_air_temperatures = data.get('mean_air_temperatures') or {}

        for zk in zones:
            self.zones[zk] = Zone.from_data(zones[zk])

        for wk in windows:
            self.windows[wk] = Window.from_data(windows[wk])

        mat_dict = {'Material': Material,
                    'MaterialNoMass': MaterialNoMass,
                    'WindowMaterialGlazing': WindowMaterialGlazing,
                    'WindowMaterialGas': WindowMaterialGas, 
                    }

        for mk in materials:
            mat = mat_dict[materials[mk]['__type__']]
            self.materials[mk] = mat.from_data(materials[mk])

        for ck in constructions:
            self.constructions[ck] = Construction.from_data(constructions[ck])

        for sk in shadings:
            self.shadings[sk] = Shading.from_data(shadings[sk])

    @classmethod
    def from_json(cls, filepath):
        with open(filepath, 'r') as fp:
            data = json.load(fp)

        path = data['path']
        weather = data['weather']

        building = cls(path, weather)
        building.data = data
        return building

    def to_json(self, filepath):
        with open(filepath, 'w+') as fp:
            json.dump(self.data, fp)

    def write_idf(self):
        write_idf(self)

    def add_zone(self, zone):
        zk =  len(self.zones)
        self.zones[zk] = zone
        mesh = self.zones[zk].surfaces
        for fk in mesh.faces():
            cpt =mesh.face_centroid(fk)
            gk = geometric_key(cpt)
            if gk in self.srf_cpt_dict:
                mesh.face_attribute(fk, 'outside_boundary_condition', 'Adiabatic')
                zk_ = self.srf_cpt_dict[gk]['zone']
                fk_ = self.srf_cpt_dict[g]['surface']
                self.zones[zk_].surfaces.face_attribute(fk_,'outside_boundary_condition', 'Adiabatic')  
                self.zones
            else:
                self.srf_cpt_dict[gk] = {'zone': zk, 'surface': fk}

    def add_window(self, window):
        self.windows[len(self.windows)] = window

    def add_material(self, material):
        self.materials[len(self.materials)] = material

    def add_materials_from_lib(self, lib):

        mat_dict = {'Material': Material,
                    'MaterialNoMass': MaterialNoMass,
                    'WindowMaterialGlazing': WindowMaterialGlazing,
                    'WindowMaterialGas': WindowMaterialGas, 
                    }

        for mk in lib:
            t = lib[mk]['__type__']
            mat = mat_dict[t].from_data(lib[mk])
            self.add_material(mat)

    def add_constructions_from_lib(self, lib):
        for ck in lib:
            con = Construction.from_data(lib[ck])
            self.add_construction(con)

    def add_construction(self, construction):
        ck = len(self.constructions)
        self.constructions[ck] = construction
        self.construction_key_dict[construction.name] = ck

    def add_shading(self, shading):
        self.shadings[len(self.shadings)] = shading

    def analyze(self, exe=None):
        idf = self.idf_filepath
        if not exe:
            exe = 'energyplus'
        out = os.path.join(compas_energyplus.TEMP, 'eplus_output')
        print(exe, '-w', self.weather,'--output-directory', out, idf)
        subprocess.call([exe, '-w', self.weather,'--output-directory', out, idf])

    def load_results(self):
        filepath = os.path.join(self.path, 'eplus_output', 'eplusout.eso')
        temps, times = read_mean_zone_temperatures(self, filepath)
        self.mean_air_temperatures = temps
        self.result_times = times

    def plot_mean_zone_temperatures(self, plot_type='scatter'):
        import plotly.express as px
        from datetime import datetime
        import pandas as pd

        times = [datetime(2022, m, d, h) for h, d, m in self.result_times]
        temps = self.mean_air_temperatures
        data = {}
        counter = 0
        for zk in self.zones:
            # print(zk)
            for i in range(len(times)):
                # print(i)
                # print(i, zk, temps[i])
                data[counter] = {'zone': zk, 
                                 'temp': temps[i][zk],
                                 'time': times[i],
                                 'hour': self.result_times[i][0],
                                 'day': self.result_times[i][1],
                                 'month': self.result_times[i][2],
                        }
                counter += 1

        df = pd.DataFrame.from_dict(data, orient='index')
        
        if plot_type == 'scatter':
            if len(self.zones) > 1:
                color_by = 'zone'
            else:
                color_by = 'temp'
            fig = px.scatter(df, x='time', y='temp', hover_data={"time": "|%B %d, %H, %Y"}, color=color_by, size=None)
        elif plot_type == 'line':
            fig = px.line(df, x='time', y='temp', hover_data={"time": "|%B %d, %H, %Y"}, color='zone')
        fig.update_xaxes(dtick="M1",tickformat="%b", ticklabelmode="period")
        fig.show()


if __name__ == '__main__':

    for i in range(50): print('')

    data = compas_energyplus.DATA
    
    path = os.path.join(compas_energyplus.TEMP)
    wea = os.path.join(data, 'weather_files', 'USA_WA_Seattle-Tacoma.Intl.AP.727930_TMY3.epw')
    # wea = os.path.join(data, 'weather_files', 'USA_CA_San.Francisco.Intl.AP.724940_TMY3.epw')
    b = Building(path, wea)

    z1 = Zone.from_json(os.path.join(compas_energyplus.DATA, 'building_parts', 'zone1.json'))
    b.add_zone(z1)

    # z2 = Zone.from_json(os.path.join(compas_energyplus.DATA, 'building_parts', 'zone2.json'))
    # b.add_zone(z2)

    # z3 = Zone.from_json(os.path.join(compas_energyplus.DATA, 'building_parts', 'zone3.json'))
    # b.add_zone(z3)

    w1 = Window.from_json(os.path.join(compas_energyplus.DATA, 'building_parts', 'w1.json'))
    b.add_window(w1)

    s1 = Shading.from_json(os.path.join(compas_energyplus.DATA, 'building_parts', 'shading1.json'))
    b.add_shading(s1)

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
    for i in range(50): print('')
    # b.analyze()
    b.load_results()
    b.plot_mean_zone_temperatures()

    b.to_json(os.path.join(compas_energyplus.DATA, 'buildings', '1zone_building.json'))

    # b2 = Building.from_json(os.path.join(compas_energyplus.DATA, 'buildings', '1zone_building.json'))
    # print(b2.constructions)
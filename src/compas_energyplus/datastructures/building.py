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
from compas_energyplus.datastructures.material import WindowMaterialGas
from compas_energyplus.datastructures.material import WindowMaterialGlazing
from compas_energyplus.datastructures.construction import Construction
from compas_energyplus.datastructures.zone import Zone
from compas_energyplus.datastructures.window import Window

# TODO: Delete previous results

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
        self.constructions = {}
        self.mean_air_temperatures = []
        self.construction_key_dict = {}

    def to_json(self, filepath):
        with open(filepath, 'w+') as fp:
            json.dump(self.data, fp)

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


        data = {'filepath' : self.filepath,
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
                'construction_key_dict': self.construction_key_dict, 
                'mean_air_temperatures' : self.mean_air_temperatures,
                }
        return data
    
    @data.setter
    def data(self, data):
        self.filepath              = data.get('filepath') or {}
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

    @classmethod
    def from_json(cls, filepath):
        with open(filepath, 'r') as fp:
            data = json.load(fp)

        filepath = data['filepath']
        weather = data['weather']

        building = cls(filepath, weather)
        building.data = data
        return building

    def write_idf(self):
        write_idf(self)

    def add_zone(self, zone):
        self.zones[len(self.zones)] = zone
    
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

    def analyze(self, exe=None):
        idf = self.filepath
        if not exe:
            exe = 'energyplus'
        out = os.path.join(compas_energyplus.TEMP, 'eplus_output')
        print(exe, '-w', self.weather,'--output-directory', out, idf)
        subprocess.call([exe, '-w', self.weather,'--output-directory', out, idf])

    def load_results(self):
        fh = open(os.path.join(compas_energyplus.TEMP, 'eplus_output', 'eplusout.eso'), 'r')
        lines = fh.readlines()
        fh.close()
        temps = []
        times = []
        del lines[:10]
        del lines[-2:]
        for i in range(0, len(lines), 2):
            line1 = lines[i]
            line2 = lines[i + 1]
            _, temp = line2.split(',')
            time = line1.split(',')
            month = int(time[2])
            day = int(time[3])
            hour = int(time[5]) - 1
            temps.append(float(temp))
            times.append([hour, day, month])
        self.mean_air_temperatures = temps
        self.result_times = times

    def plot_mean_average_temperatures(self):
        import plotly.express as px
        from datetime import datetime
        import pandas as pd

        times = [datetime(2022, m, d, h) for h, d, m in self.result_times]
        temps = b.mean_air_temperatures

        # data = {i: {'temp':temps[i], 'time':times[i]} for i in range(len(times))}
        data = {}
        for i in range(len(times)):
            data[i] = {'temp': temps[i],
                       'time': times[i],
                       'hour': self.result_times[i][0],
                       'day': self.result_times[i][1],
                       'month': self.result_times[i][2],
                      }

        df = pd.DataFrame.from_dict(data, orient='index')
        # fig = px.line(x=range(len(temps)), y=temps)
        fig = px.scatter(df, x='time', y='temp', hover_data={"time": "|%B %d, %H, %Y"}, color='temp')
        fig.update_xaxes(dtick="M1",tickformat="%b", ticklabelmode="period")
        fig.show()


if __name__ == '__main__':

    for i in range(50): print('')

    data = compas_energyplus.DATA
    
    filepath = os.path.join(compas_energyplus.TEMP, 'idf_testing.idf')
    # wea = os.path.join(data, 'weather_files', 'USA_WA_Seattle-Tacoma.Intl.AP.727930_TMY3.epw')
    wea = os.path.join(data, 'weather_files', 'USA_CA_San.Francisco.Intl.AP.724940_TMY3.epw')
    b = Building(filepath, wea)

    z1 = Zone.from_json(os.path.join(compas_energyplus.DATA, 'building_parts', 'zone1.json'))
    b.add_zone(z1)

    w1 = Window.from_json(os.path.join(compas_energyplus.DATA, 'building_parts', 'w1.json'))
    b.add_window(w1)

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
    # b.analyze()
    b.load_results()
    b.plot_mean_average_temperatures()

    b.to_json(os.path.join(compas_energyplus.DATA, 'buildings', '1zone_building.json'))

    # b2 = Building.from_json(os.path.join(compas_energyplus.DATA, 'buildings', '1zone_building.json'))
    # print(b2.constructions)
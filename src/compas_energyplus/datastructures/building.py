from __future__ import print_function

__author__ = ["Tomas Mendez Echenagucia"]
__copyright__ = "Copyright 2020, Design Machine Group - University of Washington"
__license__ = "MIT License"
__email__ = "tmendeze@uw.edu"
__version__ = "0.1.0"

import os
import compas_energyplus
import subprocess

#TODO: Volmesh?
#TODO: Assembly?

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

    def write_idf(self):
        fh = open(self.filepath, 'w')
        fh.close()
        self.write_pre()
        self.write_building()
        self.write_zones()

    def write_pre(self):
        fh = open(self.filepath, 'a')
        fh.write('\n') 
        fh.write('Version,\n')
        fh.write(f'  {self.ep_version};{"":<30}!- Version Identifier\n')
        fh.write('\n')
        fh.write('Timestep,\n')
        fh.write(f'  {self.num_timesteps};{"":<30}!- Number of Timesteps per Hour\n')  
        fh.write('\n')           
        fh.close()

    def write_zones(self):
        for zkey in self.zones:
            self.zones[zkey].write_zone()

    def write_building(self):
        fh = open(self.filepath, 'a')
        fh.write('Building,\n')
        fh.write(f'  {self.name},{"":<30}!- Name\n')
        fh.write(f'  0,{"":<30} !- North Axis (deg)\n')
        fh.write(f'  {self.terrain},{"":<30}!- Terrain\n')
        fh.write(f'  ,{"":<30} !- Loads Convergence Tolerance Value (W)\n')
        fh.write(f'  ,{"":<30} !- Temperature Convergence Tolerance Value (deltaC)\n')
        fh.write(f'  {self.solar_distribution},{"":<30}!- Solar Distribution\n')
        fh.write(f'  ,{"":<30} !- Maximum Number of Warmup Days\n')
        fh.write(f'  ;{"":<30} !- Minimum Number of Warmup Days\n')
        fh.write('\n')
        fh.close()

    def analyze(self):
        idf = self.filepath
        eplus = 'energyplus'
        out = os.path.join(compas_energyplus.TEMP, 'eplus_output')
        subprocess.call([eplus, '-w', self.weather,'--output-directory', out, idf])

if __name__ == '__main__':
    from compas_energyplus.datastructures import Zone

    data = compas_energyplus.DATA
    for i in range(50): print('')
    filepath = os.path.join(compas_energyplus.TEMP, 'idf_testing.idf')
    wea = os.path.join(data, 'USA_WA_Seattle-Tacoma.Intl.AP.727930_TMY3.epw')
    b = Building(filepath, wea)
    z1 = Zone('zone_1', filepath)
    b.zones['zone1'] = z1


    b.write_idf()
    b.analyze()
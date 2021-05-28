from __future__ import print_function

__author__ = ["Tomas Mendez Echenagucia"]
__copyright__ = "Copyright 2020, Design Machine Group - University of Washington"
__license__ = "MIT License"
__email__ = "tmendeze@uw.edu"
__version__ = "0.1.0"

import os
import compas_energyplus

class Building(object):
    def __init__(self):
        self.name = 'TomasBuilding'
        self.filepath = None
        self.ep_version = '9.5'
        self.num_timesteps = 6

    def write_idf(self):
        fh = open(self.filepath, 'w')
        fh.close()
        self.write_pre()
        self.write_building()

    def write_pre(self):
        fh = open(self.filepath, 'a')
        fh.write('Version,\n')
        fh.write(f'  {self.ep_version}{"":<20}!- Version Identifier\n')
        fh.write('\n')
        fh.write('Timestep,\n')
        fh.write(f'  {self.num_timesteps}{"":<20}!- Number of Timesteps per Hour\n')  
        fh.write('\n')           
        fh.close()

    def write_building(self):
        fh = open(self.filepath, 'a')
        fh.write('Building,\n')
        fh.write(f'  {self.name}{"":<20}!- Name\n')
        #   0,                                      !- North Axis {deg}
        #   City,                                   !- Terrain
        #   ,                                       !- Loads Convergence Tolerance Value {W}
        #   ,                                       !- Temperature Convergence Tolerance Value {deltaC}
        #   FullExteriorWithReflections,            !- Solar Distribution
        #   ,                                       !- Maximum Number of Warmup Days
        #   ;                                       !- Minimum Number of Warmup Days
        fh.write('\n')
        fh.close()
if __name__ == '__main__':
    for i in range(50): print('')

    b = Building()
    b.filepath = os.path.join(compas_energyplus.TEMP, 'idf_testing.idf')
    b.write_idf()
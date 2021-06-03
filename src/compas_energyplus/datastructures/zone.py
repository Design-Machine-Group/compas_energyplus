from __future__ import print_function

__author__ = ["Tomas Mendez Echenagucia"]
__copyright__ = "Copyright 2020, Design Machine Group - University of Washington"
__license__ = "MIT License"
__email__ = "tmendeze@uw.edu"
__version__ = "0.1.0"

import os

class Zone(object):
    def __init__(self, name, filepath):
        self.name = name
        self.filepath = filepath
    
    def write_zone(self):
        fh = open(self.filepath, 'a')
        fh.write('Zone,\n')
        fh.write(f'  {self.name},{"":<30}!- Name\n')
        fh.write(f'  0,{"":<30} !- Direction of Relative North (deg)\n')
        fh.write(f'  0,{"":<30} !- X Origin (m)\n')
        fh.write(f'  0,{"":<30} !- Y Origin (m)\n')
        fh.write(f'  0,{"":<30} !- Z Origin (m)\n')
        fh.write(f'  ,{"":<30} !- Type\n')
        fh.write(f'  1,{"":<30} !- Multiplier\n')
        fh.write(f'  ,{"":<30} !- Ceiling Height (m)\n')
        fh.write(f'  ,{"":<30} !- Volume (m3)\n')
        fh.write(f'  ,{"":<30} !- Floor Area (m2)\n')
        fh.write(f'  ,{"":<30} !- Zone Inside Convection Algorithm\n')
        fh.write(f'  ,{"":<30} !- Zone Outside Convection Algorithm\n')
        fh.write(f'  Yes;{"":<30} !- Part of Total Floor Area\n')
        fh.write('\n')
        fh.close()
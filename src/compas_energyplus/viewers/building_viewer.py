from __future__ import print_function

import compas_energyplus

__author__ = ["Tomas Mendez Echenagucia"]
__copyright__ = "Copyright 2020, Design Machine Group - University of Washington"
__license__ = "MIT License"
__email__ = "tmendeze@uw.edu"
__version__ = "0.1.0"



class BuildingViewer(object):
    def __init__(self, building):
        self.building = building

    def show(self):
        pass


if __name__ == '__main__':
    import os
    from compas_energyplus.datastructures import Building

    for i in range(50): print('')

    b = Building.from_json(os.path.join(compas_energyplus.DATA, 'buildings', '1zone_building.json'))
    
    v = BuildingViewer(b)
    v.show()

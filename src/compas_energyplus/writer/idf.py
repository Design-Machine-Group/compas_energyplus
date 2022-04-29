from __future__ import print_function

__author__ = ["Tomas Mendez Echenagucia"]
__copyright__ = "Copyright 2020, Design Machine Group - University of Washington"
__license__ = "MIT License"
__email__ = "tmendeze@uw.edu"
__version__ = "0.1.0"


def write_idf(building):
    fh = open(building.filepath, 'w')
    fh.close()
    write_pre(building)
    write_building(building)
    write_zones(building)

def write_pre(building):
    fh = open(building.filepath, 'a')
    fh.write('\n') 
    fh.write('Version,\n')
    fh.write(f'  {building.ep_version};{"":<30}!- Version Identifier\n')
    fh.write('\n')
    fh.write('Timestep,\n')
    fh.write(f'  {building.num_timesteps};{"":<30}!- Number of Timesteps per Hour\n')  
    fh.write('\n')           
    fh.close()

def write_zones(building):
    for zkey in building.zones:
        zone = building.zones[zkey]
        write_zone(building, zone)
        write_zone_surfaces(building, zone)

def write_zone(building, zone):
    fh = open(building.filepath, 'a')
    fh.write('Zone,\n')
    fh.write(f'  {zone.name},{"":<30}!- Name\n')
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

def write_zone_surfaces(building, zone):
    fh = open(building.filepath, 'a')
    for fk in zone.faces():
        write_building_surface(building, zone, fk)
    fh.close()

def write_building_surface(building, zone, fk):
    """
    BuildingSurface:Detailed,
    AdiabaticWall_2432ddde_0,               !- Name
    Wall,                                   !- Surface Type
    Generic Interior Floor,                 !- Construction Name
    1_zonename_80f89f28,                    !- Zone Name
    Adiabatic,                              !- Outside Boundary Condition
    ,                                       !- Outside Boundary Condition Object
    NoSun,                                  !- Sun Exposure
    NoWind,                                 !- Wind Exposure
    ,                                       !- View Factor to Ground
    ,                                       !- Number of Vertices
    0, 2.09095001794528, 3.05,              !- X,Y,Z Vertex 1 {m}
    0, 2.09095001794528, 0,                 !- X,Y,Z Vertex 2 {m}
    4.18190003589056, 2.09095001794528, 0,  !- X,Y,Z Vertex 3 {m}
    4.18190003589056, 2.09095001794528, 3.05; !- X,Y,Z Vertex 4 {m}
    """



def write_building(building):
    fh = open(building.filepath, 'a')
    fh.write('Building,\n')
    fh.write(f'  {building.name},{"":<30}!- Name\n')
    fh.write(f'  0,{"":<30} !- North Axis (deg)\n')
    fh.write(f'  {building.terrain},{"":<30}!- Terrain\n')
    fh.write(f'  ,{"":<30} !- Loads Convergence Tolerance Value (W)\n')
    fh.write(f'  ,{"":<30} !- Temperature Convergence Tolerance Value (deltaC)\n')
    fh.write(f'  {building.solar_distribution},{"":<30}!- Solar Distribution\n')
    fh.write(f'  ,{"":<30} !- Maximum Number of Warmup Days\n')
    fh.write(f'  ;{"":<30} !- Minimum Number of Warmup Days\n')
    fh.write('\n')
    fh.close()


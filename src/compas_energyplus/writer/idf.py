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
    write_windows(building)

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
        write_zone_thermo_schedule(building, zone)

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
    for fk in zone.surfaces.faces():
        write_building_surface(building, zone, fk)
    fh.close()

def write_building_surface(building, zone, fk):

    st = zone.surfaces.face_attribute(fk, 'surface_type')
    ct = zone.surfaces.face_attribute(fk, 'construction')
    ob = zone.surfaces.face_attribute(fk, 'outside_boundary_condition')
    if ob =='Adiabatic':
        se = 'NoSun'
        we = 'NoWind'
    else:
        se = 'SunExposed'
        we = 'WindExposed'


    fh = open(building.filepath, 'a')
    fh.write('\n')
    fh.write('BuildingSurface:Detailed,\n')
    fh.write('{}_{},                    !- Name\n'.format(zone.name, fk))
    fh.write('{},                       !- Surface Type\n'.format(st))
    fh.write('{},                       !- Construction Name\n'.format(ct))
    fh.write('{},                       !- Zone Name\n'.format(zone.name))
    fh.write('{},                       !- Outside Boundary Condition\n'.format(ob))
    fh.write(',                         !- Outside Boundary Condition Object\n')
    fh.write('{},                       !- Sun Exposure\n'.format(se))
    fh.write('{},                       !- Wind Exposure\n'.format(we))
    fh.write(',                         !- View Factor to Ground\n')
    fh.write(',                         !- Number of Vertices\n')

    for vk in zone.surfaces.face_vertices(fk):
        x, y, z = zone.surfaces.vertex_coordinates(vk)
    fh.write('{}, {}, {},               !- X,Y,Z Vertex (m)\n'.format(x, y, z))
    fh.write('\n')
    fh.close()

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

def write_windows(building):
    fh = open(building.filepath, 'a')
    for wk in building.windows:
        win = building.windows[wk]
        con = win.construction
        bsn = win.building_surface

        fh.write('\n')
        fh.write('FenestrationSurface:Detailed,\n')
        fh.write('{},            !- Name\n'.format(win.name))
        fh.write('Window,        !- Surface Type\n')
        fh.write('{},            !- Construction Name\n'.format(con))
        fh.write('{},            !- Building Surface Name\n'.format(bsn))
        fh.write(',              !- Outside Boundary Condition Object\n')
        fh.write(',              !- View Factor to Ground\n')
        fh.write(',              !- Frame and Divider Name\n')
        fh.write(',              !- Multiplier\n')
        fh.write(',              !- Number of Vertices\n')
        for x, y, z in win.nodes:
            fh.write('{}, {}, {}, !- X,Y,Z Vertex (m)\n'.format(x, y, z))
        fh.write('\n')
    fh.write('\n')
    fh.close()

def write_zone_thermo_schedule(building, zone):
    fh = open(building.filepath, 'a')
    fh.write('\n')
    fh.write('ZoneControl:Thermostat,\n')
    fh.write('  {} Thermostat,         !- Name\n'.format(zone.name))
    fh.write('  {},                    !- Zone or ZoneList Name\n'.format(zone.name))
    fh.write('  {} Thermostat Schedule, !- Control Type Schedule Name\n'.format(zone.name))
    fh.write('  ThermostatSetpoint:DualSetpoint,        !- Control 1 Object Type\n')
    fh.write('  Thermostat Setpoint Dual Setpoint 1,    !- Control 1 Name\n')
    fh.write('  ,                                       !- Control 2 Object Type\n')
    fh.write('  ,                                       !- Control 2 Name\n')
    fh.write('  ,                                       !- Control 3 Object Type\n')
    fh.write('  ,                                       !- Control 3 Name\n')
    fh.write('  ,                                       !- Control 4 Object Type\n')
    fh.write('  ,                                       !- Control 4 Name\n')
    fh.write('  0;                                      !- Temperature Difference Between Cutout And Setpoint (deltaC)\n')
    fh.write('\n')
    fh.write('Schedule:Compact,\n')
    fh.write('  {} Thermostat Schedule, !- Name\n'.format(zone.name))
    fh.write('  {} Thermostat Schedule Type Limits, !- Schedule Type Limits Name\n'.format(zone.name))
    fh.write('  Through: 12/31,                         !- Field 1\n')
    fh.write('  For: AllDays,                           !- Field 2\n')
    fh.write('  Until: 24:00,                           !- Field 3\n')
    fh.write('  4;                                      !- Field 4\n')
    fh.write('\n')
    fh.write('ScheduleTypeLimits,\n')
    fh.write('  {} Thermostat Schedule Type Limits, !- Name\n'.format(zone.name))
    fh.write('  0,                                      !- Lower Limit Value (BasedOnField A3)\n')
    fh.write('  4,                                      !- Upper Limit Value (BasedOnField A3)\n')
    fh.write('  DISCRETE;                               !- Numeric Type\n')
    fh.write('\n')
    fh.close()
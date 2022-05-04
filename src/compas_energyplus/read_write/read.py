from __future__ import print_function

__author__ = ["Tomas Mendez Echenagucia"]
__copyright__ = "Copyright 2020, Design Machine Group - University of Washington"
__license__ = "MIT License"
__email__ = "tmendeze@uw.edu"
__version__ = "0.1.0"


def read_mean_zone_temperatures(building, filepath):
    fh = open(filepath, 'r')
    lines = fh.readlines()
    fh.close()
    temps = {}
    times = []
    num_zones = len(building.zones)
    num_intro = 9 + num_zones
    del lines[:num_intro]
    del lines[-2:]
    counter = 0
    for i in range(0, len(lines), num_zones + 1):
        temps[counter] = {}
        line = lines[i]
        time = line.split(',')
        for j in range(num_zones):
            line = lines[i + j + 1]
            _, temp = line.split(',')
            temps[counter][j] = float(temp)
        
        month = int(time[2])
        day = int(time[3])
        hour = int(time[5]) - 1
        times.append([hour, day, month])
        counter += 1
    mean_air_temperatures = temps
    result_times = times
    return mean_air_temperatures, result_times
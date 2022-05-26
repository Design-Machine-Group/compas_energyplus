from __future__ import print_function

__author__ = ["Tomas Mendez Echenagucia"]
__copyright__ = "Copyright 2020, Design Machine Group - University of Washington"
__license__ = "MIT License"
__email__ = "tmendeze@uw.edu"
__version__ = "0.1.0"

import os
import json
from math import sqrt

from compas.geometry import subtract_vectors
from compas.geometry import scale_vector
from compas.geometry import add_vectors
from compas.geometry import normalize_vector
from compas.geometry import distance_point_point

class Window(object):
    def __init__(self):
        self.name = None
        self.nodes = None
        self.building_surface = None
        self.construction = None

    @classmethod
    def from_wall_and_wwr(cls, zone, wall_key, wwr, construction):
        if wwr > .95:
            wwr = .95
        nks = zone.surfaces.face_vertices(wall_key)
        pts = [zone.surfaces.vertex_coordinates(nk) for nk in nks]
        cpt = zone.surfaces.face_centroid(wall_key)
        a = zone.surfaces.face_area(wall_key) * wwr
        lx = distance_point_point(pts[0], pts[1]) - .1
        ly = a / lx
        vx = scale_vector(normalize_vector(subtract_vectors(pts[0], pts[1])), lx / 2.)
        vy = scale_vector(normalize_vector(subtract_vectors(pts[0], pts[-1])), ly / 2.)
        vx_ = scale_vector(normalize_vector(subtract_vectors(pts[0], pts[1])), -lx / 2.)
        vy_ = scale_vector(normalize_vector(subtract_vectors(pts[0], pts[-1])), -ly / 2.)

        p0 = add_vectors(cpt, add_vectors(vx_, vy_))
        p1 = add_vectors(cpt, add_vectors(vx, vy_))
        p2 = add_vectors(cpt, add_vectors(vx, vy))
        p3 = add_vectors(cpt, add_vectors(vx_, vy))

        window = cls()
        window.name = 'win_{}_{}'.format(zone.name, wall_key)
        window.nodes = [p0, p1, p2, p3]
        window.building_surface = '{}_{}'.format(zone.name, wall_key)
        window.construction = construction
        return window


    def to_json(self, filepath):
        with open(filepath, 'w+') as fp:
            json.dump(self.data, fp)

    @property
    def data(self):
        data = {'name'                  : self.name,
                'nodes'                 : self.nodes,
                'building_surface'      : self.building_surface,
                'construction'          : self.construction,
                }
        return data

    @data.setter
    def data(self, data):
        self.name               = data.get('name') or {}
        self.nodes              = data.get('nodes') or {}
        self.building_surface   = data.get('building_surface') or {}
        self.construction       = data.get('construction') or {}

    @classmethod
    def from_data(cls, data):
        window = cls()
        window.data = data
        return window


    @classmethod
    def from_json(cls, filepath):
        with open(filepath, 'r') as fp:
            data = json.load(fp)
        window = cls()
        window.data = data
        return window

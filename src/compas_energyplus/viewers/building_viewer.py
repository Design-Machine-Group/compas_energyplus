from __future__ import print_function



__author__ = ["Tomas Mendez Echenagucia"]
__copyright__ = "Copyright 2020, Design Machine Group - University of Washington"
__license__ = "MIT License"
__email__ = "tmendeze@uw.edu"
__version__ = "0.1.0"

import plotly.graph_objects as go
import plotly.express as px

import compas_energyplus
from compas.datastructures import Mesh

class BuildingViewer(object):
    def __init__(self, building):
        self.building = building
        self.data = []
        self.layout = None

    def make_layout(self):
        name = self.building.name
        title = '{0}'.format(name)
        layout = go.Layout(title=title,
                          scene=dict(aspectmode='data',
                                    xaxis=dict(
                                               gridcolor='rgb(255, 255, 255)',
                                               zerolinecolor='rgb(255, 255, 255)',
                                               showbackground=True,
                                               backgroundcolor='rgb(230, 230,230)'),
                                    yaxis=dict(
                                               gridcolor='rgb(255, 255, 255)',
                                               zerolinecolor='rgb(255, 255, 255)',
                                               showbackground=True,
                                               backgroundcolor='rgb(230, 230,230)'),
                                    zaxis=dict(
                                               gridcolor='rgb(255, 255, 255)',
                                               zerolinecolor='rgb(255, 255, 255)',
                                               showbackground=True,
                                               backgroundcolor='rgb(230, 230,230)')
                                    ),
                          showlegend=True,
                            )
        self.layout = layout

    def show(self):
        self.make_layout()
        self.add_zones()
        self.add_windows()

        fig = go.Figure(data=self.data, layout=self.layout)
        fig.show()

    def add_zones(self):
        for zk in self.building.zones:
                self.add_zone_mesh(zk)

    def add_windows(self):
        for wk in self.building.windows:
            self.add_window_mesh(wk)


    def add_window_mesh(self, key):
        vertices = self.building.windows[key].nodes
        faces = [[0, 1, 2, 3]]
        mesh = Mesh.from_vertices_and_faces(vertices, faces)
        vertices, faces = mesh.to_vertices_and_faces()
        edges = [[mesh.vertex_coordinates(u), mesh.vertex_coordinates(v)] for u,v in mesh.edges()]
        line_marker = dict(color='rgb(0,0,0)', width=1.5)
        lines = []
        x, y, z = [], [],  []
        for u, v in edges:
            x.extend([u[0], v[0], [None]])
            y.extend([u[1], v[1], [None]])
            z.extend([u[2], v[2], [None]])

        wname = self.building.windows[key].name
        lines = [go.Scatter3d(name=f'{wname}',
                              x=x,
                              y=y,
                              z=z,
                              mode='lines',
                              line=line_marker,
                              legendgroup=f'{wname}',
                              )]
        triangles = []
        for face in faces:
            triangles.append(face[:3])
            if len(face) == 4:
                triangles.append([face[2], face[3], face[0]])
        
        i = [v[0] for v in triangles]
        j = [v[1] for v in triangles]
        k = [v[2] for v in triangles]

        x = [v[0] for v in vertices]
        y = [v[1] for v in vertices]
        z = [v[2] for v in vertices]

        color = px.colors.qualitative.G10[0]


        faces = [go.Mesh3d(name='Zone',
                           x=x,
                           y=y,
                           z=z,
                           i=i,
                           j=j,
                           k=k,
                           opacity=.8,
                           colorbar_title='is_rad',
                           colorbar_thickness=10,
                           color=color,
                           hoverinfo='text',
                           legendgroup='Zone',
                           lighting={'ambient':1.}
                        #    showscale=showscale,
                        #    colorscale=colorscale,
                        #    intensity=intensity_,
                        #    intensitymode=intensitymode,
                        #    text=text,
                )]
        self.data.extend(lines)
        self.data.extend(faces)


    def add_zone_mesh(self, key):
        mesh = self.building.zones[key].surfaces
        vertices, faces = mesh.to_vertices_and_faces()
        edges = [[mesh.vertex_coordinates(u), mesh.vertex_coordinates(v)] for u,v in mesh.edges()]
        line_marker = dict(color='rgb(0,0,0)', width=1.5)
        lines = []
        x, y, z = [], [],  []
        for u, v in edges:
            x.extend([u[0], v[0], [None]])
            y.extend([u[1], v[1], [None]])
            z.extend([u[2], v[2], [None]])

        zname = self.building.zones[key].name
        lines = [go.Scatter3d(name=f'{zname}',
                              x=x,
                              y=y,
                              z=z,
                              mode='lines',
                              line=line_marker,
                              legendgroup=f'{zname}',
                              )]
        triangles = []
        for face in faces:
            triangles.append(face[:3])
            if len(face) == 4:
                triangles.append([face[2], face[3], face[0]])
        
        i = [v[0] for v in triangles]
        j = [v[1] for v in triangles]
        k = [v[2] for v in triangles]

        x = [v[0] for v in vertices]
        y = [v[1] for v in vertices]
        z = [v[2] for v in vertices]

        colors = px.colors.qualitative.Pastel2


        faces = [go.Mesh3d(name='Zone',
                           x=x,
                           y=y,
                           z=z,
                           i=i,
                           j=j,
                           k=k,
                           opacity=.8,
                           colorbar_title='is_rad',
                           colorbar_thickness=10,
                           color=colors[int(key)],
                           hoverinfo='text',
                           legendgroup='Zone',
                        #    lighting=None,
                           lighting={'ambient':1.0},
                        #    showscale=showscale,
                        #    colorscale=colorscale,
                        #    intensity=intensity_,
                        #    intensitymode=intensitymode,
                        #    text=text,
                )]
        self.data.extend(lines)
        self.data.extend(faces)


if __name__ == '__main__':
    import os
    from compas_energyplus.datastructures import Building

    for i in range(50): print('')

    b = Building.from_json(os.path.join(compas_energyplus.DATA, 'buildings', '1zone_building.json'))
    
    v = BuildingViewer(b)
    v.show()

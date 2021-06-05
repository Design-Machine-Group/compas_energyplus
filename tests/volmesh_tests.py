import rhinoscriptsyntax as rs
from compas.datastructures import VolMesh
from  compas_rhino import volmesh_from_polysurfaces

for i in range(20): print('')

srfs = rs.ObjectsByLayer('Default')

vmesh = volmesh_from_polysurfaces(VolMesh, srfs)

for c in vmesh.cells():
    print(c)
    faces = vmesh.cell_faces(c)
    for f in faces:
        cpt = vmesh.face_centroid(f)
        rs.AddTextDot(str(f), cpt)

# -*- coding: utf-8 -*-
"""
Created on Wed Sep 24 14:41:11 2014

@author: santiago
"""

def main():
    import numpy as np
    from meshpy.tet import MeshInfo, build
    from meshpy.geometry import \
            generate_surface_of_revolution, EXT_OPEN, \
            GeometryBuilder

    r = 5
    l = -3

    rz = [(0,0), (r,0), (r,l), (0,l)]

    geob = GeometryBuilder()
    geob.add_geometry(*generate_surface_of_revolution(rz,
            radial_subdiv=50, ring_markers=[1,2,3]))

    mesh_info = MeshInfo()
    geob.set(mesh_info)
    
    #mesh = build(mesh_info, max_volume=0.01)
    mesh = build(mesh_info, max_volume=0.5)
    mesh.write_vtk("/home/santiago/cyl.vtk")
#    mesh.write_neu(file("cylinder.neu", "w"), {
#        1: ("minus_z", 1),
#        2: ("outer", 2),
#        3: ("plus_z", 3),
#        })
    print "Meshpy: done"

if __name__ == "__main__":
    main()

import math
import numpy as np
import pyvista as pv
import obj


class Terrain:
    def __init__(self, p_min, terrain=None):
        self.p_min = p_min
        self.terrain = terrain
        
        if self.terrain is None:
            self.terrain = obj.WavefrontOBJ()

    def get_terrain(self):
        return self.terrain

    def add(self, elevation):
        elevation_data = elevation.read(1)
        y_shape, x_shape = elevation_data.shape
        area = x_shape * y_shape
        increment = int(math.sqrt(area) // 128)

        for x in range(0, x_shape - increment, increment):
            for y in range(0, y_shape - increment, increment):
                vertex = elevation.xy(y, x)
                v0 = self.terrain.add_vertex(vertex[0] - self.p_min[0],
                                             max(0, elevation_data[y, x] - self.p_min[2]),
                                             vertex[1] - self.p_min[1])

                vertex = elevation.xy(y, x + increment)
                v1 = self.terrain.add_vertex(vertex[0] - self.p_min[0],
                                             max(0, elevation_data[y, x + increment] - self.p_min[2]),
                                             vertex[1] - self.p_min[1])

                vertex = elevation.xy(y + increment, x + increment)
                v2 = self.terrain.add_vertex(vertex[0] - self.p_min[0],
                                             max(0, elevation_data[y + increment, x + increment] - self.p_min[2]),
                                             vertex[1] - self.p_min[1])

                vertex = elevation.xy(y + increment, x)
                v3 = self.terrain.add_vertex(vertex[0] - self.p_min[0],
                                             max(0, elevation_data[y + increment, x] - self.p_min[2]),
                                             vertex[1] - self.p_min[1])

                # self.terrain.add_face([v0, v1, v2, v3])


def export(terrain, filename='terrain.obj', debug=False):
    points = pv.wrap(np.array(terrain.vertices))
    surface = points.delaunay_2d()
    # surface.flip_normals()
    pl = pv.Plotter()
    pl.add_mesh(surface)
    pl.export_obj(filename)

    if debug:
        pl = pv.Plotter(shape=(1, 2))
        pl.add_mesh(points)
        pl.add_title('Point Cloud of 3D Surface')
        pl.subplot(0, 1)
        pl.add_mesh(surface, color=True, show_edges=True)
        pl.add_title('Reconstructed Surface')
        pl.show()

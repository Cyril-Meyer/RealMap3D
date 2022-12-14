import numpy as np
import pyvista as pv


class WavefrontOBJ:
    def __init__(self, invert_x=0):
        self.vertices = []
        self.faces = []
        self.vertices_dict = {}
        self.invert_x = invert_x
        return

    def add_vertex(self, x, y, z):
        if self.invert_x != 0:
            x = -x + self.invert_x
        v = self.vertices_dict.get((x, y, z))
        if v is None:
            self.vertices.append((x, y, z))
            v = len(self.vertices)
            self.vertices_dict[(x, y, z)] = v
        return v

    def add_vertices(self, vertices):
        for v in vertices:
            assert len(v) == 3
            self.add_vertex(v[0], v[1], v[2])

    def add_face(self, v):
        if len(v) < 3:
            raise NotImplementedError
        if self.invert_x != 0:
            self.faces.append(v[::-1])
        else:
            self.faces.append(v)
        return

    def write(self, filename):
        with open(filename, "w") as out:
            for vertex in self.vertices:
                out.write(f'v {round(vertex[0], 4)} {round(vertex[1], 4)} {round(vertex[2], 4)}\n')
            for face in self.faces:
                if len(face) >= 3:
                    out.write(f'f')
                    for i in range(len(face)):
                        out.write(f' {face[i]}')
                    out.write('\n')
                else:
                    raise NotImplementedError
        return


def export_reconstruction(object, filename='object.obj', debug=False, flip_normals=False):
    points = pv.wrap(np.array(object.vertices))
    surface = points.delaunay_2d()
    if flip_normals:
        surface.flip_normals()
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

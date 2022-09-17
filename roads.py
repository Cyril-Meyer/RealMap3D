import math
import numpy as np
import pyvista as pv
import obj

ROAD_WIDTH = 3.5
ROAD_HEIGHT = 0.5


class Roads:
    def __init__(self, p_min, track=None, terrain=None, terrain_precision=2):
        self.p_min = p_min
        self.track = track
        self.terrain = terrain
        self.ends = RoadsEnds()
        self.terrain_precision = terrain_precision

        if self.track is None:
            self.track = obj.WavefrontOBJ()
        if self.terrain is None:
            self.terrain = obj.WavefrontOBJ()

    def get_track(self):
        return self.track

    def export_track_connections(self, filename):
        self.ends.merge(filename)
        return self.track

    def get_terrain(self):
        return self.terrain

    def add(self, roads):
        for index, poi in roads.iterrows():
            road_coords = roads.loc[index, 'geometry'].coords
            v0, v1, v2, v3 = None, None, None, None
            v0d, v1d, v2d, v3d = None, None, None, None
            for c in range(len(road_coords) - 1):
                v0, v1 = v3, v2
                v0d, v1d = v3d, v2d
                # current point
                p1 = np.array(road_coords[c])
                p1 -= self.p_min
                # next point
                p2 = np.array(road_coords[c + 1])
                p2 -= self.p_min
                # direction
                dir = p2 - p1
                # normalized orthogonal vector to direction
                orthogonal = dir[1], -dir[0]
                orthogonal /= np.linalg.norm(orthogonal)

                # add track vertices
                if v0 is None or v2 is None:
                    v0 = self.track.add_vertex(p1[0] - orthogonal[0] * ROAD_WIDTH,
                                               p1[2] + ROAD_HEIGHT,
                                               p1[1] - orthogonal[1] * ROAD_WIDTH)
                    v1 = self.track.add_vertex(p1[0] + orthogonal[0] * ROAD_WIDTH,
                                               p1[2] + ROAD_HEIGHT,
                                               p1[1] + orthogonal[1] * ROAD_WIDTH)
                    v0d = self.track.add_vertex(p1[0] - orthogonal[0] * ROAD_WIDTH * 2.0,
                                                p1[2] - ROAD_HEIGHT * 3.0,
                                                p1[1] - orthogonal[1] * ROAD_WIDTH * 2.0)
                    v1d = self.track.add_vertex(p1[0] + orthogonal[0] * ROAD_WIDTH * 2.0,
                                                p1[2] - ROAD_HEIGHT * 3.0,
                                                p1[1] + orthogonal[1] * ROAD_WIDTH * 2.0)

                v2 = self.track.add_vertex(p2[0] + orthogonal[0] * ROAD_WIDTH,
                                           p2[2] + ROAD_HEIGHT,
                                           p2[1] + orthogonal[1] * ROAD_WIDTH)
                v3 = self.track.add_vertex(p2[0] - orthogonal[0] * ROAD_WIDTH,
                                           p2[2] + ROAD_HEIGHT,
                                           p2[1] - orthogonal[1] * ROAD_WIDTH)
                v2d = self.track.add_vertex(p2[0] + orthogonal[0] * ROAD_WIDTH * 2.0,
                                            p2[2] - ROAD_HEIGHT * 3.0,
                                            p2[1] + orthogonal[1] * ROAD_WIDTH * 2.0)
                v3d = self.track.add_vertex(p2[0] - orthogonal[0] * ROAD_WIDTH * 2.0,
                                            p2[2] - ROAD_HEIGHT * 3.0,
                                            p2[1] - orthogonal[1] * ROAD_WIDTH * 2.0)

                # track faces
                self.track.add_face([v3, v2, v1, v0])
                # track border faces
                self.track.add_face([v1, v2, v2d, v1d])
                self.track.add_face([v3, v0, v0d, v3d])

                # track segment ends
                if c == 0:
                    # add first part as an end
                    pe1 = [p1[0] - orthogonal[0] * ROAD_WIDTH,
                           p1[2] + ROAD_HEIGHT,
                           p1[1] - orthogonal[1] * ROAD_WIDTH]
                    pe2 = [p1[0] + orthogonal[0] * ROAD_WIDTH,
                           p1[2] + ROAD_HEIGHT,
                           p1[1] + orthogonal[1] * ROAD_WIDTH]
                    self.ends.add_end(p1[0], p1[2], p1[1], [pe1, pe2])
                if c == len(road_coords) - 2:
                    # add last part as an end
                    pe1 = [p2[0] - orthogonal[0] * ROAD_WIDTH,
                           p2[2] + ROAD_HEIGHT,
                           p2[1] - orthogonal[1] * ROAD_WIDTH]
                    pe2 = [p2[0] + orthogonal[0] * ROAD_WIDTH,
                           p2[2] + ROAD_HEIGHT,
                           p2[1] + orthogonal[1] * ROAD_WIDTH]
                    self.ends.add_end(p2[0], p2[2], p2[1], [pe1, pe2])

                # terrain vertices for better fitting
                self.terrain.add_vertex(p1[0] - orthogonal[0] * ROAD_WIDTH,
                                        p1[2] + ROAD_HEIGHT * 0.25,
                                        p1[1] - orthogonal[1] * ROAD_WIDTH)
                self.terrain.add_vertex(p1[0] + orthogonal[0] * ROAD_WIDTH,
                                        p1[2] + ROAD_HEIGHT * 0.25,
                                        p1[1] + orthogonal[1] * ROAD_WIDTH)

                direction = p2 - p1
                direction_norm = np.linalg.norm(direction) / 10
                direction /= direction_norm

                p = p1
                for i in range(1, math.floor(direction_norm), self.terrain_precision):
                    p = p1 + i * direction
                    self.terrain.add_vertex(p[0] + orthogonal[0] * ROAD_WIDTH,
                                            p[2] + ROAD_HEIGHT * 0.5,
                                            p[1] + orthogonal[1] * ROAD_WIDTH)
                    self.terrain.add_vertex(p[0] - orthogonal[0] * ROAD_WIDTH,
                                            p[2] + ROAD_HEIGHT * 0.5,
                                            p[1] - orthogonal[1] * ROAD_WIDTH)

                self.terrain.add_vertex(p2[0] + orthogonal[0] * ROAD_WIDTH,
                                        p2[2] + ROAD_HEIGHT * 0.5,
                                        p2[1] + orthogonal[1] * ROAD_WIDTH)
                self.terrain.add_vertex(p2[0] - orthogonal[0] * ROAD_WIDTH,
                                        p2[2] + ROAD_HEIGHT * 0.5,
                                        p2[1] - orthogonal[1] * ROAD_WIDTH)


class RoadsEnds:
    def __init__(self):
        self.ends = []
        self.ends_dict = {}

    def add_end(self, x, y, z, ends_points):
        v = self.ends_dict.get((x, y, z))
        if v is None:
            self.ends.append([])
            v = len(self.ends)
            self.ends_dict[(x, y, z)] = v

        for end_point in ends_points:
            self.ends[v-1].append(end_point)

    def merge(self, filename):
        pl = pv.Plotter()
        for i in range(len(self.ends)):
            if len(self.ends[i]) > 3:
                points = pv.wrap(np.array(self.ends[i]))
                surface = points.delaunay_2d()
                '''
                if surface.n_faces > 0:
                    surface.flip_normals()
                    pl.add_mesh(surface)
                '''
                pl.add_mesh(surface)
        pl.export_obj(f'{filename}')

import math
import numpy as np
import pyvista as pv
import obj

ROAD_WIDTH = 3.5
ROAD_HEIGHT = 0.5


class Roads:
    def __init__(self, p_min, track=None, terrain=None, terrain_precision=2, invert_x=0):
        self.p_min = p_min
        self.track = track
        self.terrain = terrain
        self.crossings = RoadsCrossings()
        self.terrain_precision = terrain_precision

        if self.track is None:
            self.track = obj.WavefrontOBJ(invert_x=invert_x)
        if self.terrain is None:
            self.terrain = obj.WavefrontOBJ(invert_x=invert_x)

    def get_track(self):
        return self.track

    def export_track(self, filename):
        self.track.write(filename)

    def export_track_connections(self, filename, invert_x=0):
        self.crossings.merge(filename, invert_x)
        return self.track

    def get_terrain(self):
        return self.terrain

    def get_road_points(self, road_coords, c):
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
        return p1, p2, orthogonal

    def add_terrain(self, roads):
        for index, poi in roads.iterrows():
            road_coords = roads.loc[index, 'geometry'].coords
            for c in range(len(road_coords) - 1):
                p1, p2, orthogonal = self.get_road_points(road_coords, c)
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

    def add_roads(self, roads):
        for index, poi in roads.iterrows():
            road_coords = roads.loc[index, 'geometry'].coords
            v0, v1, v2, v3 = None, None, None, None
            v0d, v1d, v2d, v3d = None, None, None, None
            for c in range(len(road_coords) - 1):
                v0, v1 = v3, v2
                v0d, v1d = v3d, v2d
                p1, p2, orthogonal = self.get_road_points(road_coords, c)

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

                # track segment crossings
                if c == 0:
                    # add first part as a crossing
                    pe1 = [p1[0] - orthogonal[0] * ROAD_WIDTH,
                           p1[2] + ROAD_HEIGHT,
                           p1[1] - orthogonal[1] * ROAD_WIDTH]
                    pe2 = [p1[0] + orthogonal[0] * ROAD_WIDTH,
                           p1[2] + ROAD_HEIGHT,
                           p1[1] + orthogonal[1] * ROAD_WIDTH]
                    self.crossings.add_crossing(p1[0], p1[2], p1[1], [pe1, pe2])
                if c == len(road_coords) - 2:
                    # add last part as a crossing
                    pe1 = [p2[0] - orthogonal[0] * ROAD_WIDTH,
                           p2[2] + ROAD_HEIGHT,
                           p2[1] - orthogonal[1] * ROAD_WIDTH]
                    pe2 = [p2[0] + orthogonal[0] * ROAD_WIDTH,
                           p2[2] + ROAD_HEIGHT,
                           p2[1] + orthogonal[1] * ROAD_WIDTH]
                    self.crossings.add_crossing(p2[0], p2[2], p2[1], [pe1, pe2])


class RoadsCrossings:
    def __init__(self):
        self.crossings = []
        self.crossings_dict = {}

    def add_crossing(self, x, y, z, crossings_points):
        x, z, y = math.trunc(x), math.trunc(y), math.trunc(z)
        v = self.crossings_dict.get((x, y))
        if v is None:
            self.crossings.append([])
            v = len(self.crossings)
            self.crossings_dict[(x, y)] = v

        for crossing_point in crossings_points:
            self.crossings[v-1].append(crossing_point)

    def merge(self, filename, invert_x):
        pl = pv.Plotter()
        meshes = pv.PolyData()
        for i in range(len(self.crossings)):
            if len(self.crossings[i]) > 3:
                if invert_x != 0:
                    self.crossings[i] = np.array(self.crossings[i])[:] * [-1, 1, 1] + (invert_x, 0, 0)
                points = pv.wrap(np.array(self.crossings[i]))
                surface = points.delaunay_2d()
                '''
                if surface.n_faces > 0:
                    surface.flip_normals()
                    pl.add_mesh(surface)
                '''
                meshes = meshes.merge(surface)
                # surface.flip_normals()
                # meshes = meshes.merge(surface)
                # pl.add_mesh(surface)
        pl.add_mesh(meshes)
        pl.export_obj(f'{filename}')

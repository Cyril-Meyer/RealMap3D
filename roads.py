import math
import numpy as np
import obj

ROAD_WIDTH = 4.5
ROAD_HEIGHT = 0.5


class Roads:
    def __init__(self, p_min, track=None, terrain=None):
        self.p_min = p_min
        self.track = track
        self.terrain = terrain

        if self.track is None:
            self.track = obj.WavefrontOBJ()
        if self.terrain is None:
            self.terrain = obj.WavefrontOBJ()

    def get_track(self):
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
                for i in range(1, math.floor(direction_norm)):
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

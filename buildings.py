import numpy as np
import obj


class Buildings:
    def __init__(self, p_min, buildings=None, buildings_roofs=None, dual_faces=False):
        self.p_min = p_min
        self.buildings = buildings
        self.buildings_roofs = buildings_roofs
        self.dual_faces = dual_faces

        if self.buildings is None:
            self.buildings = obj.WavefrontOBJ()
        if self.buildings_roofs is None:
            self.buildings_roofs = obj.WavefrontOBJ()

    def get_buildings(self):
        return self.buildings

    def get_buildings_roofs(self):
        return self.buildings_roofs

    def add(self, buildings_gis, buildings_attr_height):
        for index, poi in buildings_gis.iterrows():
            # building height
            building_height = 2
            if buildings_attr_height is not None:
                building_height = buildings_gis.loc[index, f'{buildings_attr_height}']
            building_height = max(building_height, 2)
            # building polygon
            building_coords = buildings_gis.loc[index, 'geometry'].exterior.coords

            building_z = building_coords[0][2] - self.p_min[2]
            # first point
            p0 = building_coords[0]
            # central point of building
            centroid_xy = np.array(buildings_gis.loc[index, 'geometry'].bounds)
            centroid_xy = centroid_xy[0] + (centroid_xy[2] - centroid_xy[0]) / 2, \
                          centroid_xy[1] + (centroid_xy[3] - centroid_xy[1]) / 2
            p_roof = np.array([centroid_xy[0], centroid_xy[1], 0]) - self.p_min

            roof_vertices = self.buildings_roofs.add_vertex(p_roof[0],
                                                             building_z + building_height + (building_height / 5),
                                                             p_roof[1])
            p0 -= self.p_min
            for c in range(0, len(building_coords) - 1):
                # current point
                p1 = np.array(building_coords[c])
                p1 -= self.p_min
                # next point
                p2 = np.array(building_coords[c + 1])
                p2 -= self.p_min

                v0 = self.buildings.add_vertex(p1[0], building_z - 2, p1[1])
                v1 = self.buildings.add_vertex(p2[0], building_z - 2, p2[1])
                v2 = self.buildings.add_vertex(p2[0], building_z + building_height, p2[1])
                v3 = self.buildings.add_vertex(p1[0], building_z + building_height, p1[1])
                if self.dual_faces:
                    self.buildings.add_face([v3, v2, v1, v0])
                self.buildings.add_face([v0, v1, v2, v3])
                v2 = self.buildings_roofs.add_vertex(p2[0], building_z + building_height, p2[1])
                v3 = self.buildings_roofs.add_vertex(p1[0], building_z + building_height, p1[1])
                self.buildings_roofs.add_face([v2, roof_vertices, v3])
                if self.dual_faces:
                    self.buildings_roofs.add_face([v3, roof_vertices, v2])

                # roof = self.buildings_roofs.add_vertex(p2[0], p2[2] + 6, p2[1])
                # roof_vertices.append(roof)

            # connect first and last point
            v0 = self.buildings.add_vertex(p0[0], building_z - 2, p0[1])
            v1 = self.buildings.add_vertex(p2[0], building_z - 2, p2[1])
            v2 = self.buildings.add_vertex(p2[0], building_z + building_height, p2[1])
            v3 = self.buildings.add_vertex(p0[0], building_z + building_height, p0[1])
            if self.dual_faces:
                self.buildings.add_face([v3, v2, v1, v0])
            self.buildings.add_face([v0, v1, v2, v3])

            v0 = self.buildings_roofs.add_vertex(p0[0], building_z + building_height, p0[1])
            v1 = self.buildings_roofs.add_vertex(p2[0], building_z + building_height, p2[1])
            self.buildings_roofs.add_face([v0, roof_vertices, v1])
            if self.dual_faces:
                self.buildings_roofs.add_face([v1, roof_vertices, v0])

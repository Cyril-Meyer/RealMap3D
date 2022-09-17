import random
import numpy as np
import obj

TREE_WIDTH = 0.2
TREE_HEIGHT = 5.0
LEAVE_WIDTH = 1.5


class Tree:
    def __init__(self, p_min, tree_trunks=None, tree_leaves=None, dual_faces=False):
        self.p_min = p_min
        self.tree_trunks = tree_trunks
        self.tree_leaves = tree_leaves
        self.dual_faces = dual_faces

        if self.tree_trunks is None:
            self.tree_trunks = obj.WavefrontOBJ()
        if self.tree_leaves is None:
            self.tree_leaves = obj.WavefrontOBJ()

    def get_trunks(self):
        return self.tree_trunks

    def get_leaves(self):
        return self.tree_leaves

    def add(self, vegetation_gis):
        for index, poi in vegetation_gis.iterrows():
            p = vegetation_gis.loc[index, 'geometry'].coords[0]
            p = p - self.p_min

            # trunk
            v0 = self.tree_trunks.add_vertex(p[0] + TREE_WIDTH, p[2] - TREE_HEIGHT, p[1] + TREE_WIDTH)
            v1 = self.tree_trunks.add_vertex(p[0] + TREE_WIDTH, p[2] - TREE_HEIGHT, p[1] - TREE_WIDTH)
            v2 = self.tree_trunks.add_vertex(p[0] - TREE_WIDTH, p[2] - TREE_HEIGHT, p[1] - TREE_WIDTH)
            v3 = self.tree_trunks.add_vertex(p[0] - TREE_WIDTH, p[2] - TREE_HEIGHT, p[1] + TREE_WIDTH)

            v0_up = self.tree_trunks.add_vertex(p[0] + TREE_WIDTH, p[2] + TREE_HEIGHT, p[1] + TREE_WIDTH)
            v1_up = self.tree_trunks.add_vertex(p[0] + TREE_WIDTH, p[2] + TREE_HEIGHT, p[1] - TREE_WIDTH)
            v2_up = self.tree_trunks.add_vertex(p[0] - TREE_WIDTH, p[2] + TREE_HEIGHT, p[1] - TREE_WIDTH)
            v3_up = self.tree_trunks.add_vertex(p[0] - TREE_WIDTH, p[2] + TREE_HEIGHT, p[1] + TREE_WIDTH)

            self.tree_trunks.add_face([v1, v1_up, v0_up, v0])
            self.tree_trunks.add_face([v2, v2_up, v1_up, v1])
            self.tree_trunks.add_face([v3, v3_up, v2_up, v2])
            self.tree_trunks.add_face([v0, v0_up, v3_up, v3])

            # leaves
            p = p + np.array([0, 0, TREE_HEIGHT])

            # random rotation
            theta = np.radians(random.random() * 90)
            c, s = np.cos(theta), np.sin(theta)
            r = np.array(((c, -s), (s, c)))
            p0 = np.dot([LEAVE_WIDTH, LEAVE_WIDTH], r.T)
            p1 = np.dot([LEAVE_WIDTH, -LEAVE_WIDTH], r.T)
            p2 = np.dot([-LEAVE_WIDTH, -LEAVE_WIDTH], r.T)
            p3 = np.dot([-LEAVE_WIDTH, LEAVE_WIDTH], r.T)

            v0 = self.tree_leaves.add_vertex(p[0] + p0[0], p[2] - LEAVE_WIDTH, p[1] + p0[1])
            v1 = self.tree_leaves.add_vertex(p[0] + p1[0], p[2] - LEAVE_WIDTH, p[1] + p1[1])
            v2 = self.tree_leaves.add_vertex(p[0] + p2[0], p[2] - LEAVE_WIDTH, p[1] + p2[1])
            v3 = self.tree_leaves.add_vertex(p[0] + p3[0], p[2] - LEAVE_WIDTH, p[1] + p3[1])

            v0_up = self.tree_leaves.add_vertex(p[0] + p0[0], p[2] + LEAVE_WIDTH, p[1] + p0[1])
            v1_up = self.tree_leaves.add_vertex(p[0] + p1[0], p[2] + LEAVE_WIDTH, p[1] + p1[1])
            v2_up = self.tree_leaves.add_vertex(p[0] + p2[0], p[2] + LEAVE_WIDTH, p[1] + p2[1])
            v3_up = self.tree_leaves.add_vertex(p[0] + p3[0], p[2] + LEAVE_WIDTH, p[1] + p3[1])

            self.tree_leaves.add_face([v1, v1_up, v0_up, v0])
            self.tree_leaves.add_face([v2, v2_up, v1_up, v1])
            self.tree_leaves.add_face([v3, v3_up, v2_up, v2])
            self.tree_leaves.add_face([v0, v0_up, v3_up, v3])

            self.tree_leaves.add_face([v3, v2, v1, v0])
            self.tree_leaves.add_face([v0_up, v1_up, v2_up, v3_up])

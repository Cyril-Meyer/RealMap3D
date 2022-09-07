class WavefrontOBJ:
    def __init__(self):
        self.vertices = []
        self.faces = []
        self.vertices_dict = {}
        return

    def add_vertex(self, x, y, z):
        v = self.vertices_dict.get((x, y, z))
        if v is None:
            self.vertices.append((x, y, z))
            v = len(self.vertices)
            self.vertices_dict[(x, y, z)] = v
        return v

    def add_face(self, v1, v2, v3, v4):
        self.faces.append((v1, v2, v3, v4))
        return

    def write(self, filename):
        with open(filename, "w") as out:
            for vertex in self.vertices:
                out.write(f'v {round(vertex[0], 4)} {round(vertex[1], 4)} {round(vertex[2], 4)}\n')
            for face in self.faces:
                out.write(f'f {face[0]} {face[1]} {face[2]} {face[3]}\n')
        return

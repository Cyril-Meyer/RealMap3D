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

    def add_face(self, v):
        if len(v) < 3:
            raise NotImplementedError
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

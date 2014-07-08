from pyley.GremlinQuery import GremlinQuery


class GraphObject():
    def __init__(self):
        self.__opts = {}

    def V(self):
        return GremlinQuery('g.V()', dict())

    def M(self):
        return GremlinQuery('g.Morphism()', dict())

    def Vertex(self):
        return self.V()

    def Morphism(self):
        return self.M()
import unittest
from pyley.graph import GraphObject


class GremlinQueryTests(unittest.TestCase):
    def setUp(self):
        self.opts = dict(url='http://localhost:64210/api/v1/query/gremlin')

    def test_vertex_query(self):
        g = GraphObject()
        query = g.Vertex()
        self.assertEqual(query.build(), 'g.V()')
    def test_morphism_query(self):
        g = GraphObject()
        query = g.Morphism()
        self.assertEqual(query.build(), 'g.Morphism()')

if __name__ == '__main__':
    unittest.main()
import unittest
from pyley.graph import GraphObject


class GremlinQueryTests(unittest.TestCase):
    def setUp(self):
        self.opts = dict(url='http://localhost:64210/api/v1/query/gremlin')

    def test_vertex_query(self):
        g = GraphObject()
        query = g.Vertex()
        self.assertEqual(query.build(), "g.V()")

    def test_vertex_query_with_parameters(self):
        g = GraphObject()
        query = g.V("Humphrey Bogart")
        actual = query.build()
        self.assertEqual(actual, "g.V('Humphrey Bogart')")

    def test_morphism_query(self):
        g = GraphObject()
        query = g.Morphism()
        self.assertEqual(query.build(), "g.Morphism()")

    def test_out_query(self):
        g = GraphObject()
        query = g.V().Out('name')
        temp_query = query.build()
        self.assertEqual(temp_query, "g.V().Out('name')")

    def test_all_query(self):
        g = GraphObject()
        query = g.V("Humphrey Bogart").All()
        temp_query = query.build()
        self.assertEqual(temp_query, "g.V('Humphrey Bogart').All()")


if __name__ == '__main__':
    unittest.main()
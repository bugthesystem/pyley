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
        actual = query.build()
        print actual
        self.assertEqual(actual, "g.V().Out('name')")

    def test_all_query(self):
        g = GraphObject()
        query = g.V("Humphrey Bogart").All()
        actual = query.build()
        print actual
        self.assertEqual(actual, "g.V('Humphrey Bogart').All()")

    def test_in_query(self):
        g = GraphObject()
        query = g.V().In("name").All()
        actual = query.build()
        print actual
        self.assertEqual(actual, "g.V().In('name').All()")

    def test_has_query(self):
        g = GraphObject()
        query = g.V().Has("name", "Casablanca").All()
        actual = query.build()
        print actual
        self.assertEqual(actual, "g.V().Has('name','Casablanca').All()")

    def test_complex_query1(self):
        g = GraphObject()
        query = g.V().Has("name", "Casablanca") \
            .Out("/film/film/starring") \
            .Out("/film/performance/actor") \
            .Out("name") \
            .All()
        actual = query.build()
        print actual
        self.assertEqual(actual, "g.V().Has('name','Casablanca')"
                                 ".Out('/film/film/starring')"
                                 ".Out('/film/performance/actor')"
                                 ".Out('name')"
                                 ".All()")

    def test_follow_with_morphism_path_and_typed_query(self):
        g = GraphObject()
        film_to_actor = g.Morphism().Out("/film/film/starring").Out("/film/performance/actor")
        query = g.V().Has("name", "Casablanca").Follow(film_to_actor).Out("name").All()
        actual = query.build()
        print actual
        self.assertEqual(actual, "g.V().Has('name','Casablanca')"
                                 ".Follow("
                                 "g.Morphism().Out('/film/film/starring').Out('/film/performance/actor')"
                                 ").Out('name')"
                                 ".All()")

    def test_follow_with_morphism_path_and_str_query(self):
        g = GraphObject()
        film_to_actor = g.Morphism().Out("/film/film/starring").Out("/film/performance/actor")
        query = g.V().Has("name", "Casablanca").Follow(film_to_actor.build()).Out("name").All()
        actual = query.build()
        print actual
        self.assertEqual(actual, "g.V().Has('name','Casablanca')"
                                 ".Follow("
                                 "g.Morphism().Out('/film/film/starring').Out('/film/performance/actor')"
                                 ").Out('name')"
                                 ".All()")


if __name__ == '__main__':
    unittest.main()
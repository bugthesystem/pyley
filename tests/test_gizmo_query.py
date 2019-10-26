import unittest
from pyley import GraphObject


class GizmoQueryTests(unittest.TestCase):

    def setUp(self):
        self.opts = dict(url='http://localhost:64210/api/v1/query/gizmo')


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
        
        self.assertEqual(actual, "g.V().Out('name')")


    def test_out_query_with_predicate(self):
        g = GraphObject()
        query = g.V().Out(g.Vertex())
        actual = query.build()

        self.assertEqual(actual, "g.V().Out(g.V())")


    def test_out_query_with_predicate_as_dict_and_label(self):
        g = GraphObject()
        query = g.V().Out(['foo', 'bar'], 'qux')
        actual = query.build()

        self.assertEqual(actual, "g.V().Out(['foo', 'bar'], 'qux')")


    def test_out_query_with_predicate_as_none_and_label_as_dict(self):
        g = GraphObject()
        query = g.V().Out(None, ['foo', 'bar'])
        actual = query.build()

        self.assertEqual(actual, "g.V().Out(null, ['foo', 'bar'])")


    def test_in_query(self):
        g = GraphObject()
        query = g.V().In("name").All()
        actual = query.build()
        
        self.assertEqual(actual, "g.V().In('name').All()")


    def test_both(self):
        g = GraphObject()
        query = g.V("F").Both("follows")
        actual = query.build()
        print(actual)
        self.assertEqual(actual, "g.V('F').Both('follows')")


    def test_is(self):
        g = GraphObject()
        query = g.V().Is('B', 'C')
        actual = query.build()

        self.assertEqual(actual, "g.V().Is('B', 'C')")


    def test_tag(self):
        g = GraphObject()
        query = g.V().Tag('B', 'C')
        actual = query.build()

        self.assertEqual(actual, 'g.V().Tag(["B", "C"])')


    def test_save(self):
        g = GraphObject()
        query = g.V().Save('B', 'C')
        actual = query.build()

        self.assertEqual(actual, "g.V().Save('B', 'C')")


    def test_back(self):
        g = GraphObject()
        query = g.V().Back('B')
        actual = query.build()

        self.assertEqual(actual, "g.V().Back('B')")


    def test_all_query(self):
        g = GraphObject()
        query = g.V("Humphrey Bogart").All()
        actual = query.build()
        
        self.assertEqual(actual, "g.V('Humphrey Bogart').All()")


    def test_has_query(self):
        g = GraphObject()
        query = g.V().Has("name", "Casablanca").All()
        actual = query.build()
        
        self.assertEqual(actual, "g.V().Has('name', 'Casablanca').All()")


    def test_complex_query1(self):
        g = GraphObject()
        query = g.V().Has("name", "Casablanca") \
            .Out("/film/film/starring") \
            .Out("/film/performance/actor") \
            .Out("name") \
            .All()
        actual = query.build()
        
        self.assertEqual(actual, "g.V().Has('name', 'Casablanca')"
                                 ".Out('/film/film/starring')"
                                 ".Out('/film/performance/actor')"
                                 ".Out('name')"
                                 ".All()")


    def test_follow_with_morphism_path_and_typed_query(self):
        g = GraphObject()
        film_to_actor = g.Morphism().Out("/film/film/starring").Out("/film/performance/actor")
        query = g.V().Has("name", "Casablanca").Follow(film_to_actor).Out("name").All()
        actual = query.build()
        
        self.assertEqual(actual, "g.V().Has('name', 'Casablanca')"
                                 ".Follow("
                                 "g.Morphism().Out('/film/film/starring').Out('/film/performance/actor')"
                                 ").Out('name')"
                                 ".All()")


    def test_follow_with_morphism_path_and_str_query(self):
        g = GraphObject()
        film_to_actor = g.Morphism().Out("/film/film/starring").Out("/film/performance/actor")
        query = g.V().Has("name", "Casablanca").Follow(film_to_actor.build()).Out("name").All()
        actual = query.build()
        
        self.assertEqual(actual, "g.V().Has('name', 'Casablanca')"
                                 ".Follow("
                                 "g.Morphism().Out('/film/film/starring').Out('/film/performance/actor')"
                                 ").Out('name')"
                                 ".All()")


    def test_follow_with_vertex(self):
        g = GraphObject()

        with self.assertRaises(Exception):
            g.V().Follow(g.V()).build()


    def test_union(self):
        g = GraphObject()

        query = g.Vertex().Union(g.Vertex())
        actual = query.build()

        self.assertEqual(actual, "g.V().Union(g.V())")


    def test_intersect(self):
        g = GraphObject()

        query = g.Vertex().Intersect(g.Vertex())
        actual = query.build()

        self.assertEqual(actual, "g.V().Intersect(g.V())")


    def test_get_limit(self):
        g = GraphObject()
        query = g.Vertex().GetLimit(5)
        actual = query.build()
        
        self.assertEqual(actual, "g.V().GetLimit(5)")


    def test_emit(self):
        g = GraphObject()
        query = g.Emit({'name': 'John', 'lastName': 'DOE', 'age': 25})
        
        self.assertEqual(query, 'g.Emit({"age": 25, "lastName": "DOE", "name": "John"})')


if __name__ == '__main__':
    unittest.main()

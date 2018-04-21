from unittest import TestCase
from pyley import CayleyClient, GraphObject

_CLIENT_URL = 'http://localhost:64210'


class CayleyClientTests(TestCase):
    def test_send(self):
        client = CayleyClient(_CLIENT_URL)
        g = GraphObject()
        query = g.V().Has("name", "Casablanca") \
            .Out("/film/film/starring") \
            .Out("/film/performance/actor") \
            .Out("name") \
            .All()
        response = client.Send(query)

        self.assertTrue(response.r.status_code == 200)
        self.assertTrue(response.r is not None)
        self.assertTrue(len(response.result) > 0)

        query = g.V().HasR("name", "Casablanca") \
            .Out("/film/film/starring") \
            .Out("/film/performance/actor") \
            .Out("name") \
            .All()
        response = client.Send(query)

        self.assertTrue(response.r.status_code == 200)
        self.assertTrue(response.r is not None)
        self.assertTrue(len(response.result) > 0)

    def test_a_add_quad(self):
        client = CayleyClient(_CLIENT_URL)
        response = client.AddQuad('foo', 'to', 'bar')
        self.assertEqual(response.r.status_code, 200)

        g = GraphObject()
        query = g.V("foo").Out('to').Is('bar').All()
        response = client.Send(query)
        self.assertEqual(len(response.result['result']), 1)

    def test_b_delete_quad(self):
        client = CayleyClient(_CLIENT_URL)
        response = client.DeleteQuad('foo', 'to', 'bar')
        self.assertEqual(response.r.status_code, 200)

        g = GraphObject()

        query = g.V("foo").Out('to').Is("bar").All()
        response = client.Send(query)
        self.assertIsNone(response.result['result'])

    def test_c_add_quads(self):
        client = CayleyClient(_CLIENT_URL)
        response = client.AddQuads([
            ('foo', 'to', 'bar'),
            ('baz', 'from', 'quux')
        ])
        self.assertEqual(response.r.status_code, 200)

        g = GraphObject()

        query = g.V("foo").Out('to').Is("bar").Union(
            g.V("baz").Out('from').Is("quux")
        ).All()
        response = client.Send(query)
        self.assertEqual(len(response.result['result']), 2)


    def test_d_delete_quads(self):
        client = CayleyClient(_CLIENT_URL)
        response = client.DeleteQuads([
            ('foo', 'to', 'bar'),
            ('baz', 'from', 'quux')
        ])
        self.assertEqual(response.r.status_code, 200)

        g = GraphObject()

        query = g.V("foo").Out('to').Is("bar").Union(
            g.V("baz").Out('from').Is('quux')
        ).All()
        response = client.Send(query)
        self.assertIsNone(response.result['result'])

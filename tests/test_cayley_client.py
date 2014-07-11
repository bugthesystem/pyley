from unittest import TestCase
from pyley.cayley_client import CayleyClient
from pyley.graph import GraphObject


class CayleyClientTests(TestCase):
    def test_send(self):
        client = CayleyClient()
        g = GraphObject()
        query = g.V().Has("name", "Casablanca") \
            .Out("/film/film/starring") \
            .Out("/film/performance/actor") \
            .Out("name") \
            .All()
        response = client.Send(query)
        self.assertTrue(len(response) > 0)
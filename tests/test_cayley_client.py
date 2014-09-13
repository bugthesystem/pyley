from unittest import TestCase
from pyley import CayleyClient, GraphObject


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

        print response.result

        self.assertTrue(response.r.status_code == 200)
        self.assertTrue(response.r is not None)
        self.assertTrue(len(response.result) > 0)

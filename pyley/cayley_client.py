import requests
from pyley.gremlin_query import GremlinQuery


class CayleyClient:
    def __init__(self, url="http://localhost:64210", version="v1"):
        self.url = "%s/api/%s/query/gremlin" % (url, version)

    def Send(self, query):
        if isinstance(query , str):
            return requests.post(self.url, data=query).json()
        elif isinstance(query , GremlinQuery):
            return requests.post(self.url, data=query.build()).json()
        else:
            raise Exception("Invalid query parameter in Send")
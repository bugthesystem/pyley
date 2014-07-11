import requests
from pyley.gremlin_query import GremlinQuery


class CayleyResponse:
    def __init__(self, raw_response, result):
        self.r = raw_response
        self.result = result


class CayleyClient:
    def __init__(self, url="http://localhost:64210", version="v1"):
        self.url = "%s/api/%s/query/gremlin" % (url, version)

    def Send(self, query):
        if isinstance(query, str):
            r = requests.post(self.url, data=query)
            return CayleyResponse(r, r.json())
        elif isinstance(query, GremlinQuery):
            r = requests.post(self.url, data=query.build())
            return CayleyResponse(r, r.json())
        else:
            raise Exception("Invalid query parameter in Send")
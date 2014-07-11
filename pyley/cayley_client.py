import requests


class CayleyClient:
    def __init__(self, url="http://localhost:64210", version="v1"):
        self.url = "%s/api/%s/query/gremlin" % (url, version)

    def Send(self, query):
        return requests.post(self.url, data=query.build()).json()
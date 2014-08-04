"""
pyley Python client for an open-source graph database Cayley

:copyright: (c) 2014 by Ziya SARIKAYA @ziyasal.
:license: MIT, see LICENSE for more details.

"""
import Queue
import json
import requests

__title__ = 'pyley'
__version__ = '0.1.1-dev'
__author__ = 'Ziya SARIKAYA @ziyasal'
__license__ = 'MIT'
__copyright__ = 'Copyright 2014 Ziya SARIKAYA @ziyasal'

VERSION = tuple(map(int, __version__.split('.')))


class CayleyResponse(object):
    def __init__(self, raw_response, result):
        self.r = raw_response
        self.result = result


class CayleyClient(object):
    def __init__(self, url="http://localhost:64210", version="v1"):
        self.url = "%s/api/%s/query/gremlin" % (url, version)

    def Send(self, query):
        if isinstance(query, str):
            r = requests.post(self.url, data=query)
            return CayleyResponse(r, r.json())
        elif isinstance(query, _GremlinQuery):
            r = requests.post(self.url, data=query.build())
            return CayleyResponse(r, r.json())
        else:
            raise Exception("Invalid query parameter in Send")


class GraphObject(object):
    def __init__(self):
        pass

    def V(self):
        return _GremlinQuery("g.V()")

    def V(self, *node_ids):
        builder = []
        l = len(node_ids)
        for index, node_id in enumerate(node_ids):
            if index == l - 1:
                builder.append(u"'{0:s}'".format(node_id))
            else:
                builder.append(u"'{0:s}',".format(node_id))

        return _GremlinQuery(u"g.V({0:s})".format("".join(builder)))

    def M(self):
        return _GremlinQuery("g.Morphism()")

    def Vertex(self):
        return self.V()

    def Vertex(self, *node_ids):
        if len(node_ids) == 0:
            return self.V()

        return self.V(node_ids)

    def Morphism(self):
        return self.M()

    def Emit(self, data):
        return "g.Emit({0:s})".format(json.dumps(data, default=lambda o: o.__dict__))


class _QueryDefinition(object):
    def __init__(self, token, *parameters):
        self.token = token
        self.parameters = parameters

    def build(self):
        if len(self.parameters) > 0:
            return self.token % self.parameters
        else:
            return self.token


class _GremlinQuery(object):
    def __init__(self, token, *parameters):
        self.queryDeclarations = Queue.Queue()
        q = _QueryDefinition(token, parameters) if len(parameters) > 0 else _QueryDefinition(token)
        self.queryDeclarations.put(q)

    def build(self):
        builder = []
        while not self.queryDeclarations.empty():
            query_def = self.queryDeclarations.get()
            builder.append(query_def.build())

        return "".join(builder)

    def Out(self, label):
        q = _QueryDefinition(".Out('%s')", label)
        self.queryDeclarations.put(q)

        return self

    def All(self):
        q = _QueryDefinition(".All()")
        self.queryDeclarations.put(q)

        return self

    def In(self, label):
        q = _QueryDefinition(".In('%s')", label)
        self.queryDeclarations.put(q)

        return self

    def Has(self, label, val):
        q = _QueryDefinition(".Has('%s','%s')", label, val)
        self.queryDeclarations.put(q)

        return self

    def Follow(self, query):
        if isinstance(query, str):
            q = _QueryDefinition(".Follow(%s)", query)
        elif isinstance(query, _GremlinQuery):
            q = _QueryDefinition(".Follow(%s)", query.build())
        else:
            raise Exception("Invalid parameter in follow query")

        self.queryDeclarations.put(q)

        return self

    def GetLimit(self, val):
        q = _QueryDefinition(".GetLimit(%d)", val)
        self.queryDeclarations.put(q)

        return self

    def Both(self, val):
        q = _QueryDefinition(".Both('%s')", val)
        self.queryDeclarations.put(q)

        return self
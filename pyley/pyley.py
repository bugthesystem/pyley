import json
import requests

class CayleyResponse(object):

    def __init__(self, raw_response, result):
        self.r = raw_response
        self.result = result


class CayleyClient(object):

    def __init__(self, url="http://localhost:64210", version="v1"):
        self.url = "%s/api/%s/query/gizmo" % (url, version)
        self.write_url = "%s/api/%s/write" % (url, version)
        self.delete_url = "%s/api/%s/delete" % (url, version)


    def add_query_limit(self, limit):
        if isinstance(limit, int):
            self.url = self.url + '?limit=' + str(limit)
        else:
            raise Exception("Invalid parameter for adding query limit, should be integer.")


    def Send(self, query):
        if isinstance(query, str):
            r = requests.post(self.url, data=query.encode('utf-8'))
            return CayleyResponse(r, r.json())
        elif isinstance(query, _GizmoQuery):
            r = requests.post(self.url, data=str(query).encode('utf-8'))
            return CayleyResponse(r, r.json())
        else:
            raise Exception("Invalid query parameter in Send")


    def AddQuad(self, subject, predicate, object_, label=None):
        return self.AddQuads([(subject, predicate, object_, label)])


    def AddQuads(self, quads):
        quads = [
            {
                "subject": q[0],
                "predicate": q[1],
                "object": q[2],
                "label": None if len(q) < 4 else q[3]
            }
            for q in quads
        ]
        r = requests.post(self.write_url, json=quads)
        return CayleyResponse(r, r.json())


    def DeleteQuad(self, subject, predicate, object_, label=None):
        return self.DeleteQuads([(subject, predicate, object_, label)])
        

    def DeleteQuads(self, quads):
        quads = [
            {
                "subject": q[0],
                "predicate": q[1],
                "object": q[2],
                "label": None if len(q) < 4 else q[3]
            }
            for q in quads
        ]
        r = requests.post(self.delete_url, json=quads)
        return CayleyResponse(r, r.json())


class _GizmoQuery(object):
    queryDeclarations = None

    def __init__(self):
        self.queryDeclarations = []


    def __str__(self):
        return ".".join([str(d) for d in self.queryDeclarations])


    def _put(self, token, *parameters):
        q = _QueryDefinition(token, *parameters)
        self.queryDeclarations.append(q)


class GraphObject(object):
    def V(self):
        return _Vertex("g.V()")


    def V(self, *node_ids):
        builder = []
        l = len(node_ids)
        for index, node_id in enumerate(node_ids):
            if index == l - 1:
                builder.append(u"'{0:s}'".format(node_id))
            else:
                builder.append(u"'{0:s}',".format(node_id))

        return _Vertex(u"g.V({0:s})".format("".join(builder)))


    def M(self):
        return _Morphism("g.Morphism()")


    def Vertex(self):
        return self.V()
    

    def Vertex(self, *node_ids):
        if len(node_ids) == 0:
            return self.V()
        return self.V(*node_ids)


    def Morphism(self):
        return self.M()


    def Emit(self, data):
        return "g.Emit({0:s})".format(json.dumps(data, default=lambda o: o.__dict__, sort_keys=True))


class _Path(_GizmoQuery):

    def __init__(self, parent):
        _GizmoQuery.__init__(self)
        self._put(parent)


    def Out(self, predicate=None, tags=None):
        self._bounds("Out", predicate, tags)
        return self


    def In(self, predicate=None, tags=None):
        self._bounds("In", predicate, tags)
        return self


    def Both(self, predicate=None, tags=None):
        self._bounds("Both", predicate, tags)
        return self


    def _bounds(self, method, predicate=None, tags=None):
        if predicate is None and tags is None:
            self._put("%s()", method)
        elif tags is None:
            self._put("%s(%s)", method, self._format_input_bounds(predicate))
        else:
            self._put(
                "%s(%s, %s)",
                method,
                self._format_input_bounds(predicate),
                self._format_input_bounds(tags)
            )
        return self


    def _format_input_bounds(self, value):
        if type(value) is dict:
            return json.dumps(value)

        if type(value) is str:
            return "'%s'" % value

        if value is None:
            return 'null'

        return value


    def Is(self, *nodes):
        self._put("Is('%s')", "', '".join(nodes))
        return self


    def Has(self, predicate, object):
        self._put("Has('%s', '%s')", predicate, object)
        return self


    def HasR(self, predicate, object):
        self._put("Has('%s', '%s')", object, predicate)
        return self


    def Tag(self, *tags):
        self._put("Tag(%s)", json.dumps(tags))

        return self

    def Back(self, tag):
        self._put("Back('%s')", tag)
        return self


    def Save(self, predicate, tag):
        self._put("Save('%s', '%s')", predicate, tag)
        return self


    def Intersect(self, query):
        if not isinstance(query, _Vertex) and type(query) is not str:
            raise Exception("Invalid parameter in intersect query")

        self._put("Intersect(%s)", query)
        return self


    def Union(self, query):
        if not isinstance(query, _Vertex) and type(query) is not str:
            raise Exception("Invalid parameter in union query")

        self._put("Union(%s)", query)
        return self


    def Follow(self, query):
        if not isinstance(query, _Morphism) and type(query) is not str:
            raise Exception("Invalid parameter in follow query")

        self._put("Follow(%s)", query)
        return self


    def FollowR(self, query):
        if not isinstance(query, _Morphism) and type(query) is not str:
            raise Exception("Invalid parameter in followr query")

        self._put("FollowR(%s)", query)
        return self


    def build(self):
        return str(self)


class _Vertex(_Path):

    def All(self):
        self._put("All()")
        return self


    def GetLimit(self, limit):
        self._put("GetLimit(%d)", limit)
        return self


class _Morphism(_Path):
    pass


class _QueryDefinition(object):

    def __init__(self, token, *parameters):
        self.token = token
        self.parameters = parameters


    def __str__(self):
        if len(self.parameters) > 0:
            return str(self.token) % self.parameters
        else:
            return str(self.token)

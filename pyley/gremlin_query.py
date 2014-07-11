import Queue


class _QueryDefinition:
    def __init__(self, token, *parameters):
        self.token = token
        self.parameters = parameters

    def build(self):
        if len(self.parameters) > 0:
            return self.token % self.parameters
        else:
            return self.token


class GremlinQuery:
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
        elif isinstance(query, GremlinQuery):
            q = _QueryDefinition(".Follow(%s)", query.build())
        else:
            raise Exception("Invalid query parameter")

        self.queryDeclarations.put(q)
        
        return self

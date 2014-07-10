import Queue


class _QueryDefinition:
    def __init__(self, token, parameters=dict(), has_parameter=False):
        self.token = token
        self.parameters = parameters
        self.has_parameter = has_parameter

    def build(self):
        if self.has_parameter:
            return self.token % self.parameters
        else:
            return self.token


class GremlinQuery:
    def __init__(self, token, parameters=dict()):
        self.queryDeclarations = Queue.Queue()
        q = _QueryDefinition(token, parameters)
        self.queryDeclarations.put(q)

    def build(self):
        query = ''
        while not self.queryDeclarations.empty():
            q_def = self.queryDeclarations.get()
            query += q_def.build()
        return query

    def Out(self, label):
        q = _QueryDefinition(".Out('%s')", label, True)
        self.queryDeclarations.put(q)
        return self

    def All(self):
        q = _QueryDefinition(".All()", True)
        self.queryDeclarations.put(q)
        return self
class MiddlewareBase:
    def process(self, ctx):
        raise NotImplementedError

class MiddlewarePipeline:
    def __init__(self):
        self.middlewares = []

    def add(self, middleware: MiddlewareBase):
        self.middlewares.append(middleware)

    def __iter__(self):
        return iter(self.middlewares)

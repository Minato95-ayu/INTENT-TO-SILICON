class HttpContext:
    def __init__(self, request, response):
        self.request = request
        self.response = response
        self.state = {} # For passing data between middlewares

class ConnectionPool:
    def __init__(self, size=5):
        self.size = size
        self.pool = []

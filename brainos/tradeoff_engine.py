class TradeoffEngine:
    """
    Scores the recommended architecture against cost, scale, and performance.
    """
    def evaluate(self, architecture: str) -> dict:
        if architecture == "Event-Sourced Actor Model":
            return {"security": 9, "performance": 9, "scalability": 10, "cost": 4}
        elif architecture == "Microservices with Distributed Transactions":
            return {"security": 8, "performance": 7, "scalability": 9, "cost": 6}
        elif architecture == "Edge-Cached Serverless Monolith":
            return {"security": 7, "performance": 10, "scalability": 10, "cost": 8}
        else:
            return {"security": 7, "performance": 8, "scalability": 7, "cost": 9}

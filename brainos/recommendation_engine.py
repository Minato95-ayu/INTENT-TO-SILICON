class RecommendationEngine:
    """
    Recommends software architectures based on constraints.
    """
    def recommend(self, constraints: list[str]) -> str:
        if "ACID Compliance" in constraints and "High Throughput" in constraints:
            return "Event-Sourced Actor Model"
        elif "ACID Compliance" in constraints:
            return "Microservices with Distributed Transactions"
        elif "High Read Throughput" in constraints:
            return "Edge-Cached Serverless Monolith"
        else:
            return "Modular Monolith"

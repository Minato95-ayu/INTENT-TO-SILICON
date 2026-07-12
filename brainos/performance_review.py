class PerformanceReview:
    """
    Reviews the generated logical architecture for performance bottlenecks.
    """
    def review(self, constraints: list[str], architecture: str) -> dict:
        issues = []
        optimizations = []
        
        if "High Read Throughput" in constraints and "Edge-Cached" not in architecture:
            issues.append("High Read Throughput constraint detected but architecture lacks Edge Caching.")
            optimizations.append("Added Redis Cache Layer")
            
        if "High Throughput" in constraints and "Event-Sourced" not in architecture:
            issues.append("Write throughput may bottleneck on traditional RDBMS.")
            optimizations.append("Added Kafka Event Bus")
            
        score = 100 - (len(issues) * 15)
        return {
            "score": max(score, 0),
            "findings": issues,
            "auto_remediations": optimizations
        }

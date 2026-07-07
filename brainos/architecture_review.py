from security_review import SecurityReview
from performance_review import PerformanceReview

class ArchitectureReview:
    """
    Aggregates all reviews to provide a final Architecture Score.
    """
    def generate_report(self, constraints: list[str], architecture: str, entities: dict) -> dict:
        sr = SecurityReview().review(entities)
        pr = PerformanceReview().review(constraints, architecture)
        
        overall_score = (sr["score"] + pr["score"]) // 2
        
        return {
            "overall_score": overall_score,
            "security": sr,
            "performance": pr
        }

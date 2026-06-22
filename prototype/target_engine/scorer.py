import json

# Scoring Matrices for different tiers
FRONTEND_WEIGHTS = {
    "React": {"ui": 50, "realtime": 20, "analytics": 10},
    "Flutter": {"mobile": 80, "ui": 40},
    "Vue": {"ui": 40, "analytics": 10},
    "Angular": {"ui": 30, "enterprise": 40},
    "HTML/CSS/JS": {"ui": 20}
}

BACKEND_WEIGHTS = {
    "FastAPI": {"api": 50, "ai": 80, "realtime": 30, "database": 20},
    "NestJS": {"api": 40, "workflow": 30, "database": 20},
    "Spring": {"api": 30, "enterprise": 80, "workflow": 50, "rbac": 40},
    "Go": {"api": 50, "realtime": 50, "blockchain": 20},
    "Rust": {"api": 30, "blockchain": 80, "realtime": 50}
}

DATABASE_WEIGHTS = {
    "PostgreSQL": {"database": 50, "enterprise": 60, "analytics": 40, "workflow": 20},
    "SQLite": {"database": 40, "mobile": 30},
    "MySQL": {"database": 40, "enterprise": 30}
}

SPECIAL_WEIGHTS = {
    "Jupyter": {"ai": 80, "analytics": 60},
    "Solidity": {"blockchain": 100},
    "Kotlin": {"mobile": 50},
    "Swift": {"mobile": 50}
}

class TargetScorer:
    def __init__(self, ir_data: dict):
        self.ir = ir_data
        self.features = ir_data.get("features", [])

    def compute_scores(self, weights_dict) -> dict:
        scores = {tech: 0 for tech in weights_dict.keys()}
        for feature in self.features:
            for tech, weight_map in weights_dict.items():
                if feature in weight_map:
                    scores[tech] += weight_map[feature]
        return scores

    def get_best(self, scores: dict):
        if not scores:
            return None, 0
            
        sorted_scores = sorted(scores.items(), key=lambda x: x[1], reverse=True)
        best_tech, best_score = sorted_scores[0]
        
        if best_score == 0:
            return None, 0
            
        # Confidence math: best / (best + second)
        confidence = 100
        if len(sorted_scores) > 1:
            second_score = sorted_scores[1][1]
            if second_score > 0:
                confidence = (best_score / (best_score + second_score)) * 100
                
        return best_tech, round(confidence)

    def select_target(self) -> dict:
        f_scores = self.compute_scores(FRONTEND_WEIGHTS)
        b_scores = self.compute_scores(BACKEND_WEIGHTS)
        d_scores = self.compute_scores(DATABASE_WEIGHTS)
        s_scores = self.compute_scores(SPECIAL_WEIGHTS)

        best_frontend, f_conf = self.get_best(f_scores)
        best_backend, b_conf = self.get_best(b_scores)
        best_db, d_conf = self.get_best(d_scores)
        
        # Calculate overall confidence
        confidences = [c for c in [f_conf, b_conf, d_conf] if c > 0]
        overall_confidence = sum(confidences) / len(confidences) if confidences else 0

        # Extract special targets that scored > 0
        specials = [tech for tech, score in s_scores.items() if score > 0]

        return {
            "target_plan_version": "1.0",
            "confidence": round(overall_confidence),
            "stack": {
                "frontend": best_frontend or "HTML/CSS/JS",
                "backend": best_backend or "FastAPI",
                "database": best_db or "SQLite",
                "special": specials
            },
            "generators": [
                f"{best_frontend.lower()}-generator" if best_frontend else "html-generator",
                f"{best_backend.lower()}-generator" if best_backend else "fastapi-generator",
                f"{best_db.lower()}-generator" if best_db else "sqlite-generator"
            ]
        }

def select_target(ir_data: dict) -> str:
    scorer = TargetScorer(ir_data)
    plan = scorer.select_target()
    return json.dumps(plan, indent=2)

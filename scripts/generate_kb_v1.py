"""
=============================================================================
FILE: generate_kb_v1.py
PURPOSE: Knowledge base v1 generation
=============================================================================
This file is part of the AAYU (Aayu) Intent-to-Silicon Programming Language.
The AAYU language enables developers to write code using natural language
intentions, which are compiled to optimized backend code.

For beginners: This file handles knowledge base v1 generation.
To understand the project architecture, see the ARCHITECTURE_FREEZE.md file.
=============================================================================
"""

﻿import os
import json
import random

kb_version = 'v1'
base_dir = rf'd:\intent-to-silicon-research\INTENT-TO-SILICON\prototype\intent_engine\knowledge\{kb_version}'
domains_dir = os.path.join(base_dir, 'domains')
core_dir = os.path.join(base_dir, 'core')

os.makedirs(domains_dir, exist_ok=True)
os.makedirs(core_dir, exist_ok=True)

# List of 20 domains
domain_names = [
    "education", "healthcare", "finance", "ecommerce", "government", 
    "travel", "social", "ai", "devops", "security", "cloud", "mobile", 
    "desktop", "blockchain", "gaming", "media", "analytics", "iot", "enterprise"
]

# A unified template that has all 26+ mandatory sections requested by the user
def generate_domain_blueprint(d_name):
    capitalized = d_name.capitalize()
    return {
        "domain": capitalized,
        "version": "1.0",
        "entities": [f"{capitalized}User", f"{capitalized}Record", f"{capitalized}Transaction"],
        "fields": {
            f"{capitalized}User": ["id: UUID", "name: String", "email: String", "created_at: DateTime"],
            f"{capitalized}Record": ["id: UUID", "user_id: UUID", "status: Enum"]
        },
        "relationships": [
            {"source": f"{capitalized}User", "target": f"{capitalized}Record", "type": "one_to_many"}
        ],
        "actions": ["Create", "Read", "Update", "Delete", "Archive"],
        "constraints": [
            {"entity": f"{capitalized}User", "field": "email", "rule": "must be unique and valid format"}
        ],
        "workflows": [
            f"User Onboarding -> Record Creation -> Processing"
        ],
        "database_design": {
            "primary": "PostgreSQL for ACID compliance",
            "search": "Elasticsearch for fast querying",
            "ledger": "EventStore if strict audit required"
        },
        "api_design": {
            "style": "REST by default, GraphQL if complex UI data requirements exist",
            "versioning": "URI versioning (e.g., /api/v1/...)"
        },
        "architecture_patterns": ["Modular Monolith (Starter)", "Microservices (Enterprise)"],
        "authentication": ["JWT", "OAuth2", "2FA for sensitive actions"],
        "authorization": ["RBAC (Role-Based Access Control)", "ABAC (Attribute-Based Access Control)"],
        "validation_rules": [
            "Input sanitization on all text fields",
            "Strict type checking at API boundaries"
        ],
        "security_rules": [
            "Encrypt PII at rest",
            "Rate limiting on all public endpoints"
        ],
        "performance_rules": [
            "Database indexing on frequently queried foreign keys",
            "Pagination for all collection endpoints (limit=50)"
        ],
        "caching_rules": [
            {"strategy": "Cache-Aside", "ttl": "15m", "targets": ["Public Data", "Read-Heavy Records"]}
        ],
        "deployment_rules": [
            "Containerized via Docker",
            "Stateless application servers"
        ],
        "testing_rules": [
            "Unit tests for domain logic (>80% coverage)",
            "Integration tests for API endpoints"
        ],
        "monitoring_rules": [
            "Prometheus metrics for endpoint latency",
            "Alerting on 5xx error spikes > 1%"
        ],
        "logging_rules": [
            "Structured JSON logging",
            "Never log PII or credentials"
        ],
        "error_handling": [
            "Standardized API error responses (RFC 7807)",
            "Global exception catching middleware"
        ],
        "clarification_rules": {
            "missing_modules": [
                {"trigger": f"No admin panel mentioned for {capitalized}", "question": f"Do you need a back-office Admin Panel to manage {capitalized}Records?"},
                {"trigger": "No auth mentioned", "question": "Should I implement standard email/password authentication or SSO?"}
            ]
        },
        "decision_rules": [
            {
                "condition": "users > 1000000 OR strict isolation required",
                "recommendation": "Microservices"
            },
            {
                "condition": "users <= 1000000",
                "recommendation": "Modular Monolith"
            },
            {
                "condition": "Payment handling required",
                "recommendation": "Suggest Audit Logs, Suggest Retry Mechanism, Suggest Idempotency Keys"
            }
        ],
        "architecture_recommendations": {
            "starter": {"database": "SQLite/Postgres", "cache": "None", "deployment": "Single Server"},
            "production": {"database": "Postgres (HA)", "cache": "Redis", "deployment": "Kubernetes/ECS"}
        },
        "multi_level_templates": {
            "starter": ["Basic CRUD", "SQLite", "Single Service"],
            "professional": ["Authentication", "Dashboard", "Reports", "Postgres"],
            "enterprise": ["Microservices", "Audit Logs", "Analytics", "Redis Cache", "RabbitMQ"],
            "production": ["Monitoring (Prometheus)", "CI/CD", "Auto-scaling", "Multi-AZ Deployment"]
        },
        "best_practices": [
            "Keep controllers thin and domain models fat",
            "Always use environment variables for configuration"
        ],
        "anti_patterns": [
            "God objects/classes",
            "N+1 query problems in ORM",
            "Hardcoding credentials"
        ],
        "code_templates": [
            "Repository Pattern Interface",
            "Service Layer implementation"
        ],
        "sample_projects": [
            f"Simple {capitalized} Manager",
            f"Enterprise {capitalized} Suite"
        ]
    }

# Generate generic blueprints for the 19 domains
for domain in domain_names:
    data = generate_domain_blueprint(domain)
    with open(os.path.join(domains_dir, f'{domain}.json'), 'w') as f:
        json.dump(data, f, indent=2)

# Generate a heavily customized/detailed one for E-Commerce to show depth
ecommerce_data = generate_domain_blueprint("ecommerce")
ecommerce_data["entities"] = ["Customer", "Product", "Order", "Payment", "Inventory", "Cart", "Review", "Shipping"]
ecommerce_data["clarification_rules"]["missing_modules"] = [
    {"trigger": "E-commerce requested without payment gateway", "question": "I see you're building an E-commerce system but didn't mention payments. Should I integrate Stripe or PayPal?"},
    {"trigger": "E-commerce requested without inventory tracking", "question": "Should I add an Inventory module to prevent overselling products?"},
    {"trigger": "E-commerce requested without admin panel", "question": "Do you need a back-office Dashboard to manage Orders, Products, and Customers?"}
]
ecommerce_data["decision_rules"].append({
    "condition": "Global reach required",
    "recommendation": "Suggest CDN for product images and Edge Caching for catalog."
})
ecommerce_data["multi_level_templates"]["enterprise"].extend(["Elasticsearch for Product Search", "Kafka for Order Events"])
with open(os.path.join(domains_dir, 'ecommerce.json'), 'w') as f:
    json.dump(ecommerce_data, f, indent=2)

# Generate a heavily customized one for Finance to show depth
finance_data = generate_domain_blueprint("finance")
finance_data["entities"] = ["Account", "Transaction", "Customer", "Ledger", "Loan", "Card", "AuditLog"]
finance_data["security_rules"].extend(["PCI-DSS Compliance", "End-to-End Encryption for account numbers", "Strict KYC validation"])
finance_data["clarification_rules"]["missing_modules"] = [
    {"trigger": "Finance app without KYC", "question": "Finance apps typically require KYC (Know Your Customer). Should I scaffold a KYC verification module?"},
    {"trigger": "Finance app without audit logs", "question": "Financial regulations require strict auditing. Should I automatically log all state changes to an immutable Ledger?"}
]
finance_data["decision_rules"].append({
    "condition": "Handling transactions",
    "recommendation": "Use Double-Entry Bookkeeping Ledger Pattern and Event Sourcing."
})
with open(os.path.join(domains_dir, 'finance.json'), 'w') as f:
    json.dump(finance_data, f, indent=2)


print("Knowledge Base v1 Generation Complete!")

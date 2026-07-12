"""
=============================================================================
FILE: generate_kb_quality.py
PURPOSE: Generates quality metrics KB
=============================================================================
This file is part of the AAYU (Aayu) Intent-to-Silicon Programming Language.
The AAYU language enables developers to write code using natural language
intentions, which are compiled to optimized backend code.

For beginners: This file handles generates quality metrics kb.
To understand the project architecture, see the ARCHITECTURE_FREEZE.md file.
=============================================================================
"""

﻿import os
import json

base_dir = r'd:\intent-to-silicon-research\INTENT-TO-SILICON\prototype\intent_engine\knowledge'

# Core Synonyms (Real, not procedural)
synonyms = {
    "student": ["learner", "pupil", "candidate", "scholar", "undergraduate", "graduate", "trainee"],
    "customer": ["client", "buyer", "consumer", "purchaser", "shopper", "patron", "subscriber"],
    "employee": ["staff", "worker", "personnel", "team_member", "associate", "colleague"],
    "manager": ["supervisor", "lead", "director", "head", "administrator", "boss"],
    "department": ["division", "unit", "branch", "section", "wing", "office"],
    "order": ["purchase", "booking", "reservation", "request"],
    "payment": ["transaction", "remittance", "transfer", "checkout"],
    "invoice": ["bill", "receipt", "statement", "check"],
    "doctor": ["physician", "surgeon", "specialist", "practitioner", "medic", "clinician"],
    "patient": ["sufferer", "case", "inpatient", "outpatient", "subject", "victim"],
    "teacher": ["instructor", "professor", "educator", "tutor", "lecturer", "coach", "mentor"],
    "school": ["college", "university", "academy", "institute"],
    "hospital": ["clinic", "healthcare", "medical_center", "dispensary"],
    "bank": ["financial_institution", "credit_union"]
}

verbs = {
    "create": ["make", "build", "generate", "spawn", "initiate", "establish", "setup", "add", "insert", "new", "register", "open"],
    "read": ["get", "fetch", "retrieve", "find", "search", "list", "show", "view", "display", "query", "select"],
    "update": ["edit", "modify", "change", "alter", "adjust", "patch", "revise", "amend", "fix"],
    "delete": ["remove", "destroy", "drop", "erase", "trash", "clear", "terminate", "cancel", "kill", "close"],
    "approve": ["accept", "authorize", "validate", "verify", "confirm", "endorse", "certify", "pass"],
    "reject": ["deny", "refuse", "decline", "veto", "discard", "block", "ban", "revoke"]
}

with open(os.path.join(base_dir, 'core', 'synonyms.json'), 'w') as f:
    json.dump(synonyms, f, indent=2)

with open(os.path.join(base_dir, 'core', 'verbs.json'), 'w') as f:
    json.dump(verbs, f, indent=2)

# High Quality Domains
hospital_domain = {
    "name": "Hospital",
    "entities": [
        "Patient", "Doctor", "Nurse", "Department", "Appointment", 
        "Prescription", "MedicalRecord", "LabTest", "Bill"
    ],
    "fields": {
        "Patient": ["id: UUID", "name: Text", "age: Number", "blood_type: Text", "address: Text"],
        "Doctor": ["id: UUID", "name: Text", "specialty: Text", "department_id: UUID"],
        "Appointment": ["id: UUID", "patient_id: UUID", "doctor_id: UUID", "scheduled_time: DateTime", "status: Enum"]
    },
    "relationships": [
        {"source": "Patient", "target": "Appointment", "type": "one_to_many"},
        {"source": "Doctor", "target": "Appointment", "type": "one_to_many"},
        {"source": "Department", "target": "Doctor", "type": "one_to_many"}
    ],
    "actions": [
        "Register Patient",
        "Book Appointment",
        "Admit Patient",
        "Discharge Patient",
        "Generate Bill"
    ],
    "constraints": [
        {"entity": "Patient", "field": "age", "rule": ">= 0"},
        {"entity": "Appointment", "field": "scheduled_time", "rule": "required"},
        {"entity": "Appointment", "field": "doctor_id", "rule": "must_exist_in(Doctor)"}
    ],
    "workflows": [
        "Patient Registration -> Book Appointment -> Consultation -> Billing"
    ],
    "api_templates": {
        "Appointment": ["POST /appointments", "GET /appointments/:id", "PUT /appointments/:id/cancel"]
    },
    "database_schema": "Relational (PostgreSQL preferred for strict ACID transactions in healthcare)",
    "architecture_pattern": "Microservices (Patient Service, Appointment Service, Billing Service)",
    "validation_rules": [
        "Cannot book an appointment in the past.",
        "Doctor cannot have overlapping appointments."
    ],
    "clarification_rules": [
        {"trigger": "appointment exists but doctor missing", "question": "Do you want me to create a Doctor entity first to handle this appointment?"},
        {"trigger": "billing without services", "question": "Do you want to track individual medical services and map them to the Bill?"}
    ]
}

banking_domain = {
    "name": "Banking",
    "entities": [
        "Account", "Customer", "Transaction", "Branch", "Loan", 
        "Card", "CreditScore"
    ],
    "fields": {
        "Account": ["account_number: Text", "balance: Number", "customer_id: UUID", "type: Enum"],
        "Customer": ["id: UUID", "name: Text", "ssn: Text", "kyc_status: Boolean"],
        "Transaction": ["id: UUID", "account_id: UUID", "amount: Number", "type: Enum", "timestamp: DateTime"]
    },
    "relationships": [
        {"source": "Customer", "target": "Account", "type": "one_to_many"},
        {"source": "Account", "target": "Transaction", "type": "one_to_many"},
        {"source": "Account", "target": "Card", "type": "one_to_many"}
    ],
    "actions": [
        "Open Account",
        "Transfer Funds",
        "Process Loan",
        "Issue Card"
    ],
    "constraints": [
        {"entity": "Transaction", "field": "amount", "rule": "> 0"},
        {"entity": "Customer", "field": "ssn", "rule": "unique_and_encrypted"},
        {"entity": "Account", "field": "balance", "rule": ">= 0 for Savings"}
    ],
    "workflows": [
        "KYC Verification -> Open Account -> Issue Card"
    ],
    "api_templates": {
        "Transaction": ["POST /transactions/transfer", "GET /accounts/:id/statement"]
    },
    "database_schema": "Event Sourcing or strict Relational",
    "architecture_pattern": "CQRS (Command Query Responsibility Segregation) for ledger tracking.",
    "validation_rules": [
        "Withdrawal amount cannot exceed account balance.",
        "Transfer requires valid source and destination accounts."
    ],
    "clarification_rules": [
        {"trigger": "account without customer", "question": "An Account needs an owner. Should I create a Customer entity?"}
    ]
}

ecommerce_domain = {
    "name": "E-commerce",
    "entities": [
        "Customer", "Product", "Order", "Cart", "Payment", 
        "Category", "Inventory", "Shipping"
    ],
    "fields": {
        "Product": ["id: UUID", "name: Text", "price: Number", "stock: Number", "category_id: UUID"],
        "Order": ["id: UUID", "customer_id: UUID", "total_amount: Number", "status: Enum"],
        "Payment": ["id: UUID", "order_id: UUID", "amount: Number", "method: Enum", "status: Enum"]
    },
    "relationships": [
        {"source": "Customer", "target": "Order", "type": "one_to_many"},
        {"source": "Order", "target": "Product", "type": "many_to_many"},
        {"source": "Order", "target": "Payment", "type": "one_to_one"}
    ],
    "actions": [
        "Add to Cart",
        "Place Order",
        "Process Payment",
        "Update Inventory"
    ],
    "constraints": [
        {"entity": "Product", "field": "price", "rule": "> 0"},
        {"entity": "Product", "field": "stock", "rule": ">= 0"},
        {"entity": "Order", "field": "total_amount", "rule": "== sum(product_prices)"}
    ],
    "workflows": [
        "Add to Cart -> Checkout -> Payment -> Shipping"
    ],
    "api_templates": {
        "Order": ["POST /orders", "GET /orders/:id", "PUT /orders/:id/status"]
    },
    "database_schema": "Relational (Orders/Payments) + NoSQL (Product Catalog)",
    "architecture_pattern": "Event-Driven Microservices",
    "validation_rules": [
        "Cannot place order if cart is empty.",
        "Cannot process payment if order is already paid."
    ],
    "clarification_rules": [
        {"trigger": "order without payment", "question": "How should orders be paid? Should I add a Payment entity and integration?"}
    ]
}

with open(os.path.join(base_dir, 'domains', 'hospital.json'), 'w') as f:
    json.dump(hospital_domain, f, indent=2)

with open(os.path.join(base_dir, 'domains', 'banking.json'), 'w') as f:
    json.dump(banking_domain, f, indent=2)

with open(os.path.join(base_dir, 'domains', 'ecommerce.json'), 'w') as f:
    json.dump(ecommerce_domain, f, indent=2)

print("High-Quality Domain Generation Complete!")

"""
=============================================================================
FILE: generate_kb.py
PURPOSE: Generates knowledge base for intent system
=============================================================================
This file is part of the AAYU (Aayu) Intent-to-Silicon Programming Language.
The AAYU language enables developers to write code using natural language
intentions, which are compiled to optimized backend code.

For beginners: This file handles generates knowledge base for intent system.
To understand the project architecture, see the ARCHITECTURE_FREEZE.md file.
=============================================================================
"""

﻿"""
=============================================================================
FILE: generate_kb.py
PURPOSE: Auto-generate a Knowledge Base (KB) for AAYU Intent System
=============================================================================
This script creates the core knowledge base that the AAYU language uses to
understand user intents. It generates:
- Synonym mappings (e.g., "student" = "learner" = "pupil")
- Verb actions (CRUD operations: create, read, update, delete)
- Domain entities (Hospital, Banking, E-commerce, etc.)
- Relationships between entities
- Common workflows in each domain

Why? When someone writes AAYU code, the compiler needs to understand what
they mean. This KB maps natural language to structured data.
=============================================================================
"""

import os
import json

# =========================================================================
# STEP 1: Create directory structure for the Knowledge Base
# =========================================================================
base_dir = r'd:\intent-to-silicon-research\INTENT-TO-SILICON\prototype\intent_engine\knowledge'
dirs = ['core', 'domains', 'patterns', 'templates']

for d in dirs:
    os.makedirs(os.path.join(base_dir, d), exist_ok=True)

# CORE
synonyms = {
    "student": ["learner", "pupil", "candidate", "scholar", "undergraduate", "graduate", "trainee"],
    "customer": ["client", "buyer", "consumer", "purchaser", "shopper", "patron", "subscriber"],
    "product": ["item", "goods", "merchandise", "commodity", "article", "offering"],
    "order": ["purchase", "booking", "reservation", "request", "requisition"],
    "payment": ["transaction", "remittance", "transfer", "settlement", "checkout"],
    "employee": ["staff", "worker", "personnel", "team_member", "associate", "colleague"],
    "account": ["profile", "user", "login", "credentials", "membership"],
    "manager": ["supervisor", "lead", "director", "head", "administrator", "boss"],
    "department": ["division", "unit", "branch", "section", "wing", "office"],
    "report": ["document", "summary", "analysis", "statement", "record", "log"],
    "doctor": ["physician", "surgeon", "specialist", "practitioner", "medic", "clinician"],
    "patient": ["sufferer", "case", "inpatient", "outpatient", "subject", "victim"],
    "teacher": ["instructor", "professor", "educator", "tutor", "lecturer", "coach", "mentor"]
}

verbs = {
    "create": ["make", "build", "generate", "spawn", "initiate", "establish", "setup", "add", "insert", "new", "register"],
    "read": ["get", "fetch", "retrieve", "find", "search", "list", "show", "view", "display", "query", "select"],
    "update": ["edit", "modify", "change", "alter", "adjust", "patch", "revise", "amend", "fix"],
    "delete": ["remove", "destroy", "drop", "erase", "trash", "clear", "terminate", "cancel", "kill"],
    "approve": ["accept", "authorize", "validate", "verify", "confirm", "endorse", "certify", "pass"],
    "reject": ["deny", "refuse", "decline", "veto", "discard", "block", "ban", "revoke"]
}

with open(os.path.join(base_dir, 'core', 'synonyms.json'), 'w') as f:
    json.dump(synonyms, f, indent=2)

with open(os.path.join(base_dir, 'core', 'verbs.json'), 'w') as f:
    json.dump(verbs, f, indent=2)


# DOMAINS
domains = {
    "hospital": {
        "entities": ["Patient", "Doctor", "Appointment", "MedicalRecord", "Department", "Bill", "Prescription", "Room", "Nurse", "Staff", "Ward", "Treatment", "Diagnosis", "Medicine", "LabTest", "Invoice", "Bed"],
        "relationships": [
            {"source": "Patient", "target": "Appointment", "type": "one_to_many"},
            {"source": "Doctor", "target": "Appointment", "type": "one_to_many"},
            {"source": "Patient", "target": "MedicalRecord", "type": "one_to_one"},
            {"source": "Doctor", "target": "Department", "type": "many_to_one"}
        ],
        "workflows": ["Patient Admission", "Doctor Consultation", "Lab Result Processing", "Discharge and Billing"]
    },
    "banking": {
        "entities": ["Account", "Customer", "Transaction", "Branch", "Loan", "Card", "Transfer", "Statement", "Employee", "Deposit", "Withdrawal", "Beneficiary", "CreditScore"],
        "relationships": [
            {"source": "Customer", "target": "Account", "type": "one_to_many"},
            {"source": "Account", "target": "Transaction", "type": "one_to_many"},
            {"source": "Account", "target": "Card", "type": "one_to_many"}
        ],
        "workflows": ["Account Opening", "Fund Transfer", "Loan Approval", "Card Issuance"]
    },
    "ecommerce": {
        "entities": ["Customer", "Product", "Order", "Cart", "Payment", "Review", "Category", "Inventory", "Shipping", "Seller", "Coupon", "Wishlist", "Invoice", "Address"],
        "relationships": [
            {"source": "Customer", "target": "Order", "type": "one_to_many"},
            {"source": "Order", "target": "Product", "type": "many_to_many"},
            {"source": "Order", "target": "Payment", "type": "one_to_one"}
        ],
        "workflows": ["Checkout Process", "Inventory Update", "Order Fulfillment", "Refund Processing"]
    },
    "education": {
        "entities": ["Student", "Teacher", "Course", "Enrollment", "Grade", "Assignment", "Exam", "Attendance", "Department", "Classroom", "Schedule", "Syllabus", "Result", "Fee"],
        "relationships": [
            {"source": "Student", "target": "Enrollment", "type": "one_to_many"},
            {"source": "Enrollment", "target": "Course", "type": "many_to_one"},
            {"source": "Teacher", "target": "Course", "type": "one_to_many"}
        ],
        "workflows": ["Student Registration", "Course Enrollment", "Grading System", "Attendance Tracking"]
    },
    "crm": {
        "entities": ["Lead", "Contact", "Account", "Opportunity", "Activity", "Campaign", "Case", "Task", "Note", "Event", "Pipeline", "Quote", "Contract", "User"],
        "relationships": [
            {"source": "Account", "target": "Contact", "type": "one_to_many"},
            {"source": "Lead", "target": "Opportunity", "type": "one_to_one"}
        ],
        "workflows": ["Lead Conversion", "Opportunity Management", "Customer Support Ticketing"]
    },
    "erp": {
        "entities": ["Employee", "Department", "Asset", "Vendor", "PurchaseOrder", "Invoice", "Project", "Task", "Timesheet", "Budget", "Tax", "Ledger", "Inventory", "Warehouse"],
        "relationships": [
            {"source": "Department", "target": "Employee", "type": "one_to_many"},
            {"source": "Vendor", "target": "PurchaseOrder", "type": "one_to_many"}
        ],
        "workflows": ["Procurement", "Asset Allocation", "Financial Auditing", "Project Management"]
    }
}

for d_name, d_data in domains.items():
    with open(os.path.join(base_dir, 'domains', f'{d_name}.json'), 'w') as f:
        json.dump(d_data, f, indent=2)

# PATTERNS
patterns = {
    "mvc": {
        "name": "Model-View-Controller",
        "description": "Separates an application into three interconnected components.",
        "components": ["Model", "View", "Controller"]
    },
    "microservices": {
        "name": "Microservices Architecture",
        "description": "Arranges an application as a collection of loosely coupled services.",
        "components": ["API Gateway", "Service Registry", "Independent Services", "Event Bus"]
    },
    "event_driven": {
        "name": "Event-Driven Architecture",
        "description": "Promotes the production, detection, consumption of, and reaction to events.",
        "components": ["Event Producer", "Event Broker", "Event Consumer"]
    }
}

for p_name, p_data in patterns.items():
    with open(os.path.join(base_dir, 'patterns', f'{p_name}.json'), 'w') as f:
        json.dump(p_data, f, indent=2)

# TEMPLATES
templates = {
    "rest_api": {
        "name": "REST API Skeleton",
        "routes": ["GET /", "POST /", "PUT /:id", "DELETE /:id"],
        "middlewares": ["Auth", "Logger", "ErrorHandler"]
    },
    "auth": {
        "name": "JWT Authentication",
        "features": ["Login", "Register", "Password Reset", "Token Refresh", "Role Based Access"]
    }
}

for t_name, t_data in templates.items():
    with open(os.path.join(base_dir, 'templates', f'{t_name}.json'), 'w') as f:
        json.dump(t_data, f, indent=2)


print("Knowledge Base Generation Complete!")

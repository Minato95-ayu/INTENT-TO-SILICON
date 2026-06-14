import json
import os

base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
filepath = os.path.join(base_dir, 'dictionary', 'clarification_library.json')

with open(filepath, 'r') as f:
    data = json.load(f)

data["pharmacy"] = {
    "required_concepts": ["medication_inventory", "prescription"],
    "questions": {
        "medication_inventory": {
            "question": "Medicine inventory manual hogi ya supplier ERP se linked?",
            "type": "implementation",
            "priority": "critical"
        },
        "prescription": {
            "question": "Digital prescription upload accept karenge ya sirf doctor generated?",
            "type": "implementation",
            "priority": "critical"
        },
        "payments": {
            "question": "Online payments chahiye ya sirf pay-at-counter?",
            "type": "feature",
            "priority": "optional"
        }
    }
}

data["housing"] = {
    "required_concepts": ["room_allocation", "student"],
    "questions": {
        "room_allocation": {
            "question": "Room allocation manual hoga ya automated rules pe?",
            "type": "implementation",
            "priority": "critical"
        },
        "maintenance": {
            "question": "Maintenance complaints in-app track karni hain?",
            "type": "feature",
            "priority": "optional"
        }
    }
}

data["employment"] = {
    "required_concepts": ["job_listing", "application"],
    "questions": {
        "job_listing": {
            "question": "Jobs admin post karega ya employers direct aayenge?",
            "type": "implementation",
            "priority": "critical"
        },
        "interviews": {
            "question": "Interview scheduling in-app karni hai?",
            "type": "feature",
            "priority": "optional"
        }
    }
}

data["library"] = {
    "required_concepts": ["book_catalog", "borrow_record"],
    "questions": {
        "book_catalog": {
            "question": "Library catalog external API se fetch hoga?",
            "type": "implementation",
            "priority": "critical"
        },
        "digital_content": {
            "question": "E-books aur PDFs bhi host karne hain?",
            "type": "feature",
            "priority": "optional"
        }
    }
}

data["marketplace"] = {
    "required_concepts": ["product", "seller", "buyer", "order"],
    "questions": {
        "seller": {
            "question": "Sellers ka KYC verification process kaisa hoga?",
            "type": "implementation",
            "priority": "critical"
        },
        "logistics": {
            "question": "Shipping seller handle karega ya platform?",
            "type": "implementation",
            "priority": "critical"
        },
        "subscriptions": {
            "question": "Buyers ke liye premium subscription model chahiye?",
            "type": "feature",
            "priority": "optional"
        }
    }
}

with open(filepath, 'w') as f:
    json.dump(data, f, indent=2)

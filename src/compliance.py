import random

REQUIRED_PPE = ["helmet", "vest", "gloves", "safety_shoes"]

def simulate_ppe_detection():
    return {
        "helmet": random.choice([True, True, False]),
        "vest": random.choice([True, True, False]),
        "gloves": random.choice([True, False]),
        "safety_shoes": random.choice([True, True, False]),
    }

def evaluate_compliance(ppe_status):
    missing = [item for item, present in ppe_status.items() if not present]
    is_compliant = len(missing) == 0

    return {
        "is_compliant": is_compliant,
        "missing_items": missing
    }
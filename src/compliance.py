import random

REQUIRED_PPE = ["helmet", "vest", "gloves", "safety_shoes"]

# Global store for simulated tracking states
_MOCK_STATE = {}

def simulate_ppe_detection(track_id=None):
    if track_id is not None and track_id in _MOCK_STATE:
        return _MOCK_STATE[track_id]
        
    status = {
        "helmet": random.choice([True, True, False]),
        "vest": random.choice([True, True, False]),
        "gloves": random.choice([True, False]),
        "safety_shoes": random.choice([True, True, False]),
    }
    
    if track_id is not None:
        _MOCK_STATE[track_id] = status
        
    return status

def evaluate_compliance(ppe_status):
    missing = [item for item, present in ppe_status.items() if not present]
    is_compliant = len(missing) == 0

    return {
        "is_compliant": is_compliant,
        "missing_items": missing
    }
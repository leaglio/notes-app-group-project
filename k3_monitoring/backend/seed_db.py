import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from database import SessionLocal, Violation, Base, engine
import datetime

def seed():
    # Recreate tables
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    
    db = SessionLocal()
    
    # Add some mock violations
    violations = [
        Violation(worker_id="W-102", ppe_type="Helmet", status="Missing", timestamp=datetime.datetime.now() - datetime.timedelta(minutes=15)),
        Violation(worker_id="W-085", ppe_type="Safety Vest", status="Incorrect", timestamp=datetime.datetime.now() - datetime.timedelta(minutes=45)),
        Violation(worker_id="W-201", ppe_type="Gloves", status="Missing", timestamp=datetime.datetime.now() - datetime.timedelta(hours=2)),
    ]
    
    db.add_all(violations)
    db.commit()
    print("Database seeded with mock violations.")
    db.close()

if __name__ == "__main__":
    seed()

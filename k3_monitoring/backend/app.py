from fastapi import FastAPI, UploadFile, File, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from database import SessionLocal, Violation
import cv2
import numpy as np
from ultralytics import YOLO
import datetime
import os

from roboflow import Roboflow

app = FastAPI(title="K3 PPE Compliance API")

# Enable CORS for frontend integration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- ROBOFLOW CONFIGURATION ---
ROBOFLOW_API_KEY = "X4eE2Z0S8rIQ6Nw4vt0M"
try:
    rf = Roboflow(api_key=ROBOFLOW_API_KEY)
    project = rf.workspace().project("k3-vc0ir-qajd3")
    model = project.version(1).model
except Exception as e:
    print(f"Error loading Roboflow model: {e}")
    model = None

# Dependency to get DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/")
async def root():
    return {"message": "K3 PPE Monitoring API with Roboflow is running"}

@app.get("/stats")
async def get_stats():
    db = SessionLocal()
    total_violations = db.query(Violation).count()
    logs = db.query(Violation).order_by(Violation.timestamp.desc()).limit(10).all()
    
    return {
        "total_violations": total_violations,
        "compliance_rate": 88.5,
        "active_workers": 12,
        "recent_logs": [
            {
                "id": v.id,
                "timestamp": v.timestamp.strftime("%H:%M %p"),
                "worker_id": v.worker_id,
                "ppe_type": v.ppe_type,
                "status": v.status
            } for v in logs
        ]
    }

@app.post("/detect")
async def detect_ppe(file: UploadFile = File(...)):
    if not model:
        return {"status": "error", "message": "Roboflow model not loaded"}

    # Save temp file for Roboflow inference
    temp_path = "temp_detect.jpg"
    with open(temp_path, "wb") as f:
        f.write(await file.read())

    try:
        # Perform Inference
        prediction_response = model.predict(temp_path, confidence=40, overlap=30).json()
        predictions = prediction_response.get("predictions", [])
        
        print(f"DEBUG: Received frame. Detected: {[p['class'] for p in predictions]}")

        # --- K3 COMPLIANCE LOGIC ---
        db = SessionLocal()
        found_classes = [p["class"].lower() for p in predictions]
        violations_detected = []
        
        # 1. Cek Helm
        if "helm" not in found_classes:
            new_v = Violation(worker_id="W-Auto", ppe_type="Helmet", status="Missing")
            db.add(new_v)
            violations_detected.append("No Helmet")
            
        # 2. Cek Vest
        if "vest" not in found_classes:
            new_v = Violation(worker_id="W-Auto", ppe_type="Safety Vest", status="Missing")
            db.add(new_v)
            violations_detected.append("No Vest")

        # 3. Cek Mask (Opsional, tergantung kebijakan perusahaan)
        if "mask" not in found_classes:
            new_v = Violation(worker_id="W-Auto", ppe_type="Mask", status="Missing")
            db.add(new_v)
            violations_detected.append("No Mask")

        db.commit()

        return {
            "status": "success", 
            "detections": predictions,
            "violations": violations_detected,
            "summary": f"Detected: {', '.join(found_classes) if found_classes else 'None'}"
        }
    except Exception as e:
        print(f"Prediction Error: {e}")
        return {"status": "error", "message": str(e)}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

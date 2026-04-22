from ultralytics import YOLO

class WorkerDetector:
    def __init__(self, model_path="yolov8n.pt", confidence=0.4):
        self.model = YOLO(model_path)
        self.confidence = confidence

    def detect_workers(self, frame):
        results = self.model(frame, verbose=False)
        detections = []

        for result in results:
            if result.boxes is None:
                continue

            for box in result.boxes:
                cls_id = int(box.cls[0].item())
                conf = float(box.conf[0].item())

                # COCO class 0 = person
                if cls_id == 0 and conf >= self.confidence:
                    x1, y1, x2, y2 = box.xyxy[0].tolist()
                    detections.append({
                        "label": "person",
                        "confidence": round(conf, 2),
                        "bbox": [int(x1), int(y1), int(x2), int(y2)]
                    })

        return detections
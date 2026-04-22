import cv2
import math
import time
from ultralytics import YOLO
from src.compliance import simulate_ppe_detection, evaluate_compliance
from src.logger import log_event

class RealTimeDetector:
    def __init__(self, model_path="yolov8n.pt"):
        # Load YOLOv8 model (using standard n version for fast person detection)
        self.model = YOLO(model_path)
        
    def process_frame(self, frame):
        # Run YOLOv8 tracking, specifically for class 0 (person)
        results = self.model.track(
            frame, 
            persist=True, 
            classes=[0], 
            tracker="bytetrack.yaml", 
            verbose=False
        )
        
        overall_results = []
        
        # Create a single overlay layer for all transparency effects to maintain high performance
        overlay = frame.copy()
        h, w = frame.shape[:2]
        
        if results and results[0].boxes is not None and results[0].boxes.id is not None:
            boxes = results[0].boxes.xyxy.cpu().numpy()
            track_ids = results[0].boxes.id.int().cpu().numpy()
            confidences = results[0].boxes.conf.cpu().numpy()
            
            for box, track_id, conf in zip(boxes, track_ids, confidences):
                x1, y1, x2, y2 = map(int, box)
                
                # Get or create mock PPE status for this track_id
                ppe_status = simulate_ppe_detection(track_id=int(track_id))
                compliance = evaluate_compliance(ppe_status)
                
                confidence_pct = round(float(conf) * 100, 1)
                is_compliant = compliance["is_compliant"]
                
                status_str = "SECURED" if is_compliant else "BREACH"
                log_event(status_str, compliance["missing_items"], confidence_pct)
                
                overall_results.append({
                    "track_id": track_id,
                    "ppe": ppe_status,
                    "compliance": compliance,
                    "confidence": confidence_pct,
                    "status": status_str
                })
                
                # --- CYBER-TECH VISUALIZATION ---
                # Neon Cyan for Compliant, Neon Pink/Red for Violation (BGR format)
                color_bgr = (254, 242, 0) if is_compliant else (100, 40, 255)
                
                # 1. Semi-transparent faint fill for bounding box
                cv2.rectangle(overlay, (x1, y1), (x2, y2), color_bgr, -1)
                
                # 2. Glowing Corner Bounding Box (Sleek)
                self._draw_corners(frame, (x1, y1), (x2, y2), color_bgr, thickness=1, length=20)
                
                # 3. Subtle Scanning Animation
                scan_y = y1 + int(((math.sin(time.time() * 4 + track_id) + 1) / 2) * (y2 - y1))
                cv2.line(overlay, (x1, scan_y), (x2, scan_y), color_bgr, 2)
                cv2.line(frame, (x1, scan_y), (x2, scan_y), (255, 255, 255), 1)
                
                # 4. Top Label Panel (Modern Layout)
                label = f" ID:{track_id} | {status_str} | {confidence_pct}% "
                (label_w, label_h), _ = cv2.getTextSize(label, cv2.FONT_HERSHEY_SIMPLEX, 0.45, 1)
                # Dark pill-shaped background (using a rectangle here for simplicity but styled cleanly)
                cv2.rectangle(overlay, (x1, y1 - 28), (x1 + label_w, y1 - 4), (10, 10, 15), -1)
                
                # Text on frame directly for sharpness
                text_color = (255, 255, 255) # Always white text for high contrast modern look
                cv2.putText(frame, label, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.45, text_color, 1)
                
                # 5. Side PPE Item Panel
                panel_x = x2 + 12
                panel_y = y1 + 10
                for item, is_detected in ppe_status.items():
                    item_name = item.replace("_", " ").upper()
                    # Cyan check, Pink cross
                    item_color = (254, 242, 0) if is_detected else (100, 40, 255)
                    
                    text_line = f"   {item_name}" # Space for the symbol
                    (tw, th), _ = cv2.getTextSize(text_line, cv2.FONT_HERSHEY_SIMPLEX, 0.4, 1)
                    
                    # Sleek dark background per item
                    cv2.rectangle(overlay, (panel_x, panel_y - th - 6), (panel_x + tw + 16, panel_y + 8), (10, 10, 15), -1)
                    
                    # Clean text
                    cv2.putText(frame, text_line, (panel_x + 8, panel_y + 2), cv2.FONT_HERSHEY_SIMPLEX, 0.4, (240, 240, 240), 1)
                    
                    # Modern Check/Cross symbol
                    if is_detected:
                        self._draw_check(frame, (panel_x + 6, panel_y - 6), 8, item_color, 2)
                    else:
                        self._draw_cross(frame, (panel_x + 6, panel_y - 6), 8, item_color, 2)
                        
                    panel_y += 26
                    
        # 6. Bottom Summary HUD (Cyber-tech bar)
        if overall_results:
            all_present = set()
            all_missing = set()
            for res in overall_results:
                for item, is_detected in res["ppe"].items():
                    item_clean = item.replace("_", " ").upper()
                    if is_detected:
                        all_present.add(item_clean)
                    else:
                        all_missing.add(item_clean)
                        
            present_str = f"DETECTED: {', '.join(all_present) if all_present else 'NONE'}"
            missing_str = f"MISSING: {', '.join(all_missing) if all_missing else 'NONE'}"
            
            # Sleek bottom bar
            cv2.rectangle(overlay, (0, h - 80), (w, h), (5, 5, 8), -1)
            
            # Blend overlay (alpha=0.25 for a glassy modern look)
            cv2.addWeighted(overlay, 0.25, frame, 0.75, 0, frame)
            
            # Accent line on top of bottom bar
            cv2.line(frame, (0, h - 80), (w, h - 80), (254, 242, 0), 1)
            
            # Draw bottom summary text
            cv2.putText(frame, present_str, (20, h - 45), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (254, 242, 0), 1)
            cv2.putText(frame, missing_str, (20, h - 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (100, 40, 255), 1)
        else:
            # If no detections, just blend empty overlay or do nothing
            pass

        return frame, overall_results
        
    def _draw_corners(self, img, pt1, pt2, color, thickness=1, length=20):
        x1, y1 = pt1
        x2, y2 = pt2
        
        # Outer soft glow
        glow_t = thickness + 3
        for t, c in [(glow_t, color), (thickness, (255, 255, 255))]:
            # Top-left
            cv2.line(img, (x1, y1), (x1 + length, y1), c, t)
            cv2.line(img, (x1, y1), (x1, y1 + length), c, t)
            # Top-right
            cv2.line(img, (x2, y1), (x2 - length, y1), c, t)
            cv2.line(img, (x2, y1), (x2, y1 + length), c, t)
            # Bottom-left
            cv2.line(img, (x1, y2), (x1 + length, y2), c, t)
            cv2.line(img, (x1, y2), (x1, y2 - length), c, t)
            # Bottom-right
            cv2.line(img, (x2, y2), (x2 - length, y2), c, t)
            cv2.line(img, (x2, y2), (x2, y2 - length), c, t)

    def _draw_check(self, img, pt, size, color, thickness=2):
        x, y = pt
        cv2.line(img, (x, y + size//2), (x + int(size*0.4), y + size), color, thickness)
        cv2.line(img, (x + int(size*0.4), y + size), (x + size, y - int(size*0.2)), color, thickness)

    def _draw_cross(self, img, pt, size, color, thickness=2):
        x, y = pt
        cv2.line(img, (x, y), (x + size, y + size), color, thickness)
        cv2.line(img, (x + size, y), (x, y + size), color, thickness)
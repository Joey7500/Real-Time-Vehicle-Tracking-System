import cv2
import numpy as np

def draw_bbox(frame, xyxy, color=(0,255,0), label=None):
    x1,y1,x2,y2 = map(int, xyxy)
    cv2.rectangle(frame, (x1,y1), (x2,y2), color, 2)
    if label:
        cv2.putText(frame, label, (x1, max(0,y1-6)), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)

def put_hud(frame, speed_kmh=None, type_label=None, mm_label=None, plate_text=None):
    y = 24
    for key,val in [("Speed", speed_kmh),("Type", type_label),("Make/Model", mm_label),("Plate", plate_text)]:
        if val is None: continue
        cv2.putText(frame, f"{key}: {val}", (10,y), cv2.FONT_HERSHEY_SIMPLEX, 0.6,(255,255,255),2)
        y += 24

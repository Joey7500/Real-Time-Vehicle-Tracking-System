import cv2
import numpy as np

def apply_roi_mask(frame, detections, mask):
    if mask is None: return detections
    h,w = frame.shape[:2]
    kept = []
    for b,cls,conf in detections:
        x1,y1,x2,y2 = map(int,b)
        x1 = max(0,min(x1,w-1)); x2 = max(0,min(x2,w-1))
        y1 = max(0,min(y1,h-1)); y2 = max(0,min(y2,h-1))
        patch = mask[y1:y2, x1:x2]
        if patch.size>0 and patch.mean() > 10:  # some part overlaps road
            kept.append((b,cls,conf))
    return kept

def load_mask(path):
    if not path: return None
    m = cv2.imread(path, cv2.IMREAD_GRAYSCALE)
    return m

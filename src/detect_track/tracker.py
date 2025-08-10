# Minimal IOU-based tracker stub; swap with ByteTrack/DeepSORT later.
import itertools
import numpy as np

def iou(a, b):
    ax1,ay1,ax2,ay2 = a; bx1,by1,bx2,by2 = b
    inter_x1, inter_y1 = max(ax1,bx1), max(ay1,by1)
    inter_x2, inter_y2 = min(ax2,bx2), min(ay2,by2)
    iw, ih = max(0, inter_x2-inter_x1), max(0, inter_y2-inter_y1)
    inter = iw*ih
    area_a = (ax2-ax1)*(ay2-ay1); area_b = (bx2-bx1)*(by2-by1)
    union = area_a + area_b - inter + 1e-6
    return inter/union

class SimpleTracker:
    _next_id = itertools.count(1)
    def __init__(self, iou_thres=0.3, max_age=30):
        self.tracks = {}  # id: {'box':..., 'age':0, 'history':[(cx,cy,t),...]}
        self.iou_thres = iou_thres; self.max_age = max_age

    def update(self, detections, tstamp):
        # detections: list[(box, cls, conf)]
        assigned = set()
        # match existing
        for tid, tr in list(self.tracks.items()):
            best_j, best_iou = -1, 0.0
            for j,(box,cls,conf) in enumerate(detections):
                if j in assigned: continue
                s = iou(tr['box'], box)
                if s > best_iou:
                    best_iou, best_j = s, j
            if best_iou >= self.iou_thres and best_j>=0:
                box, cls, conf = detections[best_j]
                tr['box'] = box; tr['cls']=cls; tr['conf']=conf; tr['age']=0
                cx = (box[0]+box[2])/2; cy=(box[1]+box[3])/2
                tr['history'].append((cx,cy,tstamp))
                assigned.add(best_j)
            else:
                tr['age'] += 1
                if tr['age'] > self.max_age:
                    del self.tracks[tid]
        # new tracks
        for j,(box,cls,conf) in enumerate(detections):
            if j in assigned: continue
            tid = next(self._next_id)
            cx = (box[0]+box[2])/2; cy=(box[1]+box[3])/2
            self.tracks[tid] = {'box':box, 'cls':cls, 'conf':conf, 'age':0, 'history':[(cx,cy,tstamp)]}
        # return active
        return {tid: tr for tid,tr in self.tracks.items()}

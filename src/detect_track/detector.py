from ultralytics import YOLO

class Detector:
    def __init__(self, weights_path, conf=0.25, iou=0.45, classes_keep=None):
        self.model = YOLO(weights_path)
        self.conf = conf; self.iou = iou
        self.classes_keep = set(classes_keep) if classes_keep else None

    def infer(self, frame):
        results = self.model.predict(frame, conf=self.conf, iou=self.iou, verbose=False)
        det = results[0]
        boxes = det.boxes.xyxy.cpu().numpy() if det.boxes is not None else []
        clss  = det.boxes.cls.cpu().numpy().astype(int) if det.boxes is not None else []
        confs = det.boxes.conf.cpu().numpy() if det.boxes is not None else []
        out = []
        for b,c,cf in zip(boxes, clss, confs):
            if self.classes_keep and c not in self.classes_keep: continue
            out.append((b, int(c), float(cf)))
        return out

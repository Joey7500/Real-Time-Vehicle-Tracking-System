# Placeholder Make/Model recognizer (confidence-gated; returns None for now).
class MakeModelRecognizer:
    def __init__(self, weights=None, min_conf=0.8):
        self.min_conf = min_conf
    def infer(self, crop_bgr):
        return None, 0.0

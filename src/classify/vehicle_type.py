# Placeholder Type Classifier (returns "unknown" until model is added).
class VehicleTypeClassifier:
    def __init__(self, weights=None, labels=None):
        self.labels = labels or ["sedan","hatchback","suv","van","pickup","truck","bus","motorcycle"]
    def infer(self, crop_bgr):
        return "unknown", 0.0

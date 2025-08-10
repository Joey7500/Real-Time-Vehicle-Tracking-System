# Minimal placeholder: you can integrate OpenALPR or other LPR libraries here.
# For privacy, only return result if confidence is high, and store with TTL.
class ALPR:
    def __init__(self, country="eu"):
        self.country = country
    def infer(self, crop_bgr):
        return None, 0.0

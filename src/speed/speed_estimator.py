import numpy as np

class SpeedEstimator:
    def __init__(self, fps, units="kmh"):
        self.fps = fps
        self.units = units

    def speed_from_history(self, history, img_to_world_func):
        # history: list of (cx, cy, tstamp) in consecutive frames
        if len(history) < 2: return 0.0
        (x1,y1,t1), (x2,y2,t2) = history[-2], history[-1]
        wx1, wy1 = img_to_world_func((x1,y1))
        wx2, wy2 = img_to_world_func((x2,y2))
        dist_m = np.hypot(wx2-wx1, wy2-wy1)
        dt = max(1e-6, (t2 - t1))
        mps = dist_m / dt
        if self.units == "kmh":
            return mps * 3.6
        return mps

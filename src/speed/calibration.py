import numpy as np
import cv2

class HomographyCalibrator:
    def __init__(self, image_points, world_points_m):
        ip = np.array(image_points, dtype=np.float32)
        wp = np.array(world_points_m, dtype=np.float32)
        self.H, _ = cv2.findHomography(ip, wp)  # maps image->world (x,y)
    def img_to_world(self, xy):
        x,y = xy
        p = np.array([[x,y]], dtype=np.float32)
        p = cv2.perspectiveTransform(p[None, ...], self.H)[0,0]
        return float(p[0]), float(p[1])

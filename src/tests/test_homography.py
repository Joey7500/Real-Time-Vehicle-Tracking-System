import numpy as np
from src.speed.calibration import HomographyCalibrator

def test_homography_square():
    ip = [(0,0),(10,0),(0,10),(10,10)]
    wp = [(0,0),(5,0),(0,5),(5,5)]
    H = HomographyCalibrator(ip, wp)
    assert np.allclose(H.img_to_world((5,5)), (2.5,2.5), atol=1e-2)

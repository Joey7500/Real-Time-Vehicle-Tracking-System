from src.speed.speed_estimator import SpeedEstimator

def test_speed_basic():
    est = SpeedEstimator(fps=10, units="kmh")
    hist = [(0,0,0.0),(10,0,1.0)]
    # img_to_world: 1 pixel = 0.1m (dummy)
    f = lambda xy: (xy[0]*0.1, xy[1]*0.1)
    v = est.speed_from_history(hist, f)
    # 1m in 1s -> 3.6km/h
    assert abs(v - 3.6) < 1e-3

import time, argparse, cv2
from src.utils.config import load_yaml, env
from src.utils.log import get_logger
from src.utils.drawing import draw_bbox, put_hud
from src.capture.camera import VideoSource
from src.detect_track.detector import Detector
from src.detect_track.tracker import SimpleTracker
from src.detect_track.postprocess import load_mask, apply_roi_mask
from src.speed.calibration import HomographyCalibrator
from src.speed.speed_estimator import SpeedEstimator
from src.classify.vehicle_type import VehicleTypeClassifier
from src.classify.make_model import MakeModelRecognizer
from src.alpr.alpr_openalpr import ALPR
from src.storage.db import get_session
from src.storage.crud import insert_event, update_hour_rollup

log = get_logger()

def crop(frame, box):
    x1,y1,x2,y2 = map(int, box); return frame[max(0,y1):max(0,y2), max(0,x1):max(0,x2)]

def main(video=None, camera=None, pi=False):
    cam_cfg = load_yaml("configs/camera_config.yaml")
    mdl_cfg = load_yaml("configs/models.yaml")

    fps = cam_cfg.get("fps", 30)
    mask = load_mask(cam_cfg.get("roi_mask_path"))
    calib = HomographyCalibrator(cam_cfg["homography"]["image_points"],
                                 cam_cfg["homography"]["world_points_m"])
    speed = SpeedEstimator(fps=fps, units=cam_cfg.get("speed_units","kmh"))
    speed_limit = cam_cfg.get("speed_limit_kmh", 50)

    det = Detector(mdl_cfg["detector"]["yolo_weights"],
                   conf=mdl_cfg["detector"]["conf_thres"],
                   iou=mdl_cfg["detector"]["iou_thres"],
                   classes_keep=mdl_cfg["detector"]["classes_keep"])
    trk = SimpleTracker(iou_thres=mdl_cfg["tracker"]["iou_threshold"],
                        max_age=mdl_cfg["tracker"]["max_age"])

    typ = VehicleTypeClassifier(weights=mdl_cfg["type_classifier"]["weights"],
                                labels=mdl_cfg["type_classifier"]["labels"])
    mm = MakeModelRecognizer(weights=mdl_cfg["make_model"]["weights"],
                             min_conf=mdl_cfg["make_model"]["min_confidence"])
    alpr = ALPR(country="eu")

    src = video if video else (camera if camera is not None else env("VIDEO_SOURCE", 0, int))
    cap = VideoSource(src=src,
                      width=env("FRAME_WIDTH", None, int),
                      height=env("FRAME_HEIGHT", None, int),
                      fps=env("FPS", None, int))

    t0 = time.time()
    with get_session() as s:
        while True:
            ok, frame = cap.read()
            if not ok: break
            t = time.time() - t0

            dets = det.infer(frame)
            dets = apply_roi_mask(frame, dets, mask)

            tracks = trk.update(dets, t)
            for tid, tr in tracks.items():
                spd = speed.speed_from_history(tr["history"], calib.img_to_world)
                typ_label, typ_conf = typ.infer(crop(frame, tr["box"]))
                mm_label,  mm_conf  = mm.infer(crop(frame, tr["box"]))
                plate_text, plate_conf = alpr.infer(crop(frame, tr["box"]))

                over = spd > speed_limit
                event_id = insert_event(s,
                                        track_id=tid,
                                        type_label=typ_label,
                                        make_model=mm_label,
                                        speed_kmh=spd,
                                        over_limit=over,
                                        plate_text=plate_text)
                update_hour_rollup(s, s.query(type("E",(Event:=None),{}) ).get(event_id) if False else s.query(__import__('src.storage.models',fromlist=['Event']).Event).get(event_id))

                label = f"ID {tid} | {spd:.1f} km/h"
                if typ_label and typ_label!="unknown": label += f" | {typ_label}"
                if mm_label: label += f" | {mm_label}"
                if plate_text: label += f" | {plate_text}"
                draw_bbox(frame, tr["box"], (0,255,0), label=None)
                put_hud(frame, speed_kmh=f"{spd:.1f}", type_label=typ_label,
                        mm_label=mm_label, plate_text=plate_text)

            cv2.imshow("RT Vehicle Tracking (In Progress)", frame)
            if cv2.waitKey(1) & 0xFF == 27: break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--video", type=str, default=None)
    parser.add_argument("--camera", type=int, default=None)
    parser.add_argument("--pi", action="store_true")
    args = parser.parse_args()
    main(video=args.video, camera=args.camera, pi=args.pi)

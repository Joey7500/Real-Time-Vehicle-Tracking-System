# Real-Time Vehicle Tracking System (In Progress)

A modular roadside analytics project for **Raspberry Pi 5** + **ArduCam**.  
Detects and tracks vehicles, estimates speed from a calibrated scene, classifies vehicle type (and later make/model), and offers optional privacy-aware license plate OCR with a 7-day retention policy.  
Events are stored for dashboards and time-series statistics.

---

## 📷 Example Setup

| Street View | Camera | Raspberry Pi 5 |
|-------------|--------|----------------|
| ![Street view placeholder](images/street_placeholder.jpg) | ![Camera placeholder](images/camera_placeholder.jpg) | ![Pi5 setup](images/pi5_setup.jpg) |

---

## 🚀 Features

- **YOLO detection + tracker stub** (upgrade path: ByteTrack / DeepSORT)
- **Homography-based speed estimation** in km/h
- **Coarse vehicle type classifier stub**; make/model recognition planned
- **Optional ALPR** with rolling deletion policy
- **SQLite + FastAPI API + Streamlit dashboard**
- **Config-driven**; unit tests for geometry and speed math

---

## 📂 Repository Layout
src/        → capture, detect_track, speed, classify, alpr, storage, utils, app
configs/    → camera_config.yaml, models.yaml, retention.yaml
scripts/    → run_local_demo.sh, run_pi5.sh, init_db.py
data/       → calibration images, ROI mask, demo clip
models/     → weights (ignored in git)


## 🖥️ Quick Demo
# Install dependencies
pip install -r requirements.txt

# Initialize database
python scripts/init_db.py

# Start FastAPI service
uvicorn src.app.service:app --host 0.0.0.0 --port 8080

# Run local demo (expects data/demo/sample_clip.mp4)
bash scripts/run_local_demo.sh

# In another terminal, start the dashboard:
streamlit run src/app/dashboard.py

##🛣️ Roadmap
#Replace SimpleTracker with ByteTrack / DeepSORT

#Train vehicle type model; add make/model (confidence-gated)

#WebSocket live events; richer dashboard; Pi5 acceleration

##⚖️ Privacy & Legal

#IF ALPR is enabled, keep plate text for max 7 days (configurable) and avoid long-term storage.

##📌 Status
#Core pipeline, API, DB, and dashboard scaffolding are in place.

#Classification and ALPR are currently placeholders.

#Marked “In Progress” on resume; active development planned.



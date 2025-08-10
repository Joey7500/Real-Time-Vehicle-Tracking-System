from fastapi import FastAPI
from pydantic import BaseModel
from src.storage.db import get_session
from src.storage.models import Event, AggregateHour

app = FastAPI(title="RT Vehicle Tracking API")

class EventOut(BaseModel):
    id: int; tstamp: str; track_id: int
    type_label: str | None
    make_model: str | None
    speed_kmh: float
    over_limit: bool
    plate_text: str | None

@app.get("/health")
def health():
    return {"status":"ok"}

@app.get("/latest", response_model=list[EventOut])
def latest(n: int = 20):
    with get_session() as s:
        rows = s.query(Event).order_by(Event.id.desc()).limit(n).all()
        return [EventOut(
            id=r.id, tstamp=str(r.tstamp), track_id=r.track_id,
            type_label=r.type_label, make_model=r.make_model,
            speed_kmh=r.speed_kmh, over_limit=r.over_limit, plate_text=r.plate_text
        ) for r in rows]

@app.get("/agg/hour")
def agg_hour(n: int = 48):
    with get_session() as s:
        rows = s.query(AggregateHour).order_by(AggregateHour.id.desc()).limit(n).all()
        return [{"hour": r.hour, "count": r.count, "speeding": r.speeding} for r in rows]

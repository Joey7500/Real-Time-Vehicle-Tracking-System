import datetime as dt
from sqlalchemy import select, delete
from .models import Event, AggregateHour
from sqlalchemy.orm import Session

def insert_event(s: Session, **fields):
    ev = Event(**fields)
    s.add(ev); s.commit()
    return ev.id

def delete_alpr_older_than(s: Session, cutoff: dt.datetime):
    s.execute(delete(Event).where(Event.tstamp < cutoff))
    s.commit()

def update_hour_rollup(s: Session, ev: Event):
    hour_key = ev.tstamp.strftime("%Y-%m-%d %H:00")
    row = s.execute(select(AggregateHour).where(AggregateHour.hour==hour_key)).scalar_one_or_none()
    if not row:
        row = AggregateHour(hour=hour_key, count=0, speeding=0)
        s.add(row)
    row.count += 1
    if ev.over_limit:
        row.speeding += 1
    s.commit()

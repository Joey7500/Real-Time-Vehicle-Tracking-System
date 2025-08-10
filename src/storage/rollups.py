from .db import get_session
from .models import Event
from .crud import update_hour_rollup

def rollup_recent():
    with get_session() as s:
        for ev in s.query(Event).order_by(Event.id.desc()).limit(100).all():
            update_hour_rollup(s, ev)

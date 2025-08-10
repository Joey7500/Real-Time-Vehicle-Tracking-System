import datetime as dt
from src.storage.crud import delete_alpr_older_than

def purge_old_alpr(session_factory, days=7):
    cutoff = dt.datetime.utcnow() - dt.timedelta(days=days)
    with session_factory() as s:
        delete_alpr_older_than(s, cutoff)

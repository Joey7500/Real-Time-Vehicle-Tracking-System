from src.storage.db import init_engine, get_session
from src.storage.models import Base, VehicleType

engine = init_engine()
Base.metadata.create_all(engine)

with get_session() as s:
    if not s.query(VehicleType).count():
        s.add_all([VehicleType(name=n) for n in
                   ["sedan","hatchback","suv","van","pickup","truck","bus","motorcycle"]])
        s.commit()
print("DB initialized.")

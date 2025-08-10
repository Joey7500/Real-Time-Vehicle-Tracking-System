from sqlalchemy.orm import declarative_base, relationship, Mapped, mapped_column
from sqlalchemy import Integer, String, Float, DateTime, ForeignKey, Boolean, func

Base = declarative_base()

class VehicleType(Base):
    __tablename__ = "vehicle_types"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String, unique=True)

class Event(Base):
    __tablename__ = "events"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    tstamp: Mapped = mapped_column(DateTime(timezone=True), server_default=func.now())
    track_id: Mapped[int] = mapped_column(Integer, index=True)
    type_label: Mapped[str] = mapped_column(String, nullable=True)
    make_model: Mapped[str] = mapped_column(String, nullable=True)
    speed_kmh: Mapped[float] = mapped_column(Float, default=0.0)
    over_limit: Mapped[bool] = mapped_column(Boolean, default=False)
    plate_text: Mapped[str] = mapped_column(String, nullable=True)  # keep brief; purge later

class AggregateHour(Base):
    __tablename__ = "agg_hour"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    hour: Mapped[str] = mapped_column(String, index=True)  # YYYY-MM-DD HH:00
    count: Mapped[int] = mapped_column(Integer, default=0)
    speeding: Mapped[int] = mapped_column(Integer, default=0)

from sqlalchemy import String, DateTime, func, JSON, Float
from sqlalchemy.orm import Mapped, mapped_column
from .db import Base

class Project(Base):
    __tablename__ = "projects"
    id: Mapped[str] = mapped_column(String, primary_key=True)
    name: Mapped[str] = mapped_column(String, nullable=False)
    location: Mapped[str | None] = mapped_column(String, nullable=True)
    created_at: Mapped[str] = mapped_column(DateTime(timezone=True), server_default=func.now())

class Appraisal(Base):
    __tablename__ = "appraisals"
    id: Mapped[str] = mapped_column(String, primary_key=True)
    project_id: Mapped[str] = mapped_column(String, nullable=False, index=True)
    version_name: Mapped[str] = mapped_column(String, nullable=False)

    assumptions: Mapped[dict] = mapped_column(JSON, nullable=False)
    outputs: Mapped[dict] = mapped_column(JSON, nullable=False)

    # indexed KPIs for filtering/sorting
    gdv: Mapped[float] = mapped_column(Float, nullable=False, default=0)
    tdc: Mapped[float] = mapped_column(Float, nullable=False, default=0)
    profit: Mapped[float] = mapped_column(Float, nullable=False, default=0)
    profit_margin: Mapped[float] = mapped_column(Float, nullable=False, default=0)
    residual_land_value: Mapped[float] = mapped_column(Float, nullable=False, default=0)

    created_at: Mapped[str] = mapped_column(DateTime(timezone=True), server_default=func.now())

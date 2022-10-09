"""SQLALchmy ORM models for the database objects"""

from sqlalchemy import Column, Integer, String, Date, Float, ForeignKeyConstraint
from sqlalchemy.orm import relationship

from .database import Base

class Ship(Base):
    __tablename__ = "ships"

    imo_number = Column(Integer, index=True, primary_key=True)
    reporting_period = Column(Integer, primary_key=True)
    name = Column(String)
    ship_type = Column(String)
    technical_efficiency = Column(String)
    port_of_registry = Column(String)
    home_port = Column(String)
    ice_class = Column(String)
    doc_issue_date = Column(Date)
    doc_expiry_date = Column(Date)

    monitoring_results = relationship("MonitoringResult", back_populates="ship")

class MonitoringResult(Base):
    __tablename__ = "monitoring_results"
    __table_args__ = (
            ForeignKeyConstraint(
        ["ship_imo_number", "ship_reporting_period"], ["ships.imo_number", "ships.reporting_period"]
        ),
    )

    id = Column(Integer, primary_key=True)
    total_fuel_consumption = Column(Float)
    total_co2_emissions = Column(Float)
    annual_time_spent_at_sea = Column(Float)
    average_fuel_consumption_per_distance = Column(Float)
    average_co2_emissions_per_distance = Column(Float)
    ship_imo_number = Column(Integer)
    ship_reporting_period = Column(Integer)

    ship = relationship(
        "Ship",
        foreign_keys="[MonitoringResult.ship_imo_number, MonitoringResult.ship_reporting_period]",
        back_populates="monitoring_results",
    )
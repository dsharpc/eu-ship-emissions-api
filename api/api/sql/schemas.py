"""Pydantic schemas for FastAPI"""

from pydantic import BaseModel
from datetime import date

class MonitoringResult(BaseModel):
    reporting_period: int
    total_fuel_consumption: float
    total_co2_emissions: float
    annual_time_spent_at_sea: float
    average_fuel_consumption_per_distance: float
    average_co2_emissions_per_distance: float
    imo_number: int
    reporting_period: int

    class Config:
        orm_mode = True

class Ship(BaseModel):
    imo_number: int
    reporting_period: int
    name: str
    ship_type: str
    technical_efficiency: str
    port_of_registry: str
    home_port: str
    ice_class: str
    doc_issue_date: date
    doc_expiry_date: date

    class Config:
        orm_mode = True
"""Pydantic schemas for FastAPI"""

from typing import Optional
from pydantic import BaseModel
from datetime import date

class MonitoringResult(BaseModel):
    ship_imo_number: int
    ship_reporting_period: int
    total_fuel_consumption: Optional[float]
    total_co2_emissions: Optional[float]
    annual_time_spent_at_sea: Optional[float]
    average_fuel_consumption_per_distance: Optional[float]
    average_co2_emissions_per_distance: Optional[float]

    class Config:
        orm_mode = True

class Ship(BaseModel):
    imo_number: int
    reporting_period: int
    name: str
    ship_type: Optional[str]
    technical_efficiency: Optional[str]
    port_of_registry: Optional[str]
    home_port: Optional[str]
    ice_class: Optional[str]
    doc_issue_date: date
    doc_expiry_date: date

    class Config:
        orm_mode = True


class ThetisMRVMonitoringResult(BaseModel):
    total_co2_emissions: Optional[float]
    average_co2_emissions_per_distance: Optional[float]
    annual_time_spent_at_sea: Optional[float]

    class Config:
        orm_mode = True

class ThetisMRVView(BaseModel):
    imo_number: int
    name: str
    ship_type: str
    technical_efficiency: Optional[str]
    reporting_period: int
    monitoring_results: list[ThetisMRVMonitoringResult]

    class Config:
        orm_mode = True



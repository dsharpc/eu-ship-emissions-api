"""CRUD operatinos executed via the SQLAlchemy ORM"""

from sqlalchemy.orm import Session
from . import models, schemas

def get_ship(db: Session, imo_number: int, reporting_period: int) -> models.Ship:
    """Query database and return Ship object with given imo_number and reporting_period

    Parameters
    ----------
    db : Session
    imo_number : int
        IMO to filter by
    reporting_period : int
        Reporting period to filter by

    Returns
    -------
    models.Ship
        Matching record or None if it doesn't exist
    """
    return db.query(models.Ship)\
        .filter(models.Ship.imo_number == imo_number)\
            .filter(models.Ship.reporting_period == reporting_period).first()


def create_ship(db: Session, ship: schemas.Ship) -> models.Ship:
    """Create Ship record in database using SQLAlchemy's ORM

    Parameters
    ----------
    db : Session
    ship : schemas.Ship
        Pydantic Ship model with data

    Returns
    -------
    models.Ship
        Object for the just created record
    """
    db_ship = models.Ship(imo_number=ship.imo_number,
                            reporting_period=ship.reporting_period,
                            name=ship.name,
                            ship_type=ship.ship_type,
                            technical_efficiency=ship.technical_efficiency,
                            port_of_registry=ship.port_of_registry,
                            home_port=ship.home_port,
                            ice_class=ship.ice_class,
                            doc_issue_date=ship.doc_issue_date,
                            doc_expiry_date=ship.doc_expiry_date)
    db.add(db_ship)
    db.commit()
    db.refresh(db_ship)
    return db_ship

def get_monitoring_result(db: Session, imo_number: int, reporting_period: int) -> models.MonitoringResult:
    """Query database and return Ship object with given imo_number and reporting_period

    Parameters
    ----------
    db : Session
    imo_number : int
        IMO to filter by
    reporting_period : int
        Reporting period to filter by

    Returns
    -------
    models.MonitoringResult
        Matched MonitoringResult record if it exists, None if it doesn't
    """
    return db.query(models.MonitoringResult)\
        .filter(models.MonitoringResult.ship_imo_number == imo_number)\
            .filter(models.MonitoringResult.ship_reporting_period == reporting_period).first()

def create_monitoring_result(db: Session, monitoring_result: schemas.MonitoringResult) -> models.MonitoringResult:
    """Create Monitorint Result record in database using SQLAlchemy's ORM

    Parameters
    ----------
    db : Session
    ship : schemas.MonitoringResult
        Pydantic MonitoringResult model with data

    Returns
    -------
    models.MonitoringResult
        Object for the just created record
    """
    db_monitoring_result = models.MonitoringResult(total_fuel_consumption=monitoring_result.total_fuel_consumption,
                            total_co2_emissions=monitoring_result.total_co2_emissions,
                            annual_time_spent_at_sea=monitoring_result.annual_time_spent_at_sea,
                            average_fuel_consumption_per_distance=monitoring_result.average_fuel_consumption_per_distance,
                            average_co2_emissions_per_distance=monitoring_result.average_co2_emissions_per_distance,
                            ship_imo_number=monitoring_result.imo_number,
                            ship_reporting_period=monitoring_result.reporting_period)
    db.add(db_monitoring_result)
    db.commit()
    db.refresh(db_monitoring_result)
    return db_monitoring_result